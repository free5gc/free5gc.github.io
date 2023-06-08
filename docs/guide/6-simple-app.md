# free5GC Simple Apps

In this demo we will use free5GC together with UERANSIM to exercise on some simple network applications:

- `ping` + `tcpdump`
- `wget` and `curl`

## ping + tcpdump
First start up free5GC and ueransim VMs. This requires one SSH terminal for free5gc, and two for ueransim.

Open another SSH terminal and log in into ueransim:
```
ssh 192.168.56.102 -l ubuntu
```
Use `ifconfig` to check if `uesimtun0` tunnel has been created, and use ping to check if we can `ping` through it：
```
$ ping google.com
PING google.com (172.217.27.142) 56(84) bytes of data.
64 bytes from tsa03s02-in-f14.1e100.net (172.217.27.142): icmp_seq=1 ttl=63 time=3.98 ms
64 bytes from tsa03s02-in-f14.1e100.net (172.217.27.142): icmp_seq=2 ttl=63 time=3.87 ms
64 bytes from tsa03s02-in-f14.1e100.net (172.217.27.142): icmp_seq=3 ttl=63 time=4.06 ms
^C
--- google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/mdev = 3.872/3.970/4.060/0.076 ms
```

```
$ ping -I uesimtun0 google.com
PING google.com (172.217.27.142) from 60.60.0.1 uesimtun0: 56(84) bytes of data.
64 bytes from tsa03s02-in-f14.1e100.net (172.217.27.142): icmp_seq=1 ttl=61 time=5.85 ms
64 bytes from tsa03s02-in-f14.1e100.net (172.217.27.142): icmp_seq=2 ttl=61 time=4.87 ms
64 bytes from tsa03s02-in-f14.1e100.net (172.217.27.142): icmp_seq=3 ttl=61 time=4.76 ms
^C
--- google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 4.760/5.160/5.847/0.487 ms
```

Also use `route -n` to observe if current routing table shows some routing rules regarding the two network interfaces `enp0s3` and `enp0s8`:
```
$ route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.0.2.2        0.0.0.0         UG    100    0        0 enp0s3
10.0.2.0        0.0.0.0         255.255.255.0   U     0      0        0 enp0s3
10.0.2.2        0.0.0.0         255.255.255.255 UH    100    0        0 enp0s3
192.168.56.0    0.0.0.0         255.255.255.0   U     0      0        0 enp0s8
```

The network `10.0.2.0/24` and its `enp0s3` interface are related to VirtualBox NAT network card. We can bring down this interface:
```
$ sudo ifconfig enp0s3 down
$ route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
192.168.56.0    0.0.0.0         255.255.255.0   U     0      0        0 enp0s8
```
As shown aboe we have only Host-only network `192.168.56.0/24` left. Run `ping` again:
```
$ ping 8.8.8.8
ping: connect: Network is unreachable
```

And see that it can not ping through, but runing:
```
$ ping -I uesimtun0 8.8.8.8
PING 8.8.8.8 (8.8.8.8) from 60.60.0.1 uesimtun0: 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=61 time=7.17 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=61 time=5.41 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=61 time=5.15 ms
^C
--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2005ms
rtt min/avg/max/mdev = 5.150/5.907/7.165/0.895 ms
```

shows some responses, since we ask `ping` to go through the free5GC core network. To make `ping 8.8.8.8` in addition to `ping -I uesimtun0 8.8.8.8` work, we can set the `uesimtun0` interface (IP `60.60.0.1`) as the new default gateway:
```
$ sudo ip r add default dev uesimtun0
$ route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         0.0.0.0         0.0.0.0         U     0      0        0 uesimtun0
192.168.56.0    0.0.0.0         255.255.255.0   U     0      0        0 enp0s8
```
Now traffic not for the `192.168.56.0/24` network will go to `uesimtun0`, and `ping 8.8.8.8` works this time:
```
$ ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=61 time=5.02 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=61 time=6.31 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=61 time=5.41 ms
^C
--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 5.017/5.581/6.312/0.541 ms
...
```

Note that normally we are using ueransim to simulate “terminal” UE device, not as a network device or proxy, therefore the above two routing rules suffice.

Now if we still want to run:
```
$ ping google.com
ping: google.com: Temporary failure in name resolution
```

we will get unresolved domain name. To solve this, we can modify the file `/etc/resolv.conf`:
```
sudo nano /etc/resolv.conf
```

and change the nameserver IP to `8.8.8.8`:
```
nameserver 8.8.8.8
```

