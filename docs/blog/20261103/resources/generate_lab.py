#!/usr/bin/env python3
"""Build a core-only three-S-NSSAI, three-UPF demo from a compatible ci-test checkout.

Requires PyYAML. Only GENERATED targets under config/slicing-demo/ and
composes/docker-compose-slicing-demo.yaml are changed. Source YAML is read-only.
All seven generated files are prepared before any target is replaced; failed
replacements are rolled back from staged backups on a best-effort basis.
"""

import argparse
import copy
import ipaddress
import os
from pathlib import Path
import shutil
import sys
import tempfile
import yaml

SLICES = (
    dict(label="embb", sst=1, sd="010203", pool="10.60.0.0/16", static="10.60.100.0/24", host=81),
    dict(label="urllc", sst=2, sd="000001", pool="10.61.0.0/16", static="10.61.100.0/24", host=82),
    dict(label="miot", sst=3, sd="000001", pool="10.62.0.0/16", static="10.62.100.0/24", host=83),
)
KEEP = {
    "db", "free5gc-nrf", "free5gc-amf", "free5gc-ausf", "free5gc-nssf",
    "free5gc-pcf", "free5gc-smf", "free5gc-udm", "free5gc-udr",
}


def read_yaml(path):
    if not path.is_file():
        raise FileNotFoundError(f"Required ci-test source file is missing: {path}")
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a YAML mapping in {path}")
    return data


def required(mapping, *keys):
    current = mapping
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            raise ValueError(f"Incompatible upstream ci-test config: missing {'.'.join(map(str, keys))}")
        current = current[key]
    return current


def snssai(entry):
    return {"sst": entry["sst"], "sd": entry["sd"]}


