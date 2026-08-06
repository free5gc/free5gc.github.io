# UPF Network Configuration

The UPF can install Linux `iptables` rules for each entry in `dnnList`. This
allows the UPF to configure UE traffic forwarding, source NAT, and TCP MSS
handling in the network namespace where the UPF process is running.

This configuration can be used on a host, in a Docker container, or in a
Kubernetes Pod. The configured interface must always be visible from the UPF's
own network namespace.

## Prerequisites

Before enabling automatic rule installation, make sure that:

- `iptables` is installed in the UPF runtime environment.
- The UPF process has permission to manage network rules. Containers and Pods
  normally require the `NET_ADMIN` capability.
- IPv4 forwarding is enabled in the UPF network namespace.
- The selected egress interface exists and has an IPv4 address.

The `ipForwardEnable` option controls UPF-managed `FORWARD` rules. It does not
change the kernel `net.ipv4.ip_forward` sysctl.

## DNN Configuration

The network settings are configured under `dnnList` in `upfcfg.yaml`:

```yaml
dnnList:
  - dnn: internet
    cidr: 10.60.0.0/16
    natIfCIDR: 192.168.0.0/16
    ipForwardEnable: true
    # natifname: eth0
    # tcpMss: 1400
```

The fields have the following meanings:

| Field | Required | Description |
| --- | --- | --- |
| `dnn` | Yes | Data Network Name associated with this UE address pool. |
| `cidr` | Yes | UE address pool. It is used as the source or destination CIDR in the installed rules. |
| `natifname` | No | Exact egress interface name in the UPF network namespace. This field takes precedence over `natIfCIDR`. |
| `natIfCIDR` | No | Selects the egress interface whose assigned IPv4 address belongs to this CIDR. This is an interface-network selector, not the UE address pool. |
| `ipForwardEnable` | Yes | Installs scoped uplink and downlink `FORWARD` rules when an egress interface is selected. |
| `tcpMss` | No | TCP MSS value. Zero or omitted uses path MTU discovery; a non-zero value sets a fixed MSS. |

## Egress Interface Selection

The UPF resolves the egress interface in the following order:

1. If `natifname` is set, the UPF uses that interface and ignores
   `natIfCIDR`.
2. Otherwise, if `natIfCIDR` is set, the UPF searches for interfaces with an
   IPv4 address inside that CIDR.
3. Exactly one interface must match `natIfCIDR`. UPF startup fails if no
   interface or multiple interfaces match.
4. If neither selector is set, the UPF does not install NAT, `FORWARD`, or TCP
   MSS rules for that DNN.

Use `natifname` when the interface name is stable and known. Use `natIfCIDR`
when container or Pod interface names may vary between deployments.

For example, the following configuration always selects `eth1`, even if its
address is not in `10.100.200.0/24`:

```yaml
dnnList:
  - dnn: internet
    cidr: 10.60.0.0/16
    natifname: eth1
    natIfCIDR: 10.100.200.0/24
    ipForwardEnable: true
```

## Installed Rules

When an egress interface is selected, the UPF installs a source NAT rule:

```console
iptables -t nat -A POSTROUTING -s <ue-cidr> -o <egress-interface> -j MASQUERADE
```

This replaces the UE source address with the address of the selected egress
interface. Return traffic can then be mapped back to the UE connection.

When `ipForwardEnable` is `true`, the UPF also installs these forwarding rules:

```console
iptables -A FORWARD -s <ue-cidr> -o <egress-interface> -j ACCEPT
iptables -A FORWARD -d <ue-cidr> -i <egress-interface> \
  -m state --state RELATED,ESTABLISHED -j ACCEPT
```

The first rule permits UE uplink traffic to leave through the selected
interface. The second rule permits established return traffic to reach the UE
address pool.

The UPF also installs one TCP MSS rule. When `tcpMss` is zero or omitted, the
MSS is derived from the path MTU:

```console
iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN \
  -j TCPMSS --clamp-mss-to-pmtu
```

To force an MSS of 1400 bytes, set `tcpMss: 1400`. The resulting target is:

```console
-j TCPMSS --set-mss 1400
```

NAT is installed whenever an egress interface is selected. Setting
`ipForwardEnable` to `false` disables the UPF-managed `FORWARD` and TCP MSS
rules, but does not disable the NAT rule.

Before appending a rule, the UPF checks whether the same rule already exists.
Rules appended by the UPF are removed in reverse order during a clean
shutdown.

## Host Deployment

For a host installation, use a stable interface name and enable IPv4
forwarding:

```yaml
dnnList:
  - dnn: internet
    cidr: 10.60.0.0/16
    natifname: enp3s0
    ipForwardEnable: true
```

```console
sudo sysctl -w net.ipv4.ip_forward=1
```