After the change, we can see `ping` getting responses:
```
$ ping google.com
PING google.com (216.58.200.46) 56(84) bytes of data.
64 bytes from tsa01s08-in-f46.1e100.net (216.58.200.46): icmp_seq=1 ttl=61 time=5.19 ms
64 bytes from tsa01s08-in-f46.1e100.net (216.58.200.46): icmp_seq=2 ttl=61 time=50.4 ms
64 bytes from tsa01s08-in-f46.1e100.net (216.58.200.46): icmp_seq=3 ttl=61 time=5.66 ms
^C
--- google.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/mdev = 5.191/20.423/50.414/21.207 ms
```

We can also examine the network traffic happening underneath in the scenario above. First we open another SSH terminal into ueransim, and run the following command:
```
$ sudo tcpdump -n -i any host 60.60.0.1 or 192.168.56.101
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on any, link-type LINUX_SLL (Linux cooked v1), capture size 262144 bytes
```

then run `ping 8.8.8.8` again, wait for a couple seconds, then `Ctrl-C` to exit. We see the data packets actually going in and out `uesimtun0`.
```
$ sudo tcpdump -n -i any host 60.60.0.1 or 192.168.56.101
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on any, link-type LINUX_SLL (Linux cooked v1), capture size 262144 bytes
10:24:56.138729 IP 192.168.56.101.38412 > 192.168.56.102.38740: sctp (1) [HB REQ]
10:24:56.138783 IP 192.168.56.102.38740 > 192.168.56.101.38412: sctp (1) [HB ACK]
10:24:58.456532 IP 60.60.0.1 > 8.8.8.8: ICMP echo request, id 33, seq 1, length 64
10:24:58.457416 IP 192.168.56.102.2152 > 192.168.56.101.2152: UDP, length 100
10:24:58.462136 IP 192.168.56.101.2152 > 192.168.56.102.2152: UDP, length 92
10:24:58.462324 IP 8.8.8.8 > 60.60.0.1: ICMP echo reply, id 33, seq 1, length 64
10:24:59.458823 IP 60.60.0.1 > 8.8.8.8: ICMP echo request, id 33, seq 2, length 64
10:24:59.459031 IP 192.168.56.102.2152 > 192.168.56.101.2152: UDP, length 100
10:24:59.464214 IP 192.168.56.101.2152 > 192.168.56.102.2152: UDP, length 92
10:24:59.464396 IP 8.8.8.8 > 60.60.0.1: ICMP echo reply, id 33, seq 2, length 64
10:25:00.461293 IP 60.60.0.1 > 8.8.8.8: ICMP echo request, id 33, seq 3, length 64
10:25:00.462178 IP 192.168.56.102.2152 > 192.168.56.101.2152: UDP, length 100
10:25:00.474941 IP 192.168.56.101.2152 > 192.168.56.102.2152: UDP, length 92
10:25:00.475561 IP 8.8.8.8 > 60.60.0.1: ICMP echo reply, id 33, seq 3, length 64
10:25:01.463946 IP 60.60.0.1 > 8.8.8.8: ICMP echo request, id 33, seq 4, length 64
10:25:01.464523 IP 192.168.56.102.2152 > 192.168.56.101.2152: UDP, length 100
10:25:01.469297 IP 192.168.56.101.2152 > 192.168.56.102.2152: UDP, length 92
10:25:01.470314 IP 8.8.8.8 > 60.60.0.1: ICMP echo reply, id 33, seq 4, length 64
```

## wget

Simply look for any web page for file download on the web. For example, if we choose Golang web site as an example, we may find the URL:
```
https://golang.org/dl/go1.15.8.darwin-amd64.pkg
```
Using the same network settings is the previous exercise, just
```
wget https://golang.org/dl/go1.15.8.darwin-amd64.pkg
```
And see if you can download a Golang 1.15.8 install file.

## ptt (`ssh bbsu@ptt.cc`)

You can actually use SSH in the ueransim VM to access remote site. For example, you can SSH to a well-known terminal-based BBS site in Taiwan:
```
ssh bbsu@ppt.cc
```

## Youtube

You can also use Youtube as an example app. To achieve this goal, you can install a desktop VM with graphical UI, such as Ubuntu Desktop, and follow the same procedure to install and start up UERANSIM, then access Youtube through `uesimtun0` and free5GC.

To reduce resource consumption on your host machine, you may install Lubuntu (at [https://lubuntu.me](https://lubuntu.me)), a more light-weight Ubuntu desktop distro instead. But since viewing free5GC YouTube Channel requires quite sime CPU consumption, you may have to set at least 2 CPUs and 2048 MB memory for the VM.

Refer to videos Access Youtube on Lubuntu ([1](https://youtu.be/6jbReqUWtdI), [2](https://youtu.be/FmweZt1sNJ8), [3](https://youtu.be/KSOjPZ5Lt6Q), [4](https://youtu.be/L-in_uBV6Po) and [5](https://youtu.be/Fl2XappUUBo)).