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

## 2024/11/12: free5GC v3.4.4 released!


The release of free5GC v3.4.4 includes several new features, including default profile values in the Webconsole, a search bar for profiles and subscribers, NEF support for Traffic Influence, and NAT-T support for N3IWUE in N3IWF. The N3IWF configuration file has been refactored. Bug fixes address SMF ULCL charging issues, AMF authentication procedures, UE RAT type determination, and a UDM SUCI profile B decrypt error, along with other issues reported on GitHub and the free5GC forum.

**[Features]**

- Add Profile(default values) for create subscriber in Webconsole
- Add Webconsole Search Bar for Profiles and Subscribers
- Released NEF that supporting Traffic Influence
- N3IWF support NAT-T with N3IWUE
- Go-UPF with [v0.9.3 GTP5G Version](https://github.com/free5gc/gtp5g/tree/v0.9.3)
- SMF support SDM Subscription and Unsubscription for UE Session [#123](https://github.com/free5gc/smf/pull/123)

**[Refactor]**

- N3IWF Refactor, including the configuration file [#618](https://github.com/free5gc/free5gc/pull/618)
- SMF Refactor, using Go context to track UPF association state [#122](https://github.com/free5gc/smf/pull/122)

**[Bugs]**

- SMF ULCL Charging Bugs
- AMF authentication procedure and UE RAT type determination issues.
- UDM SUCI profile B decrypt error [#41](https://github.com/free5gc/udm/pull/41)
- Fix some bug reports from [Issues](https://github.com/free5gc/free5gc/issues) or [Forum](https://forum.free5gc.org/)

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
