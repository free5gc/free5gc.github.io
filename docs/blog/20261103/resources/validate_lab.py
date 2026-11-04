#!/usr/bin/env python3
"""Static configuration consistency audit; does not contact Docker or any NF."""
import argparse
import ipaddress
from pathlib import Path
import sys
import yaml

SLICES = (
    (1, "010203", "embb", "10.60.0.0/16", 81),
    (2, "000001", "urllc", "10.61.0.0/16", 82),
    (3, "000001", "miot", "10.62.0.0/16", 83),
)
REQUIRED_SERVICES = {
    "db", "free5gc-nrf", "free5gc-amf", "free5gc-ausf", "free5gc-nssf",
    "free5gc-pcf", "free5gc-smf", "free5gc-udm", "free5gc-udr",
} | {"free5gc-upf-" + s[2] for s in SLICES}


def read(path):
    if not path.is_file():
        raise ValueError(f"Missing file: {path}")
    with path.open(encoding="utf-8") as stream:
        data = yaml.safe_load(stream)
    require(isinstance(data, dict), f"Invalid YAML root at {path}")
    return data


def require(ok, why):
    if not ok:
        raise ValueError(why)


def ident(snssai):
    return int(snssai["sst"]), str(snssai["sd"])


def targets(compose, service):
    out = {}
    for item in service.get("volumes", []):
        if isinstance(item, str):
            fields = item.split(":")
            require(len(fields) in (2, 3), f"Invalid volume: {item}")
            source, target = fields[:2]
            require(target not in out, f"Duplicate container mount destination: {target}")
            out[target] = source
        elif isinstance(item, dict):
            target, source = item.get("target"), item.get("source")
            require(target not in out, f"Duplicate container mount destination: {target}")
            out[target] = source
        else:
            raise ValueError(f"Unsupported volume syntax {item!r}")
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ci-test", required=True, type=Path)
    args = parser.parse_args()
    root = args.ci_test.expanduser().resolve()
    cdir = root / "config" / "slicing-demo"
    cpath = root / "composes" / "docker-compose-slicing-demo.yaml"
    compose = read(cpath)
    amf = read(cdir / "amfCfg.yaml")
    nssf = read(cdir / "nssfCfg.yaml")
    smf = read(cdir / "smfCfg.yaml")
    services = compose["services"]

    required_ids = {(sst, sd) for sst, sd, _, _, _ in SLICES}
    for item in amf["configuration"]["plmnSupportList"]:
        require({ident(x) for x in item["snssaiList"]} == required_ids,
                "AMF plmnSupportList S-NSSAI mismatch")
    for item in nssf["configuration"]["supportedNssaiInPlmnList"]:
        require({ident(x) for x in item["supportedSnssaiList"]} == required_ids,
                "NSSF supportedNssaiInPlmnList mismatch")
    require({ident(x["snssai"]) for x in nssf["configuration"]["nsiList"]} == required_ids,
            "NSSF nsiList mismatch")
    sc = smf["configuration"]
    require({ident(x["sNssai"]) for x in sc["snssaiInfos"]} == required_ids,
            "SMF snssaiInfos mismatch")
    for item in sc["snssaiInfos"]:
        require([x["dnn"] for x in item["dnnInfos"]] == ["internet"],
                "Unexpected SMF DNN configuration")
    require(not sc.get("ulcl", False), "ULCL is outside this topology")
    require(set(services) == REQUIRED_SERVICES,
            f"Unexpected service set (missing={REQUIRED_SERVICES - set(services)}, extra={set(services) - REQUIRED_SERVICES})")
    require(set(compose["networks"]) == {"privnet"}, "Expected one Docker private network")
    privnet = compose["networks"]["privnet"]
    network = ipaddress.ip_network(privnet["ipam"]["config"][0]["subnet"], strict=True)
    require(network.version == 4 and network.prefixlen == 24, "Expected IPv4 /24")
    bridge = privnet.get("driver_opts", {}).get("com.docker.network.bridge.name", "")
    require(0 < len(bridge) <= 15 and bridge != "br-free5gc", "Unexpected bridge name")
    require((root / "config" / "ueRoutingCfg.yaml").is_file(),
            "Missing SMF UE routing source config/ueRoutingCfg.yaml")

    upnodes = sc["userplaneInformation"]["upNodes"]
    links = sc["userplaneInformation"]["links"]
    require(upnodes.get("gNB1", {}).get("type") == "AN", "Missing conceptual gNB1 node")
    require(len(links) == 3 and {tuple(sorted(l.items())) for l in links}
            == {tuple(sorted({"A": "gNB1", "B": "UPF_" + label.upper()}.items()))
                for _, _, label, _, _ in SLICES}, "Unexpected SMF user-plane links")
    require(len(upnodes) == 4, "Unexpected extra SMF user-plane nodes")

    for sst, sd, label, pool, host in SLICES:
        fqdn = f"upf-{label}.free5gc.org"
        key = "UPF_" + label.upper()
        node = upnodes[key]
        require(node.get("nodeID") == fqdn and node.get("addr") == fqdn,
                f"SMF UPF node/addr mismatch for {label}")
        infos = node["sNssaiUpfInfos"]
        require(len(infos) == 1 and ident(infos[0]["sNssai"]) == (sst, sd),
                f"SMF UPF slice mismatch for {label}")
        dnninfos = infos[0]["dnnUpfInfoList"]
        require(len(dnninfos) == 1 and dnninfos[0]["dnn"] == "internet",
                f"SMF UPF DNN mismatch for {label}")
        require(dnninfos[0]["pools"] == [{"cidr": pool}], f"SMF IP pool mismatch for {label}")
        require(node["interfaces"][0]["interfaceType"] == "N3"
                and fqdn in node["interfaces"][0]["endpoints"],
                f"SMF N3 interface mismatch for {label}")
        upf = read(cdir / f"upf-{label}.yaml")
        require(upf["pfcp"]["nodeID"] == fqdn and upf["pfcp"]["addr"] == fqdn,
                f"UPF PFCP FQDN mismatch for {label}")
        require(len(upf["dnnList"]) == 1 and upf["dnnList"][0]["dnn"] == "internet",
                f"Unexpected UPF DNN list for {label}")
        require(upf["dnnList"][0]["cidr"] == pool
                and upf["dnnList"][0]["natIfCIDR"] == str(network),
                f"UPF IP/NAT pool mismatch for {label}")
        require(upf["gtpu"]["ifList"] == [{"addr": fqdn, "type": "N3"}],
                f"UPF N3 interface mismatch for {label}")
        service = services[f"free5gc-upf-{label}"]
        require(fqdn in service["networks"]["privnet"]["aliases"],
                f"UPF Docker alias missing for {label}")
        require(service["networks"]["privnet"]["ipv4_address"] == str(network.network_address + host),
                f"UPF static IP mismatch for {label}")
        require(targets(compose, service).get("/free5gc/config/upfcfg.yaml")
                == f"../config/slicing-demo/upf-{label}.yaml",
                f"UPF config mount missing for {label}")

    names = [svc.get("container_name") for svc in services.values()]
    require(all(name and name.startswith("slice-") for name in names), "Container prefix mismatch")
    require(len(names) == len(set(names)), "Container name collision within demo")
    for name, service in services.items():
        for network_name in service.get("networks", {}):
            require(network_name == "privnet", f"Unexpected {name} network: {network_name}")
        for dep in (service.get("depends_on", {}) if isinstance(service.get("depends_on", {}), list)
                    else service.get("depends_on", {}).keys()):
            require(dep in services, f"Dangling depends_on: {name} -> {dep}")
        for destination, source in targets(compose, service).items():
            if isinstance(source, str) and source.startswith(("../", "./")):
                require((cpath.parent / source).exists(),
                        f"Missing bind-mount source for {name} -> {destination}: {source}")
        address = service.get("networks", {}).get("privnet", {}).get("ipv4_address")
        if address:
            require(ipaddress.ip_address(address) in network,
                    f"Service {name} fixed IP is outside demo subnet")
    fixed = [v.get("networks", {}).get("privnet", {}).get("ipv4_address")
             for v in services.values()]
    fixed = [x for x in fixed if x]
    require(len(fixed) == len(set(fixed)), "Duplicated fixed IP addresses")

    mounted = {
        "free5gc-smf": ("/free5gc/config/smfcfg.yaml", "../config/slicing-demo/smfCfg.yaml"),
        "free5gc-amf": ("/free5gc/config/amfcfg.yaml", "../config/slicing-demo/amfCfg.yaml"),
        "free5gc-nssf": ("/free5gc/config/nssfcfg.yaml", "../config/slicing-demo/nssfCfg.yaml"),
    }
    for name, (destination, source) in mounted.items():
        require(targets(compose, services[name]).get(destination) == source,
                f"Incorrect demo configuration mount for {name}")
    smf_service = services["free5gc-smf"]
    require(targets(compose, smf_service).get("/free5gc/config/uerouting.yaml")
            == "../config/ueRoutingCfg.yaml", "SMF UE routing bind mount is missing")
    command = smf_service.get("command", "")
    if isinstance(command, list):
        command = " ".join(command)
    require("-c ./config/smfcfg.yaml" in command
            and "-u ./config/uerouting.yaml" in command,
            "SMF command does not load both required config files")
    expected_deps = {"free5gc-upf-" + s[2] for s in SLICES}
    deps = smf_service.get("depends_on", {})
    require(expected_deps.issubset(deps), "SMF does not depend on all three UPFs")

    print("PASS: AMF/NSSF/SMF S-NSSAIs, UPF mapping, Compose mounts, N4 endpoints, IP pools, and dependencies are statically consistent.")
    print("SCOPE: YAML/file checks only; Docker startup, PFCP association, NAS and user-plane traffic require separate runtime evidence.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        sys.exit("FAIL: " + str(exc))
