# History

## 2024

### 3/28: v3.4.1

In free5GC v3.4.1, Convergent Charging on PDU Session will be fully supported!
Users will see the data usage on the webconsole after the PDU Session is created (please note that: The charging method (Online/Offline) needs to be determined during the subscription creation).

![](./assets/charging-demo.gif)

### 2/16: v3.4.0

We are delighted to unveil the release of free5GC v3.4.0! In this latest version, free5GC now boasts support for [OAuth](https://oauth.net/2/) within the Service-Based Architecture (SBA), marking a significant advancement in its capabilities. Furthermore, we have diligently addressed several issues and bugs that were reported by the Open-Source community, ensuring a smoother and more reliable user experience.

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
    - Source code: [https://github.com/free5gc/n3iwue](https://github.com/free5gc/n3iwue)