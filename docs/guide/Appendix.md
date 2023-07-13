<!-- Google tag (gtag.js) --> <script async src="https://www.googletagmanager.com/gtag/js?id=G-JETJ7TJ805"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-JETJ7TJ805'); </script>

# Appendix
## Appendix A: OAM 
1. Run the OAM server
```
cd webconsole
go run server.go
```
2. Access the OAM by
```
URL: http://localhost:5000
Username: admin
Password: free5gc
```
3. Now you can see the information of currently registered UEs (e.g. Supi, connected state, etc.) in the core network at the tab "DASHBOARD" of free5GC webconsole

**Note: You can add the subscribers here too**

## Appendix B: Orchestrator
Please refer to [free5gmano](https://github.com/free5gmano)

## Appendix C: IPTV
Please refer to [free5GC/IPTV](https://github.com/free5gc/IPTV)

## Appendix D: System Environment Cleaning
The below commands may be helpful for development purposes.

1. Remove POSIX message queues
    - ```ls /dev/mqueue/```
    - ```rm /dev/mqueue/*```
2. Remove gtp5g tunnels (using tools in libgtp5gnl)
    - ```cd ./src/upf/lib/libgtp5gnl/tools```
    - ```./gtp5g-tunnel list pdr```
    - ```./gtp5g-tunnel list far```
3. Remove gtp5g devices (using tools in libgtp5gnl)
    - ```cd ./src/upf/lib/libgtp5gnl/tools```
    - ```sudo ./gtp5g-link del {Dev-Name}```

## Appendix E: Change Kernel Version
1. Check the previous kernel version: `uname -r`
2. Search specific kernel version and install, take `5.0.0-23-generic` for example
```bash
sudo apt search 'linux-image-5.0.0-23-generic'
sudo apt install 'linux-image-5.0.0-23-generic'
sudo apt install 'linux-headers-5.0.0-23-generic'
```
3. Update initramfs and grub
```bash
sudo update-initramfs -u -k all
sudo update-grub
```
4. Reboot, enter grub and choose kernel version `5.0.0-23-generic`
```bash
sudo reboot
```
#### Optional: Remove Kernel Image
```
sudo apt remove 'linux-image-5.0.0-23-generic'
sudo apt remove 'linux-headers-5.0.0-23-generic'
```

## Appendix F: Program the SIM Card
Install packages:
```bash
sudo apt-get install pcscd pcsc-tools libccid python-dev swig python-setuptools python-pip libpcsclite-dev
sudo pip install pycrypto
```

Download PySIM
```bash
git clone git://git.osmocom.org/pysim.git
```

Change to pyscard folder and install
```bash
cd <pyscard-path>
sudo /usr/bin/python setup.py build_ext install
```

Verify your reader is ready

```bash
sudo pcsc_scan
```

Check whether your reader can read the SIM card
```bash
cd <pysim-path>
./pySim-read.py –p 0
```

Program your SIM card information
```bash
./pySim-prog.py -p 0 -x 208 -y 93 -t sysmoUSIM-SJS1 -i 208930000000003 --op=8e27b6af0e692e750f32667a3b14605d -k 8baf473f2f8fd09487cccbd7097c6862 -s 8988211000000088313 -a 23605945
```

You can get your SIM card from [**sysmocom**](http://shop.sysmocom.de/products/sysmousim-sjs1-4ff). You also need a card reader to write your SIM card. You can get a card reader from [**here**](https://24h.pchome.com.tw/prod/DCAD59-A9009N6WF) or use other similar devices.


