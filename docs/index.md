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


## Latest Release (free5GC v3.4.0)

We are delighted to unveil the release of free5GC v3.4.0! In this latest version, free5GC now boasts support for [OAuth](https://oauth.net/2/) within the Service-Based Architecture (SBA), marking a significant advancement in its capabilities. Furthermore, we have diligently addressed several issues and bugs that were reported by the Open-Source community, ensuring a smoother and more reliable user experience.

### Highlights

- OAuth Support
    - NRF acts as authorization server
    - All Services in AMF, SMF, NRF, PCF, UDR, UDM, AUSF, NSSF are supported to validate/request access token
- Implicit De-registration
    - Use case: UE has registered on Old AMF and send registration request to new AMF
        - New AMF is able to get the UE context by asking the old AMF, and old AMF will do the implicit de-registration.
- Support NAS Reroute ([Issue #413](https://github.com/free5gc/free5gc/issues/413))
- Support NITZ (Network Identiy and Time Zone) in UE Configuration Update Command ([Issue #113](https://github.com/free5gc/free5gc/issues/113))
- Bugfix
    - [Issue #421](https://github.com/free5gc/free5gc/issues/421)
    - [Issue #387](https://github.com/free5gc/free5gc/issues/387)
- Release N3IWUE
    - Source code: https://github.com/free5gc/n3iwue

### Next Step(s)

We remain committed to enhancing free5GC with new features, and we have a roadmap in place to support the following functionalities:

- Online/Offline Charging (Incomming release)
- SBI R17 support (Will be released in 2024 Q3 or Q4)
- release TNGF
- Packet Rusher CI integration

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
