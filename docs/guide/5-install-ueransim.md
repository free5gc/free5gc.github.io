<!-- Google tag (gtag.js) --> <script async src="https://www.googletagmanager.com/gtag/js?id=G-JETJ7TJ805"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-JETJ7TJ805'); </script>

# Installing UERANSIM - a UE/RAN Simulator

In this demo we will practice:

- Installing UERANSIM
- Configuring free5GC and UERANSIM
- Running UERANSIM against free5GC

## 1. Install ueramsim VM

Repeat the steps of cloning `free5gc` VM from the base VM, create a new VM for the UERANSIM simulator:

- Name the VM `ueransim`, and create new MAC addresses for all network cards.
- Make sure the VM has internet access and can log in using SSH.
- Change the hostname to `ueransim`.
- Make the Host-only network interface have static IP address `192.168.56.102`.
- Reboot the ueransim VM, as well as the free5gc VM.
- You can ping `192.168.56.101` from the ueransim VM, and also `ping 192.168.56.102` from the free5gc VM.

## 2. Install UERANSIM

Search “ueransim” on the web, and get the [web site](https://github.com/aligungr/UERANSIM).
On the web site, check what the UERANSIM open-source project is about. Then navigate to the [installation page](https://github.com/aligungr/UERANSIM/wiki/Installation) or follow the instructions below.

To download UERANSIM:
```bash
cd ~
git clone https://github.com/aligungr/UERANSIM
cd UERANSIM
# if using free5GC v3.3.0 or below
git checkout 3a96298
# if using free5GC v3.4.0 or above
git checkout e4c492d
# if using free5GC v3.4.x and to get EAP-AKA-PRIME fix
git checkout 85a0fbf
```

Update and upgrade UERANSIM VM first:
```bash
sudo apt update
sudo apt upgrade
```

Install required tools:
```bash
sudo apt install make
sudo apt install g++
sudo apt install libsctp-dev lksctp-tools
sudo apt install iproute2
sudo snap install cmake --classic
```

Build UERANSIM:
```bash
cd ~/UERANSIM
make
```

## 3. Install free5GC WebConsole
free5GC provides a simple web tool WebConsole to help creating and managing UE registrations to be used by various 5G network functions (NF). 

If WebConsole isn't installed yet, please, SSH into free5gc's VM (`192.168.56.101`) and follow the [instructions contained on this section here](./3-install-free5gc.md#d-install-webconsole).


## 4. Use WebConsole to Add an UE

First start up the WebConsole server:
```bash
cd ~/free5gc/webconsole
./bin/webconsole
```

The screen shows the port number `:5000` at the end. Open your web browser from your host machine, and enter the URL `http://192.168.56.101:5000`

- On the login page, enter username `admin` and password `free5gc`.
- Once logged in, widen the page until you see “Subscribers” on the left-hand side column.
- Click on the `Subscribers` tab and then on the `New Subscriber` button
    - Scroll down to `Operator Code Type` and change it from "OPc" to "OP".
    - Leave the other fields unchanged. This registration data is used for ease of testing and actual use later.
    - Scroll all the way down and click on `Submit`.
- Once the data shows up on the "Subscribers" table, you can press `Ctrl-C` on the terminal to kill the WebConsole process on the free5gc VM
- You can view more tutorials through this [link](./Webconsole/Create-Subscriber-via-webconsole.md). 
>[!NOTE]
>
>You have to make sure that the parameters on the webconsole are consistent with the UE.

## 5. Setting free5GC and UERANSIM Parameters

In free5gc VM, we need to edit three files:

- `~/free5gc/config/amfcfg.yaml`
- `~/free5gc/config/smfcfg.yaml`
- `~/free5gc/config/upfcfg.yaml`

First SSH into free5gc VM, and change `~/free5gc/config/amfcfg.yaml`:
```bash
cd ~/free5gc
nano config/amfcfg.yaml
```

Replace ngapIpList IP from `127.0.0.1` to `192.168.56.101`, namely from:
```yaml
...
  ngapIpList:  # the IP list of N2 interfaces on this AMF
  - 127.0.0.1
```
into:
```yaml
...
  ngapIpList:  # the IP list of N2 interfaces on this AMF
  - 192.168.56.101  # 127.0.0.1
```

Next edit `~/free5gc/config/smfcfg.yaml`:
```bash
nano config/smfcfg.yaml
```
and in the entry inside `userplaneInformation / upNodes / UPF / interfaces / endpoints`, change the IP from `127.0.0.8` to `192.168.56.101`, namely from:
```yaml
...
  interfaces: # Interface list for this UPF
   - interfaceType: N3 # the type of the interface (N3 or N9)
     endpoints: # the IP address of this N3/N9 interface on this UPF
       - 127.0.0.8
```
into:
```yaml
...
  interfaces: # Interface list for this UPF
   - interfaceType: N3 # the type of the interface (N3 or N9)
     endpoints: # the IP address of this N3/N9 interface on this UPF
       - 192.168.56.101  # 127.0.0.8
```
Finally, edit `~/free5gc/config/upfcfg.yaml`，and chage gtpu IP from `127.0.0.8` into `192.168.56.101`, namely from:
```yaml
...
  gtpu:
    forwarder: gtp5g
    # The IP list of the N3/N9 interfaces on this UPF
    # If there are multiple connection, set addr to 0.0.0.0 or list all the addresses
    ifList:
      - addr: 127.0.0.8
        type: N3
```
into:
```yaml
...
  gtpu:
    forwarder: gtp5g
    # The IP list of the N3/N9 interfaces on this UPF
    # If there are multiple connection, set addr to 0.0.0.0 or list all the addresses
    ifList:
      - addr: 192.168.56.101  # 127.0.0.8
        type: N3
```

## 6. Setting UERANSIM
In the ueransim VM, there are two files related to free5GC：

- `~/UERANSIM/config/free5gc-gnb.yaml`
- `~/UERANSIM/config/free5gc-ue.yaml`

The second file is for UE, which we don’t have to change if the data inside is consistent with the (default) registration data we set using WebConsole previously.

First SSH into ueransim, and edit the file `~/UERANSIM/config/free5gc-gnb.yaml`, and change the ngapIp IP, as well as the gtpIp IP, from `127.0.0.1` to `192.168.56.102`，and also change the IP in amfConfigs into `192.168.56.101`, that is, from:
```yaml
...
  ngapIp: 127.0.0.1   # gNB's local IP address for N2 Interface (Usually same with local IP)
  gtpIp: 127.0.0.1    # gNB's local IP address for N3 Interface (Usually same with local IP)

  # List of AMF address information
  amfConfigs:
    - address: 127.0.0.1
```
into:
```yaml
...
  ngapIp: 192.168.56.102  # 127.0.0.1   # gNB's local IP address for N2 Interface (Usually same with local IP)
  gtpIp: 192.168.56.102  # 127.0.0.1    # gNB's local IP address for N3 Interface (Usually same with local IP)

  # List of AMF address information
  amfConfigs:
    - address: 192.168.56.101  # 127.0.0.1
```
Next we examine the file `~/UERANSIM/config/free5gc-ue.yaml`，and see if the settings is consistent with those in free5GC (via WebConsole), for example:
```yaml
# IMSI number of the UE. IMSI = [MCC|MNC|MSISDN] (In total 15 or 16 digits)
supi: 'imsi-208930000000003'
# Mobile Country Code value
mcc: '208'
# Mobile Network Code value (2 or 3 digits)
mnc: '93'

# Permanent subscription key
key: '8baf473f2f8fd09487cccbd7097c6862'
# Operator code (OP or OPC) of the UE
op: '8e27b6af0e692e750f32667a3b14605d'
# This value specifies the OP type and it can be either 'OP' or 'OPC'
opType: 'OP'

...

# Initial PDU sessions to be established
sessions:
  - type: 'IPv4'
    apn: 'internet'
    slice:
      sst: 0x01
      sd: 0x010203

# List of requested S-NSSAIs by this UE
slices:
  - sst: 0x01
    sd: 0x010203

...
```
The data appear to be the same as what we set in WebConsole.

## 7. Testing UERANSIM against free5GC

SSH into free5gc. If you have rebooted free5gc, remember to run:
```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o <dn_interface> -j MASQUERADE
sudo systemctl stop ufw
```

**Note:** In Ubuntu Server 20.04 and 22.04 the dn_interface may be called `enp0s3` or `enp0s4` by default. Use the command `ip a` to help to figure it out

In addition, execute the following command:
```bash
sudo iptables -I FORWARD 1 -j ACCEPT
```

**Tip:** As per the information on the [appendix page](./Appendix.md#appendix-h-using-the-reload_host_configsh-script), it's possible to use a script to reload the config above automatically after reboot

Also, make sure you have make proper changes to the free5GC configuration files, then run `./run.sh`:
```bash
cd ~/free5gc
./run.sh
```

At this time free5GC has been started.

Next, prepare three additional SSH terminals from your host machine (if you know how to use `tmux`, you can use just one).

In terminal 1: SSH into ueransim, make sure UERANSIM is built, and configuration files have been changed correctly, then execute `nr-gnb`:
```bash
cd ~/UERANSIM
build/nr-gnb -c config/free5gc-gnb.yaml
```

In terminal 2, SSH into ueransim, and execute `nr-ue` with admin right:
```bash
cd ~/UERANSIM
sudo build/nr-ue -c config/free5gc-ue.yaml # for multiple-UEs, use -n and -t for number and delay
```

In terminal 3, SSH into ueransim, and ping `192.168.56.101` to see free5gc is alive. Then, use ifconfig to see if the tunnel `uesimtun0` has been created (by nr-ue):
```bash
ifconfig

enp0s3: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.0.2.15  netmask 255.255.255.0  broadcast 10.0.2.255
        inet6 fe80::a00:27ff:fe65:1472  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:65:14:72  txqueuelen 1000  (Ethernet)
        RX packets 80  bytes 32423 (32.4 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 90  bytes 12860 (12.8 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

enp0s8: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.56.102  netmask 255.255.255.0  broadcast 192.168.56.255
        inet6 fe80::a00:27ff:fe5e:be64  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:5e:be:64  txqueuelen 1000  (Ethernet)
        RX packets 1515  bytes 130490 (130.4 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 1010  bytes 206670 (206.6 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 3445  bytes 174416 (174.4 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 3445  bytes 174416 (174.4 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

uesimtun0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1500
        inet 60.60.0.1  netmask 255.255.255.255  destination 60.60.0.1
        inet6 fe80::2034:d00:a76:84b7  prefixlen 64  scopeid 0x20<link>
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 500  (UNSPEC)
        RX packets 3  bytes 252 (252.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 13  bytes 732 (732.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

Now use `ping`:
```bash
ping -I uesimtun0 google.com
```
If `ping` gets replies, then free5GC is running properly. Congratulations!

## 8. Testing UERANSIM deregister via nr-cli

Create new terminal, use nr-cli to show the running device
```bash
./build/nr-cli --dump
UERANSIM-gnb-208-93-1
imsi-208930000000001
```

Control `imsi-208930000000001` to send dereg normal to the free5GC
```bash
sudo ./build/nr-cli imsi-208930000000001 --exec "deregister normal"
```
And you would see the De-registration signal/logs in UE:
```bash
[2024-05-21 08:01:57.175] [nas] [debug] De-registration required due to [NORMAL]
[2024-05-21 08:01:57.185] [nas] [debug] Starting de-registration procedure due to [NORMAL]
[2024-05-21 08:01:57.185] [nas] [debug] Performing local release of PDU session[1]
[2024-05-21 08:01:57.185] [nas] [debug] Performing local release of PDU session[2]
[2024-05-21 08:01:57.185] [nas] [info] UE switches to state [MM-DEREGISTER-INITIATED]
```
