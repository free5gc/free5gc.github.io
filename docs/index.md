<!-- <iframe width="616" height="400" src="https://www.youtube.com/embed/SFO2z5-4zxs?list=PLeDUIabcS2_p4fjApgJHNiVpfYSzz1oJi" title="free5GC Demonstration with 5G SA gNB and UE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe> -->

<!-- Google tag (gtag.js) --> <script async src="https://www.googletagmanager.com/gtag/js?id=G-JETJ7TJ805"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-JETJ7TJ805'); </script>

## What is free5GC?
<img width="300" src="./assets/logo.png"/>

The free5GC is an open-source project for 5th generation (5G) mobile core networks. The ultimate goal of this project is to implement the 5G core network (5GC) defined in 3GPP Release 15 (R15) and beyond.

Currently, the major contributors are from National Yang Ming Chiao Tung University ([NYCU](https://en.nycu.edu.tw/){target=_blank}). Please refer to our roadmap for the features of each release.

- The source code of the latest version of free5GC can be downloaded from [here](https://github.com/free5gc/free5gc){target=_blank}.
- Follow our [LinkedIn](https://www.linkedin.com/company/free5gc/){target=_blank} page to get the news about free5GC.

> [!NOTE]
> Thank you very much for your interest in free5GC. The license of free5GC follows Apache 2.0. That is, anyone can use free5GC for commercial purposes for free.

> [!NOTE]
> Want to contribute to free5GC? Check out our [How to contribute](https://free5gc.org/guide/contribute/) page for more information.

## 2024/9/5: free5GC v3.4.3 released!
The release of free5GC v3.4.3 includes several new features, such as new network function TNGF, support for an empty SD value in SNSSAI, and the ability to disable CGF in CHF. It also features a refactored Subscriber Modal Page in the Webconsole. Additionally, several bugs have been fixed, including issues with double registration with N3IWF and unauthorized UE context releases, along with other bug fixes reported via GitHub issues and the free5GC forum.

**[Features]**

- Release TNGF ([TNGFUE Installation](./guide/TNGF/tngfue-installation.md))
- Support empty SD value (SNSSAI)
- Support disable CGF in CHF

**[Refactor]**

- Refactor Subscriber Modal Page in Webconsole

**[Bugs]**

- Fix can't registration with N3IWF twice problems
- Fix UEs can be context released by a second UE without authentication (src: [Issue](https://github.com/free5gc/free5gc/issues/580))
- Fix some bug reports from [Issues](https://github.com/free5gc/free5gc/issues) or [Forum](https://forum.free5gc.org/)

> [!NOTE]
> The history of the version release can be found on the [history page](./history.md).

### Next Step(s)

![](./assets/roadmap-0924.png)

We remain committed to enhancing free5GC with new features, and we have a roadmap in place to support the following functionalities:

- Kubernetes deployment (quick installation)
- Release NEF
- SBI R17 support (Will be released in 2024 Q3 or Q4)
- Packet Rusher CI integration
- Time Sensitive Network (TSN)
- 5G LAN
