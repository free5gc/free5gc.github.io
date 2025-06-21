# NR-DC(New Radio-Dual Connectivity)

> [!Note]
> Author: [Alonza Tu](https://www.linkedin.com/in/feng-tu/)
> Date: 2025/06/05

![DC](./DC.png)

## Introduction

Introduction for NR-DC, please refer to: [Introducing NR-DC: Dual Connectivity for Next-Gen 5G Capabilities](https://free5gc.org/blog/20250219/20250219/)

In the design document, it only concerns the core network side. For RAN and UE, there will prensent where to append the additional tunnel information but without real implementation for actual using.

## Types

In real 5G networks, the NR-DC feature can be implemented in two ways:

1. [**Static Approach**](#static-approach): Two tunnels are established when the gNB and UE's PDU session starts.
2. [**Dynamic Approach**](#dynamic-approach): After the PDU session is established, the gNB can dynamically offload QoS traffic to the secondary gNB or retrieve the traffic at any time.

## Basic Setup

Before discussing the approach methods, we have to do some modification in [SMF](https://free5gc.org/doc/Smf/design/).

In the current system, there will only be one **TUNNEL** record in `SMContext`:

```go
type SMContext struct {
    ...
    LocalULTeid uint32
    LocalDLTeid uint32
    ...
    Tunnel   *UPTunnel
    ...
}
```

To support the second tunnel creation, there are three new items in `SMContext`:

```go
type SMContext struct {
    ...
    LocalULTeid uint32
    LocalDLTeid uint32
=>  LocalULTeidForSplitPDUSession uint32
=>  LocalDLTeidForSplitPDUSession uint32
    ...
    Tunnel   *UPTunnel
=>  DCTunnel *UPTunnel
    ...
}
```

## Static Approach

In static approach, **TWO TUNNELs** will be created during PDU session established.

So, in the procedure of PDU session establishment, we need to do some modification:

According to [TS 23.502 4.3.2.2](https://www.tech-invite.com/3m23/tinv-3gpp-23-502.html), the steps 11 to 16 will be the PDU session's tunnels configuration procedure:

<!-- ```mermaid
sequenceDiagram
    participant UE
    participant Master-gNB
    participant AMF
    participant SMF
    participant UPF

    SMF->>AMF: 11. N1N2 Message Transfer
    AMF->>Master-gNB: 12. N2 PDU Session Request
    Master-gNB<<->>UE: 13. PDU Session Establishment Accept
    Master-gNB->>AMF: 14. N2 PDU Session Response
    AMF->>SMF: 15. Update SMContext Request
    SMF<<->>UPF: 16. N4 Session Modification
``` -->

![procedure](./PDUSessionEstablishmentProcedure.png)

In the general case, step 11 (N1N2 Message Transfer) contains a single UPLINK TEID and related information, allowing the gNB to determine where to forward the packet.
However, in NR-DC, the SMF should generate **TWO UPLINK TEIDs** for the two tunnels. Both are stored as `ngapType.PDUSessionResourceSetupRequestTransferIEs`: one `under ngapType.ProtocolIEIDULNGUUPTNLInformation`, and the other under `ngapType.ProtocolIEIDAdditionalULNGUUPTNLInformation`.

These informations will be encapsulated as N2 PDU Session Request by [AMF](https://free5gc.org/doc/Amf/design/) and sent to Master-gNB.

> [!Note]
> According to [TS 38.413 9.4.3.1](https://www.tech-invite.com/3m38/tinv-3gpp-38-413.html), `AdditionalULNGUUPTNLInformation` can carry the secondary UPLINK TEID for the second tunnel using.
> ![38413-9.3.4.1](./38413-9.3.4.1.png)

After receiving these two UPLINK TEIDs, if the Master-gNB is configured as turning on the DC function, it should save the first UPLINK TEID for itself using and send the additional(second) UPLINK TEID to the Secondary-gNB via Xn-interface. Once the Secondary-gNB get the UPLINK TEID, it returns its DOWNLINK TEID back to the Master-gNB.

<!-- ```mermaid
sequenceDiagram
    participant Master-gNB
    participant Secondary-gNB
    participant AMF

    AMF->>Master-gNB: 12. N2 PDU Session Request
    
    Note over Master-gNB, Secondary-gNB: Xn-interface
    Master-gNB->>Secondary-gNB: Second UPLINK TEID
    Secondary-gNB->>Master-gNB: Second DOWNLINK TEID
    Note over Master-gNB, Secondary-gNB: Xn-interface

    Master-gNB->>AMF: 14. N2 PDU Session Response
``` -->

![Xn-interface](./Xn-interface.png)

Finally, Master-gNB will encapsolate these **TWO DOWNLINK TEIDs** into the data type of `ngapType.PDUSessionResourceSetupResponseTransfer`, the first one is under `DLQosFlowPerTNLInformation` and the other is under `AdditionalDLQosFlowPerTNLInformation`. Then, these IEs will be send back to core network as N2 PDU Session Response in step 14.

> [!Note]
> Accordint to [TS 38.413 9.3.4.2](https://www.tech-invite.com/3m38/tinv-3gpp-38-413.html), `AdditionalDLQosFlowPerTNLInformation` can carry the secondary DOWNLINK TEID for the second tunnel using.
> ![38413-9.3.4.2](./38413-9.3.4.2.png)

Once SMF get **TWO DOWNLINK TEIDs** in N2 message, it will set a flag `HasNRDCSupport` as true in `SMContext` and store the addition downlink tunnel information. Then, the second tunnel, **DCTunnel** will be create in the PDU session update procedure. The tunnel's rules will be sent to UPF via step 16(N4Session Modification).

> [!Warning]
> In current implementation, the Master-gNB will process the default traffics and the Secondary-gNB will process all the specified QoS traffics which are configured through [webconsole](https://free5gc.org/guide/Webconsole/Create-Subscriber-via-webconsole/).

Finally, you can use these tunnel to transfer traffics in efficient.

## Dynamic Approach

Under development, expected to support dynamic traffic offloading in future SMF releases.

## How to use?

Please refer to our user guide: [NR-DC](https://free5gc.org/guide/9-nr-dc/)

## Code Implementation

- [SMF: feat/nr-dc(static version)](https://github.com/free5gc/smf/pull/156)
- [free5GC: feat/nr-dc(static version)](https://github.com/free5gc/free5gc/pull/674)

## Reference

- [PacketRusher](https://github.com/HewlettPackard/PacketRusher)
- [TS 23.502 Procedure for the 5G System](https://www.tech-invite.com/3m23/tinv-3gpp-23-502.html)
- [TS 37.340 E-UTRA and NR – Multi-connectivity – Overall description – Stage 2](https://www.tech-invite.com/3m37/tinv-3gpp-37-340.html)
- [TS 38.413 NG-RAN — NG interface – NG Application Protocol (NGAP)](https://www.tech-invite.com/3m38/tinv-3gpp-38-413.html)