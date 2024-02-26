<!-- Google tag (gtag.js) --> <script async src="https://www.googletagmanager.com/gtag/js?id=G-JETJ7TJ805"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-JETJ7TJ805'); </script>

# Configuration

## SBI Configuration

### NF IP

There are registerIP and bindingIP design on every NF's sbi interface.

```yaml
configuration:
  sbi: # Service-based interface information
    scheme: http # the protocol for sbi (http or https)
    registerIPv4: 127.0.0.18 # IP used to register to NRF
    bindingIPv4: 127.0.0.18  # IP used to bind the service
    port: 8000 # port used to bind the service
```

This is due to some orchestration, such as Kubernetes or OpenStack, has the design of service IP mapping.

![Service IP Mapping](https://i.imgur.com/pvimSfV.png)

Use Kubernetes as an example. K8s has the service type that enable users to define the service IP outside the pod. But the service IP may be different from the IP assigned inside the pod. Therefore, if we register the binding IP inside the pod to NRF, NRF cannot know which service IP outside the pod has attached. As the result, we need to separate registerIP from bindingIP in this scenario.

If you are not sure what IP you should set, just configure it as the same IP address.

### OAuth2

- Enable OAuth2 setting in NRF config (nrfcfg.yaml):
```yaml
configuration:
  sbi: # Service-based interface information
    oauth: true
```
- Set NRF's certificate path in each NF:
```yaml
configuration:
    nrfCertPem: cert/nrf.pem # NRF Certificate
```
- For more detailed information about OAuth2 in free5GC, please refer to the [Design Document](./OAuth2/OAuth2Design.md).

## Sample configuration

We provide a sample config to connect to outer ran under `/sample/ran_attach_config/`. The architecture is as following.

![free5GC sample config](https://i.imgur.com/sCASTJY.png)

As the result, user's RAN IP must set to 192.168.0.0/24 subnet or let the routing route to this subnet.

Notice: If user wants to use the setting, aware to set 192.168.0.1 to your host as well.

## SMF Configuration

### A. Configure SMF with S-NSSAI
1. Configure NF Registration SMF S-NSSAI in `smfcfg.yaml`

![](https://i.imgur.com/Qbx3yHn.png)

### B. Configure Uplink Classifier (ULCL) information in SMF

1. Configure UE routing path in `uerouting.yaml`

![](https://i.imgur.com/jmGjIGG.png)

* DestinationIP and DestinationPort will be the packet destination.
* UPF field will be the packet datapath when it match the destination above.

***For more detail of SMF config, please refer to [here](./SMF-Config.md).***
