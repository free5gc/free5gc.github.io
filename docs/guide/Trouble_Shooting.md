<!-- Google tag (gtag.js) --> <script async src="https://www.googletagmanager.com/gtag/js?id=G-JETJ7TJ805"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-JETJ7TJ805'); </script>

# Trouble Shooting

### 1. `ERROR: [SCTP] Failed to connect given AMF    N3IWF=NGAP`

This error occured when N3IWF was started before AMF finishing initialization. This error usually appears when you run the TestNon3GPP in the first time.

Rerun the test should be fine. If it still not be solved, larger the sleeping time in line 110 of `test.sh`.

### 2. TestNon3GPP

TestNon3GPP will modify the `config/amfcfg.conf`. So, if you had killed the TestNon3GPP test before it finished, you might need to copy `config/amfcfg.conf.bak` back to `config/amfcfg.conf` to let other tests pass.

`cp config/amfcfg.conf.bak config/amfcfg.conf`

### 3. DB on TLS to H2C

If you meet any problems about https or mogodb, it maybe couse our new version from v3.0.1 to v3.0.2 has change http to H2C verion. Try the command below.

`mongo --eval "db.NfProfile.drop()" free5gc`

### 4. `MQCreate() Error creating message queue: Too many open files UPF=Util` (UPF)

Remove POSIX message queues

```bash
ls /dev/mqueue/
rm /dev/mqueue/*
```

### 5. Remove gtp devices (using tools in libgtp5gnl) (UPF)
```bash
cd lib/libgtp5gnl/tools
sudo ./gtp5g-link del {Dev-Name}
```

### 6. `UPF Cli Run Error: open Gtp5g: open link: create: file exists`
```bash
sudo ip link del upfgtp
```

### 7. SMF cannot communicate with UPF / UPF cannot start after a reboot or crash

The message below shows up on the logs:

```log
[WARN][SMF][Main] Failed to setup an association with UPF[127.0.0.8], error:Request Transaction [1]: retry-out
```

Verify on the logs if you got this message:

```log
[ERRO][UPF][Main] UPF Cli Run Error: open Gtp5g: open link: create: operation not supported
```

If yes, then try to load the GTP module on the system:

```bash
modprobe gtp5g
```

If this outputs an error like this:

```log
modprobe: FATAL: Module gtp5g not found in directory /lib/modules/5.4.0-xxx-generic
```

Reinstall the GTP-U kernel module using:
```bash
cd ~
git clone -b v0.8.3 https://github.com/free5gc/gtp5g.git
cd ~/gtp5g
sudo make
sudo make install
```

Then, once running the core `run.sh` script, you should obtain the message on the logs:

```log
[INFO][SMF][Main] Received PFCP Association Setup Accepted Response from UPF[127.0.0.8]
```

and it should work as normal

After that, if it's required to reload the module, just run `modprobe gtp5g` again

**Note:** The symptoms described above may happen if the host machine updated it's kernel version recently

References: [Free5GC Forum](https://forum.free5gc.org/t/erro-upf-main-upf-cli-run-error-open-gtp5g-open-link-create-operation-not-supported/1795) and [Install Guide](./3-install-free5gc.md)

### 8. Decode HTTP/2 packet in Wireshark
    
1. Run Network Function

    Check has XXFsslkey.log

2. Edit >> Preference >> Protocols >> SSL (TLS)
    
    ![](https://i.imgur.com/dzzMib5.png)

3. Add keylog

    ![](https://i.imgur.com/gV7x5QU.png)

4. Filter http2

    ![](https://i.imgur.com/ctBIYQy.png)

### 9. Decode H2C (HTTP2 clear text without TLS)

The similar reason as NEA0 NAS message. Althrough H2C is clear text, wirshark still considers these packets as the normal TCP packets and does not decode them by HTTP2.

To see the details of H2C packets, do the following configuration.

1. Analyze → Decode As…

    ![](https://i.imgur.com/NJ2brow.png)

2. click Add button to add the decode rules

    ![](https://i.imgur.com/Ct4KLgO.png)

    Decode the packets from the TCP ports listened by each NF as HTTP2 packets.

### 10. To clear all iptables rules

If something went wrong, it's possible to reset iptables' rules back using:
```bash
sudo iptables -P INPUT ACCEPT
sudo iptables -P FORWARD ACCEPT
sudo iptables -P OUTPUT ACCEPT
sudo iptables -t nat -F
sudo iptables -t mangle -F
sudo iptables -F
sudo iptables -X
```

Then remember to read the [rules required](./5-install-ueransim.md#7-testing-ueransim-against-free5gc) by the free5GC.