def generate(root, net, bridge):
    config_dir, compose_dir = root / "config", root / "composes"
    paths = {
        "compose": compose_dir / "docker-compose-ci-e2e-basic.yaml",
        "smf": config_dir / "smfCfg.yaml",
        "nssf": config_dir / "nssfCfg.yaml",
        "amf": config_dir / "amfCfg.yaml",
        "upf": config_dir / "upfCfg.yaml",
        "routing": config_dir / "ueRoutingCfg.yaml",
    }
    sources = {name: read_yaml(path) for name, path in paths.items()}
    out = {}
    dest = config_dir / "slicing-demo"

    # Configure the AMF's PLMN slice support lists.
    amf = copy.deepcopy(sources["amf"])
    plmns = required(amf, "configuration", "plmnSupportList")
    if not isinstance(plmns, list) or not plmns:
        raise ValueError("AMF plmnSupportList must be nonempty")
    for plmn in plmns:
        plmn["snssaiList"] = [snssai(s) for s in SLICES]
    tais = required(amf, "configuration", "supportTaiList")
    if not isinstance(tais, list) or not tais:
        raise ValueError("AMF supportTaiList must be nonempty")
    for tai in tais:
        tai["tac"] = str(tai["tac"]).zfill(6)
    out[dest / "amfCfg.yaml"] = amf

    nssf = copy.deepcopy(sources["nssf"])
    nc = required(nssf, "configuration")
    supported = required(nc, "supportedNssaiInPlmnList")
    if not isinstance(supported, list) or not supported:
        raise ValueError("NSSF supportedNssaiInPlmnList must be nonempty")
    for entry in supported:
        entry["supportedSnssaiList"] = [snssai(s) for s in SLICES]
    nrf_id = required(nc, "nrfUri").rstrip("/") + "/nnrf-nfm/v1/nf-instances"
    nc["nsiList"] = [
        {"snssai": snssai(s), "nsiInformationList": [{"nrfId": nrf_id, "nsiId": i + 1}]}
        for i, s in enumerate(SLICES)
    ]
    plmn_id = copy.deepcopy(required(amf, "configuration", "servedGuamiList")[0]["plmnId"])
    tac = tais[0]["tac"]
    for amf_set in nc.get("amfSetList", []):
        for availability in amf_set.get("supportedNssaiAvailabilityData", []):
            availability["tai"] = {"plmnId": copy.deepcopy(plmn_id), "tac": tac}
            availability["supportedSnssaiList"] = [snssai(s) for s in SLICES]
    out[dest / "nssfCfg.yaml"] = nssf

    smf = copy.deepcopy(sources["smf"])
    sc = required(smf, "configuration")
    base_snssai = required(sc, "snssaiInfos")
    if not isinstance(base_snssai, list) or not base_snssai:
        raise ValueError("SMF snssaiInfos must be nonempty")
    available_dnns = required(base_snssai[0], "dnnInfos")
    internet_dnns = [copy.deepcopy(d) for d in available_dnns if d.get("dnn") == "internet"]
    if len(internet_dnns) != 1:
        raise ValueError("Expected exactly one 'internet' DNN entry in first upstream SMF S-NSSAI")
    sc["snssaiInfos"] = [
        {"sNssai": snssai(s), "dnnInfos": copy.deepcopy(internet_dnns)}
        for s in SLICES
    ]
    up_nodes = {"gNB1": {"type": "AN"}}  # conceptual; gNB is not started
    links = []
    for s in SLICES:
        fqdn = f'upf-{s["label"]}.free5gc.org'
        up_key = "UPF_" + s["label"].upper()
        up_nodes[up_key] = {
            "type": "UPF", "nodeID": fqdn, "addr": fqdn,
            "sNssaiUpfInfos": [{
                "sNssai": snssai(s),
                "dnnUpfInfoList": [{
                    "dnn": "internet", "pools": [{"cidr": s["pool"]}],
                    "staticPools": [{"cidr": s["static"]}],
                }],
            }],
            "interfaces": [{
                "interfaceType": "N3", "endpoints": [fqdn], "networkInstances": ["internet"],
            }],
        }
        links.append({"A": "gNB1", "B": up_key})
    sc["userplaneInformation"] = {"upNodes": up_nodes, "links": links}
    sc.pop("ulcl", None)
    out[dest / "smfCfg.yaml"] = smf

    for s in SLICES:
        upf = copy.deepcopy(sources["upf"])
        fqdn = f'upf-{s["label"]}.free5gc.org'
        required(upf, "pfcp")["addr"] = fqdn
        upf["pfcp"]["nodeID"] = fqdn
        required(upf, "gtpu")["ifList"] = [{"addr": fqdn, "type": "N3"}]
        upf["dnnList"] = [{
            "dnn": "internet", "cidr": s["pool"], "natIfCIDR": str(net),
            "ipForwardEnable": True,
        }]
        out[dest / f'upf-{s["label"]}.yaml'] = upf

    compose = copy.deepcopy(sources["compose"])
    services = required(compose, "services")
    missing = KEEP.union({"free5gc-upf"}) - set(services)
    if missing:
        raise ValueError(f"CI-test basic Compose missing expected service(s): {sorted(missing)}")
    base_upf = copy.deepcopy(services["free5gc-upf"])
    compose["services"] = {k: v for k, v in services.items() if k in KEEP}
    compose["name"] = "free5gc-slicing-demo"
    for s in SLICES:
        label = s["label"]
        upf = copy.deepcopy(base_upf)
        upf["container_name"] = "slice-upf-" + label
        upf["volumes"] = [f"../config/slicing-demo/upf-{label}.yaml:/free5gc/config/upfcfg.yaml:ro"]
        upf["networks"] = {"privnet": {
            "aliases": [f"upf-{label}.free5gc.org"],
            "ipv4_address": str(net.network_address + s["host"]),
        }}
        compose["services"]["free5gc-upf-" + label] = upf

    for service, filename, mount in (
        ("free5gc-smf", "smfCfg.yaml", "smfcfg.yaml"),
        ("free5gc-nssf", "nssfCfg.yaml", "nssfcfg.yaml"),
        ("free5gc-amf", "amfCfg.yaml", "amfcfg.yaml"),
    ):
        nf = compose["services"][service]
        nf["volumes"] = [v for v in nf.get("volumes", [])
                         if not (isinstance(v, str) and (
                             f":/free5gc/config/{mount}" in v
                             or ":/free5gc/config/uerouting.yaml" in v
                         ))]
        nf["volumes"].insert(0, f"../config/slicing-demo/{filename}:/free5gc/config/{mount}:ro")

    # SMF calls ReadUERoutingConfig() even without configured ULCL paths.
    smf_service = compose["services"]["free5gc-smf"]
    smf_service["volumes"].append(
        "../config/ueRoutingCfg.yaml:/free5gc/config/uerouting.yaml:ro"
    )
    smf_service["command"] = "./smf -c ./config/smfcfg.yaml -u ./config/uerouting.yaml"
    dependencies = smf_service.get("depends_on", {})
    if isinstance(dependencies, dict):
        dependencies.pop("free5gc-upf", None)
        dependencies.update({"free5gc-upf-" + s["label"]: {"condition": "service_started"}
                             for s in SLICES})
    elif isinstance(dependencies, list):
        smf_service["depends_on"] = [d for d in dependencies if d != "free5gc-upf"] + [
            "free5gc-upf-" + s["label"] for s in SLICES
        ]
    else:
        raise ValueError("Unsupported SMF depends_on format")

    privnet = copy.deepcopy(required(compose, "networks", "privnet"))
    privnet.setdefault("ipam", {})["config"] = [{"subnet": str(net)}]
    privnet.setdefault("driver_opts", {})["com.docker.network.bridge.name"] = bridge
    compose["networks"] = {"privnet": privnet}
    for nf in compose["services"].values():
        name = nf.get("container_name")
        if name and not name.startswith("slice-"):
            nf["container_name"] = "slice-" + name
        network = nf.get("networks", {}).get("privnet", {})
        if isinstance(network, dict) and network.get("ipv4_address"):
            old = ipaddress.ip_address(network["ipv4_address"])
            if old not in net:
                # Preserve the last octet of CI-test's original private IPv4.
                network["ipv4_address"] = str(net.network_address + int(old) % 256)
        if "depends_on" in nf:
            deps = nf["depends_on"]
            if isinstance(deps, dict):
                nf["depends_on"] = {k: v for k, v in deps.items() if k in compose["services"]}
            elif isinstance(deps, list):
                nf["depends_on"] = [k for k in deps if k in compose["services"]]
            else:
                raise ValueError("Unsupported depends_on format")
    addresses = [v.get("networks", {}).get("privnet", {}).get("ipv4_address")
                 for v in compose["services"].values()
                 if isinstance(v.get("networks", {}).get("privnet", {}), dict)]
    addresses = [ip for ip in addresses if ip]
    if len(addresses) != len(set(addresses)):
        raise ValueError(f"Duplicate private network addresses in generated Compose: {addresses}")

    out[compose_dir / "docker-compose-slicing-demo.yaml"] = compose
    return out


