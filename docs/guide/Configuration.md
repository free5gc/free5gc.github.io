<!-- Google tag (gtag.js) --> <script async src="https://www.googletagmanager.com/gtag/js?id=G-JETJ7TJ805"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-JETJ7TJ805'); </script>

# Configuration

## SBI Configuration

There are registerIP and bindingIP design on every NF's sbi interface.

![SBI interface](https://i.imgur.com/IB0cqqP.png)

This is due to some orchestration, such as Kubernets or OpenStack, has the design of service IP mapping.

![Service IP Mapping](https://i.imgur.com/pvimSfV.png)

Use Kubernets as an example. K8S has the service type that enable users to define the service IP outside the pod. But the service IP may be different from the IP assigned inside the pod. Therefore, if we register the binding IP inside the pod to NRF, NRF cannot know which service IP outside the pod has attached. As the result, we need to separate registerIP from bindingIP in this scenario.

If you are not sure what IP you should set, just configure it as the same IP address.

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
