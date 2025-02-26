<!-- <iframe width="616" height="400" src="https://www.youtube.com/embed/SFO2z5-4zxs?list=PLeDUIabcS2_p4fjApgJHNiVpfYSzz1oJi" title="free5GC Demonstration with 5G SA gNB and UE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe> -->

<!-- Google tag (gtag.js) --> <script async src="https://www.googletagmanager.com/gtag/js?id=G-JETJ7TJ805"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-JETJ7TJ805'); </script>

<img width="300" src="./assets/logo.png"/>

The free5GC (a Linux Foundation project) is an open-source project for 5th generation (5G) mobile core networks. The ultimate goal of this project is to implement the 5G core network (5GC) defined in 3GPP Release 15 (R15) and beyond.

Currently, the major contributors are from National Yang Ming Chiao Tung University ([NYCU](https://en.nycu.edu.tw/){target=_blank}).

- The source code of the latest version of free5GC can be downloaded from [here](https://github.com/free5gc/free5gc){target=_blank}.
- Information about TSC (Technical Steering Committee) can be found at [free5gc/governance](https://github.com/free5gc/governance/blob/main/CONTRIBUTORS.md).
- Follow our [LinkedIn](https://www.linkedin.com/company/free5gc/){target=_blank} page to get the news about free5GC.
- Please refer to our roadmap for the features of each release.

> [!NOTE]
> The Linux Foundation announced that free5GC officially joined the Linux Foundation on September 16, 2024, during the Open Source Summit Europe in Vienna, Austria. Check out the press release [here](https://www.linuxfoundation.org/press/worlds-leading-open-source-mobile-packet-core-free5gc-moves-under-linux-foundation-to-provide-open-source-alternatives-across-5g-deployments).

> [!NOTE]
> Thank you very much for your interest in free5GC. The license of free5GC follows Apache 2.0. That is, anyone can use free5GC for commercial purposes for free.

> [!NOTE]
> Please check out the [Google Scholar](https://scholar.google.com/scholar?hl=en&as_sdt=2007&q=free5gc) page here for publications using free5GC.

> [!NOTE]
> Want to contribute to free5GC? Check out our [How to contribute](https://free5gc.org/guide/contribute/) page for more information.

## 2025/02/26: free5GC v3.4.5 released!


The release v3.4.5 of free5GC fixed a series of bugs, which including:

- Online Charging feature with ULCL deployment
- [SMF #71: SM contexts collection Response not compliant to standard](https://github.com/free5gc/smf/issues/71)
- [free5GC #627: There is an error in the information listed for QoS-related parameters](https://github.com/free5gc/free5gc/issues/627)
- [free5GC #630: Regarding the PDU session release process during IDLE state](https://github.com/free5gc/free5gc/issues/630)
- free5GC Issue #617 - #620, #635 - #638

Besides, the version v3.4.5 is the final release for 3GPP R15.
We're no longer maintain the 3GPP R15 branch, any technical issue/vulnerability/feature will be added in the [3GPP R17 branch](https://github.com/free5gc/free5gc/tree/next) only.

> [!NOTE]
> The history of the version release can be found on the [history page](./history.md).

### Next Step(s)

![](./assets/roadmap-1124.png)

We remain committed to enhancing free5GC with new features, and we have a roadmap in place to support the following functionalities:

- Kubernetes deployment (quick installation)
- SBI R17 support
- Packet Rusher CI integration
- NR-DC
- Roaming
- 5G LAN