def write_transaction(outputs, root, overwrite):
    targets = list(outputs)
    existing = [p for p in targets if p.exists()]
    if existing and not overwrite:
        raise FileExistsError(f"Generated target(s) already exist: {existing}. Do not use --force on your working lab without a backup.")
    with tempfile.TemporaryDirectory(dir=root, prefix=".slicing-demo-staging-") as td:
        stage = Path(td)
        staged, backed_up, committed = {}, {}, []
        for i, (target, data) in enumerate(outputs.items()):
            candidate = stage / f"{i}.yaml"
            candidate.write_text(
                "# Generated free5GC slicing demonstration; not a production template.\n"
                + yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
                encoding="utf-8",
            )
            # Catch YAML serialization / schema errors before changing anything.
            read_yaml(candidate)
            staged[target] = candidate
        for i, target in enumerate(existing):
            backup = stage / f"backup-{i}.yaml"
            shutil.copy2(target, backup)
            backed_up[target] = backup
        try:
            for target in targets:
                target.parent.mkdir(parents=True, exist_ok=True)
                os.replace(staged[target], target)
                committed.append(target)
        except Exception:
            for target in reversed(committed):
                if target in backed_up:
                    os.replace(backed_up[target], target)
                else:
                    target.unlink(missing_ok=True)
            raise
    for target in targets:
        print("Wrote", target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ci-test", required=True, type=Path)
    parser.add_argument("--subnet", default="10.230.200.0/24")
    parser.add_argument("--bridge-name", default="br-f5gc-slice")
    parser.add_argument("--force", action="store_true", help="Replace generated targets only; make a backup first")
    args = parser.parse_args()
    root = args.ci_test.expanduser().resolve()
    if not root.is_dir():
        raise NotADirectoryError(root)
    net = ipaddress.ip_network(args.subnet, strict=True)
    if not isinstance(net, ipaddress.IPv4Network) or net.prefixlen != 24:
        raise ValueError("--subnet must be an IPv4 /24 subnet")
    if not args.bridge_name or len(args.bridge_name) > 15:
        raise ValueError("--bridge-name must be 1 to 15 characters")
    outputs = generate(root, net, args.bridge_name)
    write_transaction(outputs, root, args.force)
    print("\nNext: python3 scripts/validate_lab.py --ci-test", root)
    print("Then: docker compose -f composes/docker-compose-slicing-demo.yaml config --quiet")
    print("Check Docker network and bridge availability before starting the lab.")
    print("PFCP node associations do not establish slice-specific PDU session routing.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        sys.exit(f"ERROR: {exc}")
