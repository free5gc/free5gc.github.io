# The role of VNFD and NSD in 5G Network Slicing




## Overview

Before you read this article, I highly recommend you read this blog article first:  [**How to deploy a free5GC network slice on OpenStack**](https://free5gc.org/blog/network_slice/). This blog article is written by my friend Daniel Hsieh, and in his article, he went through the entire process of how to deploy a free5GC network slice on OpenStack. He also introduces some architectures we need to know when we were deploying the free5GC network slice. However, there are still some details remaining, so in this blog article, I will explore more details and what role these components play in the overall experiment. Daniel used 8 steps to explain how to [deploy a free5GC Network Slice] .In this article, I am going to focus on VNFD and NSD, which appear in steps No.5 and No.6, these two most important concepts while we are creating the network slice. By this article, you will understand more about the 5G network slicing. 

### VNFD 

VNFD, You may have seen this word a few times in Daniel’s blog posts already, but what exactly is VNFD? Before I tell you the answer directly, there is something I want you to know first.


We know that network slicing is a technology that allows network operators to divide physical network infrastructure into multiple customized virtual network slices, and each of the slices can meet specific requirements for specific use cases.  One of the most important functions of 5G network slicing is the virtual network function (VNF). VNF is a virtualized network service running on an open computing platform. In this free5GC network slicing experiment, the VNF in our experiment is our NF in free5GC, such as UPF, NSSF, UDM... etc. When you load all your VNFs into OpenStack, it should be like this:

![vnf on OS](https://github.com/Leon777-coder/blog/assets/69491904/c36da1be-d22a-4f3a-8af1-69117fc5f04c)




So what is VNFD? What is the connection between it and VNF? VNFD's full name is Virtual Network Function Descriptor. A VNFD is a deployment template that describes a VNF in terms of deployment and operational behavior requirements. It also contains connectivity, interface, and virtualized resource requirements. The VNFD conforms to the GS NFV-SOL 001 specifications and standards specified by ETSI. The Virtual Network Function Descriptor (VNFD) file describes the instantiation parameters and operational behaviors of the VNFs. It contains KPIs and other key requirements that can be used in the process of onboarding and managing the lifecycle of a VNF. Each VNFD template has the following fields:

![VNFD TEM](https://github.com/Leon777-coder/blog/assets/69491904/ed32de18-b516-4921-bc36-43f291171230)



In the deployment of free5GC network slicing experiment, if you onboard all your VNFs successfully, then your VNFD should also be like this:



![vnfd status](https://github.com/Leon777-coder/blog/assets/69491904/bf330243-a439-4aa3-81ac-893e2e122b2e)



As you can see, every VNFD is matched with its represented VNF and its IP address, VNFD acts as a blueprint or template for VNF. Also be aware that The VNFD is a static description file, not a dynamic configuration file. The metadata description in the VNFD is not changed during the whole VNF lifecycle. Some VNF parameters described in the VNFD can be declared to be configurable during the VNF design phase, and further be configured by the VNFM during or after VNF instantiation. 



### VNFD Architecture And Details

The UML representation of the VNFD high-level structure is shown in the figure below.


![vnfd2](https://github.com/Leon777-coder/blog/assets/69491904/cb5a209f-692e-4ae8-9693-fb0622be6901)



The ETSI released a specification that defines the requirements for the structure and format of a VNFD. As you can see, this graph illustrates the high‐level structure of a VNFD. The VNFD is composed of one or many virtual deployment units (VDUs) that describe the deployment resources and operation behavior of a VNF component (VNFC). Virtual Deployment Unit(VDU) is a basic part of VNF. It is the VM that hosts the network function. They are virtual machines that host the VNF or parts of it. Each part of the VNF is a VNFC and can be deployed on one or more VDUs. Each VDU is characterized, among other elements, by the software image loaded on it and the resources needed to deploy it. That is the flavor of Nova in OpenStack, which can set Disk, Memory, CPU, etc. An NS(Network Service) might contain different VNF. A VNF might also contain different VDU. Each level puts constraints on the subsequent levels, information in a lower level does not appear in a higher level. This is a complex and flexible architecture, very beautiful, very powerful. 


The following graph shows the composition of the virtual deployment unit in a VNFD: 


![VDU](https://github.com/Leon777-coder/blog/assets/69491904/7638904f-579b-45f8-9f80-84b267d18c63)



This graph illustrates a VDU deployment view. A VDU describes mainly the virtual compute (VC), virtual storage (VS), and virtual memory (VM) resources that are necessary for deploying a VNFC, and it could be linked via connection points (CPD) to other VDUs or to external VDUs that belong to other VNFs via external CPD. Virtual links in the VNFD indicate how the VDUs are connected and via which CPD. This means that different VDUs can be connected to each other through the CPD. However, in free5GC network slicing, things might be different. For 5G's NS (network slice), since there are already many VNFs in 5G, under the 5G network slice architecture, an NS contains many VNFs, but a VNF always contains one and only VDU. We use AMF as an example, (AMF is an NF in free5GC) AMF is an important and complete function and we didn't break it into more pieces. Therefore, there are not many examples in our 5G of a VNF having many VDUs. Each VNF contains one PDU only, and the via connection points (CPD) function will no longer be used in 5G network slicing, although it is a powerful and convenient function.









### NSD

NSD is a template file, whose parameters follow the ETSI MANO specification, used by the NFV Orchestrator (NFVO) for deploying network services (as a combination of multiple VNFs). Which consists of information used by the NFV Orchestrator (NFVO) for the life cycle management of an NS. Just like VNFD, 
NSD is also a static configuration file.



An NS is a composition of Network Functions (NF) arranged as a set of functions with unspecified connectivity between them or according to one or more forwarding graphs. As the following figure shows, the description of an NS as used by the NFV Management and Orchestration (MANO) functions to deploy an NS instance includes or references the descriptors of its constituent objects:

![NSD1](https://github.com/Leon777-coder/blog/assets/69491904/5ce26407-fd11-4e58-b2b6-dc0f9c1fd31f)

As the specification mentioned in ETSI GS NFV-IFA 014 V3.3.1, an NSD references at least either one VNFD or one nested NSD, just like this graph has shown. Here is an example code if today we want to instantiate VNF1 and VNF2 in the experiment.  


```bat
tosca_definitions_version: tosca_simple_profile_for_nfv_1_0_0
imports:
  - VNFD1
  - VNFD2
topology_template:
  node_templates:
    VNF1:
      type: tosca.nodes.nfv.VNF1
      requirements:
        - virtualLink1: VL1
        - virtualLink2: VL2
    VNF2:
      type: tosca.nodes.nfv.VNF2
    VL1:
      type: tosca.nodes.nfv.VL
      properties:
      network_name: net0
      vendor: tacker
    VL2:
      type: tosca.nodes.nfv.VL
      properties:
          network_name: net_mgmt
          vendor: tacker
```

In the above NSD template, VL1 and VL2 are substituting the virtual links of VNF1. If we want to apply the NFs we have in free5GC, just import these NFs into the VNF to which they belong. 

To onboard the above NSD:


```bat
tacker nsd-create –nsd-file <nsd file> <nsd name>
```


And this is also how we can use NSD to import all the VNFs we want to create network slices, it is very easy and convenient to create free5GC network slice that we want, the step was mentioned in Dainel's blog article. 



### Deployment flavor

Please go back to the VNFD high-level structure, On the right side we can see the DnfDf, which stands for VNF deployment flavor. Deployment flavor is a very important concept in NSD and VNFD, therefore it needs to be explained separately. Since VNFD and NSD are not dynamic configuration files but static configuration files. Even static configuration file has their own advantages, however, they are irreversible and lack of flexibility. To overcome this problem, we have a concept called deployment flavor. While we are using these static configuration files, we can have different deployment flavors, therefore when we are deploying these static configuration files, we can have different ways to deploy them. For example, when we deploy them, we use the 10 MB memory, and we use 100 MB memory to deploy another one. In this example, while we are deploying our deployment parameters are different, then we can define it into deployment flavor. Deployment flavor helps NSD and VNFD to increase their flexibility as a static configuration file. Make sure it's not 100% unchangeable. We can deploy different type of Deployment_Flavor that case needs, like Deployment_Flavor#2, Deployment_Flavor#3, Deployment_Flavor#4. Therefore, we can deploy different NS and VNF for different specific needs. Add some deployment flexibility as much as possible under the limitation that they are static configuration files.

![image](https://github.com/Leon777-coder/blog/assets/69491904/ca4800c4-0248-4868-8eb1-20a4ab580730)








That's it, I hope this blog article can help you learn more about 5G network slicing, even if you go back and read this previous blog post [**How ​​to deploy free5GC network slicing on OpenStack**](https://free5gc.org/blog/network_slice/) now, I think you will have a clearer idea of ​​how the whole experiment works. Learning the theory behind the scenes will always help you further your studies.





## Reference
https://docs.openstack.org/tacker/latest/contributor/vnfd_template_description.html

https://docs.openstack.org/tacker/ocata/devref/nsd_usage_guide.html

Atoui, Wassim & Assy, Nour & Gaaloul, Walid & Grida Ben Yahia, Imen. (2020). Configurable Deployment Descriptor Model in NFV. Journal of Network and Systems Management. 28. 10.1007/s10922-020-09531-2. 

Automated Network Service Scaling in NFV: Concepts, Mechanisms and Scaling Workflow

ETSI GS NFV-IFA 011 V2.4.1

ETSI GS NFV-IFA 014 V3.3.1

## About
Greetings everyone, my name is Leon Sawada, I am a 2nd-year master's student in NYCU Wireless Internet Research and Engineering (WIRE) Laboratory. My research field is network slicing, and I will be very grateful if this blog article help you understand more about these components in network slicing. Best wishes.
