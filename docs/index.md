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

## 2024/7/2: free5GC v3.4.2 released!

The free5GC v3.4.2 includes a Go version update to 1.21 and refactoring for OpenAPI Release 17. New features include setting static IPs for UEs and OAuth2 authentication for the webconsole, plus an ULCL example in free5gc-compose. Bug fixes and a new commit message check are also included.

[Refactor]
	- Go version bump to Go1.21
	- Refactor NFs for preparation upgrading openapi to Release17

[Features]
	- Set Static-IP for UE in webconsole 
	- Webconsole acts as AF and uses OAuth2 authentication to get OAM service from NFs
	- Add ULCL docker-compose example in [free5gc-compose](https://github.com/free5gc/free5gc-compose)

[Bugs]
	- Fix N3IWUE fails to ping when having flow rules([v1.0.1](https://github.com/free5gc/n3iwue/tree/v1.0.1))
	- Fix some bugs report from [Issues](https://github.com/free5gc/free5gc/issues) or [Forum](https://forum.free5gc.org/)

[Chore]
	- Apply [Conventional Commit Message](https://www.conventionalcommits.org/en/v1.0.0/) check in Pull Request



> [!NOTE] 
> The history of the version release can be found on the [history page](./history.md).

### Next Step(s)

![](./assets/roadmap-0524.png)

We remain committed to enhancing free5GC with new features, and we have a roadmap in place to support the following functionalities:

- SBI R17 support (Will be released in 2024 Q3 or Q4)
- release NEF
- release TNGF
- Packet Rusher CI integration
- Kubernetes deployment (quick installation)
- Time Sensitive Network (TSN)
- 5G LAN

## **Sponsors**

### ![](./assets/platinum.png){: style="height:40px;width:40px" align=left} Platinum
<div class="info-block">
<img class="info-block-img" src="./assets/members/saviah.jpeg"/>
<img class="info-block-img" src="./assets/members/cht.jpeg"/>
<img class="info-block-img" src="./assets/members/onf.png"/>
<img class="info-block-img" src="./assets/members/edge-core.png"/>
</div>

### ![](./assets/golden.png){: style="height:40px;width:40px" align=left} Gold
<div class="info-block">
<img class="info-block-img" src="./assets/members/wnc.png"/>
</div>

### ![](./assets/silver.png){: style="height:40px;width:40px" align=left} Silver
<div class="info-block">
<img class="info-block-img" src="./assets/members/estinet.png"/>
</div>

## **Hardware Sponsors**
<div class="info-block">
<img class="info-block-img" src="./assets/members/alpha.png"/>
<img class="info-block-img" src="./assets/members/Intel.png"/>
<img class="info-block-img" src="./assets/members/Advantech.png"/>
<img class="info-block-img" src="./assets/members/Transnet.png"/>
<img class="info-block-img" src="./assets/members/Moxa.png"/>
<img class="info-block-img" src="./assets/members/Accton.png"/>
</div>
