<!-- Google tag (gtag.js) --> <script async src="https://www.googletagmanager.com/gtag/js?id=G-JETJ7TJ805"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-JETJ7TJ805'); </script>

# Creating a free5GC VM and Setting up Network

In this demo we will exercise:

- Cloning an existing VM, and install free5GC on it
- Setting up the networking for the free5GC VM

> [!TIPS]
> Refer to video [Clone VM and Change IP](https://youtu.be/6Ql8St1_NH0).

## 1. Check up an existing VM for Cloning
Launch VirtualBox, and make sure the Ubuntu VM (ubuntu) we created before can boot up, then:

- Log in into the VM using SSH from the host machine, and check if the VM has internet access
- Make sure you have done `sudo apt update` and `sudo apt upgrade` (or you can do it again)
- Shutdown the VM. You can:
  - use command `sudo shutdown -P now`, or
  - click the “Close Window” of the Ubuntu VM terminal and choose the middle option (better not force to turn off the machine power)
  - later if you just want to reboot, enter `sudo shutdown -r now`

## 2. Create a free5GC VM
First let’s clone a new VM:

- Select an existing VM (ubuntu) and click the buttons on the right: / Snapshopts / Clone.
- Name the new VM `free5gc`.
- The MAC address rule: Create new MAC addresses for all network cards.
- Choose the Link cloning option (or you can also choose to complete clone the VM if you like).

After the new VM is created:

- Start up the new free5gc VM, and use the same username and password to log in.
- In the Ubuntu terminal, issue `ping` and `ifconfig` again to make sure it has internet access, and also make note of the IP address of the Host-only network interface.
    - for example the IP could still be `192.168.56.101`, and the interface name is `enp0s8`.
- Log in into free5gc VM using SSH, and make sure all things working properly.

## 3. Change hostname

The cloned free5gc VM still has host name `ubuntu` (or the name you gave it in the original VM). Let’s rename the VM to `free5gc`. You can do this by editing the file `/etc/hostname` (using `vi` or `nano`):
```
sudo nano /etc/hostname
# or 
sudo vi /etc/hostname
```
In the file, change ubuntu into `free5gc`。If you are using nano ，you can press `Ctrl-O` to save the file, then `Ctrl-X` to exit.

Let’s also change the file `/etc/hosts` by replacing the ubuntu inside into `free5gc`:
```
sudo nano /etc/hosts
```

New content of the file `/etc/hosts` looks like this:
```
127.0.0.1 localhost
127.0.1.1 free5gc
...
```

The changes will take effect after next reboot.

## 4. Setting Static IP Address
The Host-only network interface, by default, gets its IP address through DHCP. The cloned free5gc VM seems to have trouble obtaining new IP address. We can change the host-only interface to use static IP address instead, which can save a lot of trouble later.

Here let’s fix the static IP address as `192.168.56.101`:
```
$ cd /etc/netplan
$ ls
00-installer-config.yaml
$ cat 00-installer-config.yaml
```
The original content of the file `00-installer-config.yaml` looks like:
```
# This is the network config written by 'subiquity'
network:
  ethernets:
    enp0s3:
      dhcp4: true
    enp0s8:
      dhcp4: true
  version: 2
```
meaning the VM has two network interfaces. Using `ifconfig` we know that `enp0s8` is the name of the Host-only network interface. We can edit the file:
```
sudo nano 00-installer-config.yaml
```
and change it into:
```
# This is the network config written by 'subiquity'
network:
  ethernets:
    enp0s3:
      dhcp4: true
    enp0s8:
      dhcp4: no
      addresses: [192.168.56.101/24]
  version: 2
```
First check if the new content is correct:
```
sudo netplan try
```
Press enter to exit, if successful. The apply tne new interface setting:
```
sudo netplan apply
```
Run `ifconfig` to see if the network setting has been changed correctly:
```
enp0s3: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 10.0.2.15  netmask 255.255.255.0  broadcast 10.0.2.255
        inet6 fe80::a00:27ff:fec4:254f  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:c4:25:4f  txqueuelen 1000  (Ethernet)
        RX packets 2  bytes 1180 (1.1 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 18  bytes 1894 (1.8 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

enp0s8: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.56.101  netmask 255.255.255.0  broadcast 192.168.56.255
        inet6 fe80::a00:27ff:fe7e:ada6  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:7e:ad:a6  txqueuelen 1000  (Ethernet)
        RX packets 8420  bytes 531867 (531.8 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 10887  bytes 823487 (823.4 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 6621  bytes 596035 (596.0 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 6621  bytes 596035 (596.0 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
We can also check the routing table, just to have a grasp of what is going on regarding the network setting:
```
$ route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.2.2        0.0.0.0         UG    100    0        0 enp0s3
10.0.2.0        0.0.0.0         255.255.255.0   U     0      0        0 enp0s3
10.0.2.2        0.0.0.0         255.255.255.255 UH    100    0        0 enp0s3
192.168.56.0    0.0.0.0         255.255.255.0   U     0      0        0 enp0s8
```

For the display above, we learn that the Host-only network `192.168.56.0/24` does not have internet access by itself (even though we can access it using SSH from the host machine). Internet access is through the NAT network `10.0.2.0/24`, with the gateway being `10.0.2.2` (provided by VirtualBox).
Now we can SSH into free5gc VM using `192.168.56.101`:
```
ssh 192.168.56.101 -l ubuntu
```
This is also how we interact with free5gc VM from now on.
