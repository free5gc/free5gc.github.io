# User Guide

## Information

- [Hardware tested](./hardware.md)
- [Supported features](./features.md)

## Roadmap

Here are the features in the roadmap, these item is planned to be supported in the near future:

* Charging Function (CHF)
* Network Exposure Function (NEF)

## free5GC Installation Guide
For people who are not familiar with virtual machines and Linux installation, here are some example demonstrations:

- [Creating a Ubuntu VM using VirtualBox](./1-vm-en.md)
- [Creating and Configuring a free5GC VM](./2-config-vm-en.md)
- [Installing](./3-install-free5gc.md) and [Testing](./4-test-free5gc.md) free5GC Core Network
- [Installing a UE/RAN Simulator](./5-install-ueransim.md)
- [free5GC Simple Apps](./6-simple-app.md)
- All of tutorial videos are available at our Youtube Channel [EN](https://www.youtube.com/watch?v=R-9vH_6VJ2Q&list=PLeDUIabcS2_rQd3yVJrBAYb-MbcqNgjC9)/[ZH-TW](https://www.youtube.com/watch?v=lD5iYvCB4CQ&list=PLeDUIabcS2_pdhCN3sz5gFdT-mTukyX-v)
- [Environment setup of multiple SMF, DNN, and UPF](https://www.youtube.com/watch?v=AEMrjKRWarw)

## Configuration
- [Environment](./Environment.md)
- [Basic](./Configuration.md)
- [SMF](./SMF-Config.md)
- [Webconsole](./New-Subscriber-via-webconsole.md)
- [Select UPF based on S-NSSAI](https://github.com/s5uishida/free5gc_ueransim_snssai_upf_sample_config)
- [Select nearby UPF according to the connected gNodeB](https://github.com/s5uishida/free5gc_ueransim_nearby_upf_sample_config)
- [ULCL](https://github.com/s5uishida/free5gc_ueransim_ulcl_sample_config)
- [Netns5g - A free5gc and UERANSIM deployment using Linux network namespaces](https://github.com/konradkar2/netns5g)

## Deployment

For Container deployment:

- [free5GC Compose](https://github.com/free5gc/free5gc-compose) (Docker Compose)
- [Towards5gs-helm](https://github.com/Orange-OpenSource/towards5gs-helm) (Kubernetes)

## Others
- [Release Note](https://github.com/free5gc/free5gc/releases)
- [Trouble Shooting](./Trouble_Shooting.md)
- [Appendix](./Appendix.md)