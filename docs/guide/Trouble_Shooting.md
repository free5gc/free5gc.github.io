<!-- Google tag (gtag.js) --> <script async src="https://www.googletagmanager.com/gtag/js?id=G-JETJ7TJ805"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-JETJ7TJ805'); </script>

# Troubleshooting

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

Reinstall the GTP-U kernel module (refer to [these instructions](./3-install-free5gc.md#c-install-user-plane-function-upf))

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

### 10. Clear all iptables rules

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

Then remember to add back the [rules required](./5-install-ueransim.md#7-testing-ueransim-against-free5gc) by the free5GC.

**Note:** You may consider using the `reload_host_config.sh` script for this task (see [this appendix section](./Appendix.md#appendix-h-using-the-reload_host_configsh-script))

### 11. Fix UERANSIM's EAP-AKA' behavior

If you face issues similar to the one reported on [the forum](https://forum.free5gc.org/t/authentication-method-eap-aka-not-working/2260) or the message `SEMANTICALLY_INCORRECT_MESSAGE` when seting up UERANSIM's UE after configuring it to use EAP-AKA-PRIME as authentication method on Webconsole, check the solution below:

#### First method

Clone the nightly version from commit `85a0fbf`:

Follow the cloning instructions from [this guide page here](https://free5gc.org/guide/5-install-ueransim/#2-install-ueransim)

#### Second method

Update your UERANSIM installation with the fix:

1. Enter UERANSIM's folder (the folder where the source code is already cloned):
```bash
cd UERANSIM
```

2. Move the version of your source code to the commit where the fixes were merged:
```bash
git checkout 85a0fbf
```

3. Rebuild UERANSIM
```bash
make
```
### 12. N3IWUE fails to connect with `[ERRO][N3UE][IKE] Not Success` message

As per the instructions on [N3IWUE install guide](./n3iwue-installation.md#3-use-webconsole-to-add-ue), the parameters of the configuration file `n3ue.yaml` must match those on free5GC's database. 

If you get log messages like those below:

```bash
# on free5GC
[WARN][AMF][Gmm][amf_ue_ngap_id:RU:6,AU:8(Non3GPP)][supi:SUPI:imsi-208930000001234] NAS MAC verification failed(received: 0xc0c0d135, expected: 0x6f1f9365)
[ERRO][AMF][Gmm][amf_ue_ngap_id:RU:6,AU:8(Non3GPP)][supi:SUPI:imsi-208930000001234] NAS message is ciphered, but MAC verification failed
# on N3IWUE
[INFO][N3UE][IKE] Get EAP
[ERRO][N3UE][IKE] Not Success
^C4 packets captured
4 packets received by filter
0 packets dropped by kernel
[FATA][N3UE][Init] panic: runtime error: invalid memory address or nil pointer dereference
```

Double check if SQN matches. If not, update it on N3IWUE's side using:

```bash
nano n3iwue/config/n3ue.yaml # adjust this path if needed
```

Refer to the `Security` section on the file:

```bash
info:
    version: 1.0.1
    description: Non-3GPP UE configuration
configuration:
    N3IWFInformation:
...
    Security:
                K: b73a90cbcf3afb622dba83c58a8415df
                RAND: b120f1c1a0102a2f507dd543de68281f
                SQN: 16f3b3f71005
                AMF: 8000
                OP: b672047e003bb952dca6cb8af0e5b779
                OPC: df0c67868fa25f748b7044c6e7c245b8
```

Note that SQN is dinamically updated while N3IWUE is running, so this issue might get caused by the N3IWUE being killed during the authentication phase which may cause the value to not match (e.g. it was updated on just one side).

Once the parameters are updated, save and close the configuration file. Now N3IWUE should work correctly.

### 13. Unable to find WPA2-EAP encryption option in OpenWrt installation

According to [OpenWrt Wiki](https://openwrt.org/docs/guide-user/network/wifi/freeradius#configure_wireless_access_point), 802.1x authentication is probably missing. This is due `wpad-mini` package not having it. To solve this, install `wpad` instead:
1. Login to AP as `root` using SSH

```bash
ssh root@<IP>
# Example:
ssh root@192.168.1.1
```
**Tip:** The default IP address is 192.168.1.1, change IP in the command above if your setup requires it.
2. Update package database

```bash
opkg update
```
3. Add WPA-EAP support

**Note:** Executing the steps below will remove the support for WPA3-SAE on your AP (which may be used by other wireless networks), remember to change the affected Wi-Fi networks to WPA2-PSK

**Tip:** To add WPA3 support back, install `wpad-openssl` instead of `wpad`

A. First Method

Remove `wpad-mini` and install `wpad`
```bash
opkg remove wpad-mini
opkg install wpad
```

If the commands above fail with the messages `No packages removed.` or `[...] Cannot install package wpad.`, try the second method

B. Second Method

Remove `wpad-basic-mbedtls` and install `wpad`
```bash
opkg remove wpad-basic-mbedtls
opkg install wpad
```
4. Reboot the AP to make sure the new configuration was applied
```bash
reboot
```
References: [OpenWrt Wiki](https://openwrt.org/docs/guide-user/network/wifi/freeradius) and [OpenWrt Github Issue #3363](https://github.com/openwrt/luci/issues/3363)


### 14. Troubleshooting missing packages when trying to build TNGFUE on Ubuntu

First, remember to update packages source before installing packages
```
sudo apt update
```

To install all prerequisites in one line:
```
sudo apt install libssl-dev libdbus-1-dev libnl-3-dev libnl-genl-3-dev libnl-route-3-dev
```

**(Alternatively)** Error messages and their related packages:

* openssl/ssl.h: No such file or directory
```
sudo apt install libssl-dev
```
* dbus/dbus.h: No such file or directory
```
sudo apt install libdbus-1-dev
```
* netlink/netlink.h: No such file or directory
```
sudo apt install libnl-3-dev
```
* /usr/bin/ld: cannot find -lnl-genl-3
```
sudo apt install libnl-genl-3-dev
```
* /usr/bin/ld: cannot find -lnl-route-3
```
sudo apt install libnl-route-3-dev
```