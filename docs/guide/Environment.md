# Recommended Environment

free5gc has been tested against the following environment:

- Software
    - OS: Ubuntu 20.04.1
    - gcc 7.3.0
    - Go 1.14.4 linux/amd64
    - kernel version 5.4.0-42-generic

The listed kernel version is required for the UPF element.

- Minimum Hardware
    - CPU: Intel i5 processor
    - RAM: 4GB
    - Hard drive: 160GB
    - NIC: Any 1Gbps Ethernet card supported in the Linux kernel

- Recommended Hardware
    - CPU: Intel i7 processor
    - RAM: 8GB
    - Hard drive: 160GB
    - NIC: Any 10Gbps Ethernet card supported in the Linux kernel

This guide assumes that you will run all 5GC elements on a single machine.


## Hardware Tested 

Some 5G UE and gNodeB hardware have been tested with free5GC by partners or community members:
- 5G UE (Support 5G SA):
    - [APAL 5G Dongle](https://www.apaltec.com/dongle/)
    - [APAL 5G MiFi](https://www.apaltec.com/mifi/)
    - [Samsung S21 5G](https://www.samsung.com/us/smartphones/galaxy-s21-5g/)
    - Huawei P40 5G ([forum link](https://forum.free5gc.org/t/running-free5gc-stage3-with-amarisoft-gnodeb-ue/532))
    - Huawei Mate30 5G ([forum link](https://forum.free5gc.org/t/real-ue-register-failed/281))
- gNodeB:
    - Alpha gNodeB
    - Compal gNodeB
    - FII gNodeB
    - ITRI gNodeB
    - Lions gNodeB
    - Amarisoft gNodeB ([forum link](https://forum.free5gc.org/t/running-free5gc-stage3-with-amarisoft-gnodeb-ue/532))
    - Nokia gNodeB ([forum link](https://forum.free5gc.org/t/real-ue-register-failed/281))
    - Nokia (AMIA AirScale Indoor Subrack 473098A)

Welcome to report the tested hardware not listed above on Github issue or free5GC forum.

**PS:** if you don't have any hardware available, suggest to use [UERANSIM](https://github.com/aligungr/UERANSIM) to simulate.

(Refer to **Advanced environment setup** section)