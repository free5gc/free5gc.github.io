# SMF Config / ULCL Config
This document explains the detail of SMF config.
Also provide some examples about conversion between config file and real userplane topology

***ULCL limitation:
The branching UPF now can't connect to the Internet. 
It only serves as a Intranet in the UPF topology.
(Please refers to the topology of example 2)***

## SBI 


| Field    | meaning                                 |
| -------- | --------------------------------------- |
| scheme   | The protocol for SBI                                        |
| registerIPv4 | IP used to register to NRF  |
| bindingIPv4 | IP used to bind the service  |
| port     | SMF bind the SBI service to this port |

## PFCP

| Field    | meaning |
| -------- | -------- |
| addr     | The IP address of N4 interface on the SMF (PFCP)     |


## Userplane Information
| Field                 | meaning                                                                            |
| --------------------- | ---------------------------------------------------------------------------------- |
| userplane_information | Includes topology and information of RAN and UPFs which are controlled by this SMF |
| up_nodes              | The node in the user plane topology. Includes gNodeB, I-UPF and A-UPF              |
|          links             |   The edge in the user plane topology                                                                                 |
| type                  | Indicate it is RAN or specific kind of  UPF                                        |
| node_id               | The PFCP IPv4 address for UPF                                                      |


***Note:  
up_resource_ip serves as default user plane IP for the UPF.  
In this version, UPF will determine its user plane IP by itself.  
So setting up_resource_ip in SMF config won't affect real config in user plane.***
# AMF Config
To understand whole PDU session config, we must take a step forward to understand the AMF config.


| Field | meaning |
| -------- | -------- |
| NGAPIPList     | The IP list of N2 interfaces on the AMF     |
| SBI | Same meaning with SMF/SBI. |


# Example 1

### SMF Config
* sbi:
    * scheme: http
    * registerIPv4: 127.0.0.2
    * bindingIPv4: 127.0.0.2
    * port: 8000
* pfcp:
    * addr: 10.200.200.1
* userplane_information:
    * up_nodes:
        * gNB1:
            * type: AN
        * UPF:
            * type: UPF
            * node_id: 10.200.200.102
    * links:
        * A: gNB1
        * B: UPF

### AMF Config
* ngapIpList:
    * 127.0.0.1
* sbi:
    * scheme: http
    * registerIPv4: 127.0.0.18
    * bindingIPv4: 127.0.0.18
    * port: 8000

### Representing Topology
![](https://i.imgur.com/J9WPF8q.png)
 


# Example 2
### SMF Config
* sbi:
    * scheme: https
    * registerIPv4: 127.0.0.2
    * bindingIPv4: 127.0.0.2
    * port: 29502
* pfcp:
    * addr: 10.200.200.1
* userplane_information:
    * up_nodes:
        * gNB1:
            * type: AN
        * BranchingUPF:
            * type: UPF
            * node_id: 10.200.200.102
        * AnchorUPF1:
            * type: UPF
            * node_id: 10.200.200.101
        * AnchorUPF2:
            * type: UPF
            * node_id: 10.200.200.103
        * links:
          * A: gNB1
            B: BranchingUPF
          * A: BranchingUPF
            B: AnchorUPF1
          * A: BranchingUPF
            B: AnchorUPF2

### AMF Config
* ngapIpList:
    * 127.0.0.1
* sbi:
    * scheme: https
    * registerIPv4: 127.0.0.18
    * bindingIPv4: 127.0.0.18
    * port: 8000

### Representing Topology
![](https://i.imgur.com/tMm2Owa.png)



