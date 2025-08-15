# NR-DC(New Radio-Dual Connectivity)

> [!Note]
>
> - Introduction for NR-DC, please refer to: [Introducing NR-DC: Dual Connectivity for Next-Gen 5G Capabilities](https://free5gc.org/blog/20250219/20250219/)
> - About Implementation details, please refer to: [NR-DC(New Radio-Dual Connectivity)](https://free5gc.org/doc/NR-DC/nr-dc/)

![DC](./NR-DC/DC.png)

## Types

In real 5G networks, the NR-DC feature can be triggered in two ways:

1. [**Static Approach**](#static-approach): Two tunnels are established when the gNB and UE's PDU session starts.
2. [**Dynamic Approach**](#dynamic-approach): After the PDU session is established, the gNB can dynamically offload QoS traffic to the secondary gNB or retrieve the traffic at any time.

## Static Approach

### Expected Behavior

- After PDU session established, there will be **TWO TUNNELs** in this PDU session:
    1. The first tunnel (handled by Master-gNB): forward the default(non-specified QoS traffic) traffic.
    2. The second tunnel (handled by Secondary-gNB): forward the specified QoS traffic configured via [webconsole](https://free5gc.org/guide/Webconsole/Create-Subscriber-via-webconsole/).

### How to trigger NR-DC?

In the PDU session establishment procedure, we need to prepare **TWO TUNNELs'** information (one is for Master-gNB, and te other is for Secondary-gNB) after step 12(N2 PDU Session Request) and encapsulate them in step 14(N2 PDU Session Response):

![procedure](./NR-DC/PDUSessionEstablishmentProcedure.png)

> [!Warning]
> You may need to do Xn-interface communication between gNBs or hardcode the informations in development environment.
> Communications include:
>
> - Master-gNB sends UPLINK Tunnel information to Secondary-gNB.
> - Master-gNB retrieve DOWNLINK TEID information from Secondary-gNB.

Here we take `buildPDUSessionResourceSetupResponseTransfer` function under free5GC's integration test as an example, this function will be called before step 14 for building the data of the response:

- For basic, no NR-DC, it only contains **FIRST_DOWNLINK_TEID** and **MASTER_GNB_IP**:

    ```go
    func buildPDUSessionResourceSetupResponseTransfer() (data ngapType.PDUSessionResourceSetupResponseTransfer) {
        var data ngapType.PDUSessionResourceSetupResponseTransfer
        // QoS Flow per TNL Information
        qosFlowPerTNLInformation := &data.QosFlowPerTNLInformation
        qosFlowPerTNLInformation.UPTransportLayerInformation.Present = ngapType.UPTransportLayerInformationPresentGTPTunnel
        // UP Transport Layer Information in QoS Flow per TNL Information
        upTransportLayerInformation := &qosFlowPerTNLInformation.UPTransportLayerInformation
        upTransportLayerInformation.Present = ngapType.UPTransportLayerInformationPresentGTPTunnel
        upTransportLayerInformation.GTPTunnel = new(ngapType.GTPTunnel)
    =>  dowlinkTeid := binary.BigEndian.AppendUint32(nil, <FIRST_DOWNLINK_TEID>)
        upTransportLayerInformation.GTPTunnel.GTPTEID.Value = dowlinkTeid
    =>  upTransportLayerInformation.GTPTunnel.TransportLayerAddress = ngapConvert.IPAddressToNgap(<MASTER_GNB_IP>, "")
        // Associated QoS Flow List in QoS Flow per TNL Information
        associatedQosFlowList := &qosFlowPerTNLInformation.AssociatedQosFlowList
        associatedQosFlowItem := ngapType.AssociatedQosFlowItem{}
        associatedQosFlowItem.QosFlowIdentifier.Value = qosId
        associatedQosFlowList.List = append(associatedQosFlowList.List, associatedQosFlowItem)
        return
    }
    ```

- For NR-DC, we need to add the **SECOND_DOWNLINK_TEID** and **SECONDARY_GNB_IP**(ignore the basic part which is same with above):

    ```go
    func buildPDUSessionResourceSetupResponseTransferWithDC() (data ngapType.PDUSessionResourceSetupResponseTransfer) {
        // QoS Flow per TNL Information
        ...
        // UP Transport Layer Information in QoS Flow per TNL Information
        ...
        // Associated QoS Flow List in QoS Flow per TNL Information
        ...
        // DC QoS Flow per TNL Information
        DCQosFlowPerTNLInformationItem := ngapType.QosFlowPerTNLInformationItem{}
        DCQosFlowPerTNLInformationItem.QosFlowPerTNLInformation.UPTransportLayerInformation.Present = ngapType.UPTransportLayerInformationPresentGTPTunnel
        // DC Transport Layer Information in QoS Flow per TNL Information
        DCUpTransportLayerInformation := &DCQosFlowPerTNLInformationItem.QosFlowPerTNLInformation.UPTransportLayerInformation
        DCUpTransportLayerInformation.Present = ngapType.UPTransportLayerInformationPresentGTPTunnel
        DCUpTransportLayerInformation.GTPTunnel = new(ngapType.GTPTunnel)
    =>  DCUpTransportLayerInformation.GTPTunnel.GTPTEID.Value = aper.OctetString(<SECOND_DOWNLINK_TEID>)
    =>  DCUpTransportLayerInformation.GTPTunnel.TransportLayerAddress = ngapConvert.IPAddressToNgap(<SECONDARY_GNB_IP>, "")
        // DC Associated QoS Flow List in QoS Flow per TNL Information
        DCAssociatedQosFlowList := &DCQosFlowPerTNLInformationItem.QosFlowPerTNLInformation.AssociatedQosFlowList
        DCAssociatedQosFlowItem := ngapType.AssociatedQosFlowItem{}
        DCAssociatedQosFlowItem.QosFlowIdentifier.Value = qosId
        DCAssociatedQosFlowList.List = append(DCAssociatedQosFlowList.List, DCAssociatedQosFlowItem)
        // Additional DL QoS Flow per TNL Information
        data.AdditionalDLQosFlowPerTNLInformation = new(ngapType.QosFlowPerTNLInformationList)
        data.AdditionalDLQosFlowPerTNLInformation.List = append(data.AdditionalDLQosFlowPerTNLInformation.List, DCQosFlowPerTNLInformationItem)
        return
    }
    ```

After the response received by AMF, core network will create the **DC Tunnel** for specifed QoS traffics and update the corresponding forwarding rules in UPF via N4 session.

## Dynamic Approach

### Expected Beaviors

- When dual connectivity is not activated:

    - The specified traffic flow will be offloaded to the secondary gNB.
    - Two tunnels will exist within a single PDU session.

- When dual connectivity is being activated:

    - The second tunnel will be merged back into the master tunnel and subsequently released.
    - The PDU session will revert to a single tunnel configuration.

### How to trigger offload?

> [!Caution]
> Before initiating the offload procedure, you must first specify the desired traffic flow settings through the web console.

To illustrate how to trigger offload, we use the `buildPDUSessionResourceModifyIndicationTransferWithDC` function from free5GC's integration test as an example. This function can be invoked at any time when you wish to initiate an offload operation.

![dynamicProcedure](./NR-DC/dynamicProcedure.png)

When the master gNB decides to offload specific traffic to the secondary gNB, it should first interact with the secondary gNB via the Xn interface to obtain the second tunnel's information.

Subsequently, the master gNB encapsulates the tunnel information into a `ngapType.PDUSessionResourceModifyIndicationTransfer` structure. This data type is used to carry tunnel information and is formatted as an NGAPPDU.

```go
func buildPDUSessionResourceModifyIndicationTransferWithDC(enbaleDC bool) ngapType.PDUSessionResourceModifyIndicationTransfer {
    var data ngapType.PDUSessionResourceModifyIndicationTransfer
    // QoS Flow per TNL Information
    ···
    // UP Transport Layer Information in QoS Flow per TNL Information
    ···
    // Associated QoS Flow List in QoS Flow per TNL Information
    ···
=>  if enableDC {
        // DC QoS Flow per TNL Information
        DCQosFlowPerTNLInformationItem := ngapType.QosFlowPerTNLInformationItem{}
        DCQosFlowPerTNLInformationItem.QosFlowPerTNLInformation.UPTransportLayerInformation.Present = ngapType.UPTransportLayerInformationPresentGTPTunnel
        // DC Transport Layer Information in QoS Flow per TNL Information
        DCUpTransportLayerInformation := &DCQosFlowPerTNLInformationItem.QosFlowPerTNLInformation.UPTransportLayerInformation
        DCUpTransportLayerInformation.Present = ngapType.UPTransportLayerInformationPresentGTPTunnel
        DCUpTransportLayerInformation.GTPTunnel = new(ngapType.GTPTunnel)
        DCUpTransportLayerInformation.GTPTunnel.GTPTEID.Value = aper.OctetString(<SECOND_DOWNLINK_TEID>)
        DCUpTransportLayerInformation.GTPTunnel.TransportLayerAddress = ngapConvert.IPAddressToNgap(<SECONDARY_GNB_IP>, "")
        // DC Associated QoS Flow List in QoS Flow per TNL Information
        DCAssociatedQosFlowList := &DCQosFlowPerTNLInformationItem.QosFlowPerTNLInformation.AssociatedQosFlowList
        DCAssociatedQosFlowItem := ngapType.AssociatedQosFlowItem{}
        DCAssociatedQosFlowItem.QosFlowIdentifier.Value = qosId
        DCAssociatedQosFlowList.List = append(DCAssociatedQosFlowList.List, DCAssociatedQosFlowItem)
        // Additional DL QoS Flow per TNL Information
        data.AdditionalDLQosFlowPerTNLInformation = new(ngapType.QosFlowPerTNLInformationList)
        data.AdditionalDLQosFlowPerTNLInformation.List = append(data.AdditionalDLQosFlowPerTNLInformation.List, DCQosFlowPerTNLInformationItem)
    }
    return data
}
```

If the transition is from a single connection to dual connectivity, the `enableDC` parameter should be set to include the second tunnel's information. This instructs the core network to create and update the PDR/FAR in the data plane, thereby configuring the second tunnel.

Conversely, if the transition is from dual connectivity back to a single connection, the modify indication transfer message does not need to include the `enableDC` section. The core network will detect the current state and, upon parsing the transfer message, will disable the second tunnel accordingly.

Once the modify indication transfer request is accepted and successfully processed, the core network will respond with an `ngapType.PDUSessionResourceModifyConfirmTransfer` message. This message contains the modified tunnel information, including its TEID. The master gNB can then use this information to update the secondary gNB.

## Reference

- [TS 23.502 Procedure for the 5G System](https://www.tech-invite.com/3m23/tinv-3gpp-23-502.html)
- [TS 37.340 E-UTRA and NR – Multi-connectivity – Overall description – Stage 2](https://www.tech-invite.com/3m37/tinv-3gpp-37-340.html)