Persist the sysctl according to the Linux distribution, for example in a file
under `/etc/sysctl.d/`.

## Docker Deployment

The interface name assigned by Docker can depend on the attached networks.
Selecting the interface by its network CIDR is usually more stable:

```yaml
dnnList:
  - dnn: internet
    cidr: 10.60.0.0/16
    natIfCIDR: 10.100.200.0/24
    ipForwardEnable: true
```

The UPF container requires network administration permission and IPv4
forwarding:

```yaml
services:
  upf:
    cap_add:
      - NET_ADMIN
    sysctls:
      net.ipv4.ip_forward: "1"
```

Docker may perform another source NAT operation when traffic leaves the host.
The UPF rule translates the UE address to the UPF container address; host-level
Docker networking then controls routing or NAT outside the container namespace.

## Kubernetes Deployment

In Kubernetes, `natIfCIDR` can select the primary Pod interface from the Pod
network CIDR:

```yaml
dnnList:
  - dnn: internet
    cidr: 10.60.0.0/16
    natIfCIDR: 192.168.0.0/16
    ipForwardEnable: true
```

The UPF container needs the `NET_ADMIN` capability:

```yaml
securityContext:
  capabilities:
    add:
      - NET_ADMIN
```

The CNI must also permit IP forwarding inside the Pod network namespace. When
Calico is managed by the Tigera Operator, it can be enabled with:

```console
kubectl patch installation.operator.tigera.io default \
  --type merge \
  --patch '{"spec":{"calicoNetwork":{"containerIPForwarding":"Enabled"}}}'
```

Other CNI implementations have different settings. Confirm that
`net.ipv4.ip_forward` is `1` inside the UPF Pod after applying the platform
configuration.

## Intermediate UPF

An intermediate UPF that does not provide N6 egress normally does not require
NAT. Omit both interface selectors for that DNN:

```yaml
dnnList:
  - dnn: internet
    cidr: 10.60.0.0/16
    ipForwardEnable: true
```

Without `natifname` or `natIfCIDR`, the UPF does not install the rules described
on this page.

## Verification

First verify the available interfaces and kernel forwarding state from the UPF
network namespace:

```console
ip -br addr
cat /proc/sys/net/ipv4/ip_forward
```

Inspect the installed rules:

```console
iptables -t nat -S POSTROUTING
iptables -S FORWARD
iptables -t mangle -S FORWARD
```

Use verbose counters while generating UE traffic:

```console
iptables -t nat -L POSTROUTING -n -v --line-numbers
iptables -L FORWARD -n -v --line-numbers
iptables -t mangle -L FORWARD -n -v --line-numbers
```

For Docker, run the commands with `docker exec`:

```console
docker exec -it upf iptables -t nat -L POSTROUTING -n -v --line-numbers
```

For Kubernetes, run them with `kubectl exec` from a machine that has access to
the cluster:

```console
kubectl exec -n free5gc deployment/free5gc-free5gc-upf-upf -- \
  iptables -t nat -L POSTROUTING -n -v --line-numbers
```

NAT, uplink, and downlink counters do not need to be equal. NAT is evaluated
when a new connection creates a conntrack entry, while `FORWARD` is evaluated
for every forwarded packet. A TCP MSS counter remains zero when the test sends
only ICMP traffic.

## Troubleshooting

| Symptom | Possible cause |
| --- | --- |
| The configured `natifname` is not found | The name belongs to the host namespace rather than the UPF namespace, or the runtime assigned a different name. |
| `natIfCIDR` does not match an interface | The CIDR does not contain any address assigned inside the UPF namespace. |
| `natIfCIDR` matches multiple interfaces | The selector is too broad. Use a narrower CIDR or set `natifname`. |
| Rule installation returns a permission error | The process does not have `NET_ADMIN`, or the runtime security policy blocks `iptables`. |
| `FORWARD` counters remain zero | UE packets may not be reaching this UPF, or the PFCP/GTP-U path may be incorrect. |
| Counters increase but external access fails | Check kernel forwarding, CNI or Docker egress, host firewall policy, and the upstream route. |
| TCP MSS counter remains zero during ping | This is expected because the TCPMSS target applies only to TCP SYN packets. |

If an older deployment script installs broad `MASQUERADE` or `FORWARD` rules,
remove those duplicate rules before enabling UPF-managed rules. A broad rule
placed earlier in the same chain can match traffic before the scoped rule and
make its counter remain zero.

## Related Documentation

- [free5GC Configuration](https://free5gc.org/guide/Configuration/)
- [Install free5GC](https://free5gc.org/guide/3-install-free5gc/)
- [Run free5GC with Docker Compose](https://free5gc.org/guide/0-compose/)
