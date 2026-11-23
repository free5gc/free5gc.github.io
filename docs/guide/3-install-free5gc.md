<!-- Google tag (gtag.js) --> <script async src="https://www.googletagmanager.com/gtag/js?id=G-JETJ7TJ805"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-JETJ7TJ805'); </script>

# Installation

> [!Note]
> For quick setup, please refer to [free5GC Quick Setup](./quick-setup.md).

## A. Prerequisites

1\. Linux Kernel Version

* The UPF uses the [gtp5g kernel module](https://github.com/free5gc/gtp5g). Choose a kernel compatible with **gtp5g v0.10.3** and install its matching headers before building the module. `/lib/modules/$(uname -r)/build` must exist. Check the running kernel with:

```bash
uname -r
```

> [!Note]
> Ubuntu **26.04.1**, kernel **6.18.64-061864-generic**, unmodified **gtp5g v0.10.3**, and **MongoDB 9.0.8** passed native NF startup and UE-to-DN validation. See [Quick Setup prerequisites](./quick-setup.md#prerequisites) for the tested scope and kernel limitations. Unmodified gtp5g v0.10.3 fails to build on Ubuntu kernel **7.0.0-43-generic** because of a UDP tunnel API change.

You will not be able to run most of the tests in [Test](./4-test-free5gc.md) page unless you deploy a UPF.

2\. Golang Version

* As noted above, free5gc is built and tested with Go 1.26.2
* To check the version of Go on your system, from a command prompt:
```bash
go version
```

* If another version of Go is installed, remove the existing version and install Go 1.26.2:

```bash
# this assumes your current version of Go is in the default location:
sudo rm -rf /usr/local/go
wget https://dl.google.com/go/go1.26.2.linux-amd64.tar.gz
sudo tar -C /usr/local -zxvf go1.26.2.linux-amd64.tar.gz
```

* If Go is not installed on your system:

```bash
wget https://dl.google.com/go/go1.26.2.linux-amd64.tar.gz
sudo tar -C /usr/local -zxvf go1.26.2.linux-amd64.tar.gz
mkdir -p ~/go/{bin,pkg,src}
# The following assume that your shell is bash:
echo 'export GOPATH=$HOME/go' >> ~/.bashrc
echo 'export GOROOT=/usr/local/go' >> ~/.bashrc
echo 'export PATH=$PATH:$GOPATH/bin:$GOROOT/bin' >> ~/.bashrc
echo 'export GO111MODULE=auto' >> ~/.bashrc
source ~/.bashrc
```

* Further information and installation instructions for `golang` are available at the [official golang site](https://golang.org/doc/install).

3\. Control-plane Supporting Packages

```bash
sudo apt -y update
sudo apt -y install wget git
```

* To check whether AVX is supported by the CPU, you can use the command:
```bash
lscpu | grep avx
```
* Install MongoDB Community Edition. These commands follow the quick-setup repository selection: **MongoDB 9.0** on Ubuntu 26.04 and **MongoDB 8.2** on the other releases below. Ubuntu 26.04 support starts with MongoDB 9.0.4; the validated patch version is 9.0.8. Run the following steps in the same terminal so the selected variables remain available.
    1. Select the Ubuntu repository and import its public key
        ```bash
        case "$(lsb_release -rs)" in
            20.04)
                ubuntu_codename=focal
                mongodb_version=8.2
                mongodb_key_version=8.0
                ;;
            22.04)
                ubuntu_codename=jammy
                mongodb_version=8.2
                mongodb_key_version=8.0
                ;;
            24.04|25.04)
                ubuntu_codename=noble
                mongodb_version=8.2
                mongodb_key_version=8.0
                ;;
            26.04)
                ubuntu_codename=resolute
                mongodb_version=9.0
                mongodb_key_version=9
                ;;
            *)
                echo "Unsupported Ubuntu release" >&2
                exit 1
                ;;
        esac
        sudo apt install -y gnupg curl
        curl -fsSL "https://pgp.mongodb.com/server-${mongodb_key_version}.asc" | \
            sudo gpg -o "/usr/share/keyrings/mongodb-server-${mongodb_key_version}.gpg" --dearmor
        ```
    2. Create a list file for MongoDB
        ```bash
        echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-${mongodb_key_version}.gpg ] https://repo.mongodb.org/apt/ubuntu ${ubuntu_codename}/mongodb-org/${mongodb_version} multiverse" | sudo tee "/etc/apt/sources.list.d/mongodb-org-${mongodb_version}.list"
        ```
        - you can determine the release by running `cat /etc/lsb-release`
    3. Reload local package database & Install the MongoDB packages
        ```bash
        sudo apt update
        sudo apt install -y mongodb-org
        ```
    4. Run MongoDB Community Edition
        ```bash
        # using systemd
        sudo systemctl start mongod
        sudo systemctl status mongod
        sudo systemctl enable mongod    # optional
        # using init
        sudo service mongod start
        sudo service mongod status
        ```
* **WARNING: MongoDB 5.0+ requires a CPU with AVX support. Or downgrade your MongoDB to 4.4**
    * see [this post on MongoDB's official forum](https://www.mongodb.com/community/forums/t/mongodb-5-0-cpu-intel-g4650-compatibility/116610/2)
    * see also [docker-library/mongo#485 (comment)](https://github.com/docker-library/mongo/issues/485#issuecomment-891991814)
    * When you are using `Ubuntu 20.04` and a CPU without AVX support, you can use the `mongodb` package provided by Ubuntu. 
        ```bash
        sudo apt install mongodb # MongoDB Server v3.6.8
        ```

4\. User-plane Supporting Packages

```bash
sudo apt -y update
sudo apt -y install git gcc g++ cmake autoconf libtool pkg-config libmnl-dev libyaml-dev
```

5\. Linux Host Network Settings

By default, automatic network rule installation is disabled in the UPF configuration. You can either configure the required Linux host network rules manually or configure the UPF to install them automatically through `upfcfg.yaml`. See [UPF N6 NAT Configuration](./10-UPF-Config.md) for the available settings.

```bash
sudo sysctl -w net.ipv4.ip_forward=1
sudo iptables -t nat -A POSTROUTING -o <dn_interface> -j MASQUERADE
sudo iptables -A FORWARD -p tcp -m tcp --tcp-flags SYN,RST SYN -j TCPMSS --set-mss 1400
sudo systemctl stop ufw
sudo systemctl disable ufw # prevents the firewall from starting after a OS reboot
```

Or use `reload_host_config.sh` from free5GC
```bash
sudo ./<PATH-TO-free5GC>/reload_host_config.sh <dn_interface>
# Example
sudo ./free5gc/reload_host_config.sh enp0s3
```

**Note:** For more information regarding the reload script, please, check [this appendix section](./Appendix.md#appendix-h-using-the-reload_host_configsh-script)

## B. Install Control Plane Elements

1. Clone the free5GC repository
    * To install the current `main` branch with the dependency versions in this guide:

        ```bash
        cd ~
        git clone --recursive -b main -j `nproc` https://github.com/free5gc/free5gc.git
        cd free5gc
        ```

    * After changing free5GC revisions, synchronize submodules to the commits recorded by that revision:

        ```bash
        cd ~/free5gc
        git submodule sync --recursive
        git submodule update --init --recursive --jobs `nproc`
        ```

    * For a tagged free5GC release, use the dependency versions documented for that release. The validation described above uses the current-main dependency set.

2. Compile network function services in `free5gc`
    * To do so individually (e.g., AMF only):

        ```bash
        cd ~/free5gc
        make amf
        ```

    * To build all network functions:

        ```bash
        cd ~/free5gc
        make
        ```

## C. Install User Plane Function (UPF)

1. Verify the compatible kernel and matching headers described in [Prerequisites](#a-prerequisites):

    ```bash
    uname -r
    ```

2. Retrieve the 5G GTP-U kernel module using `git` and build it

    ```bash
    git clone -b v0.10.3 https://github.com/free5gc/gtp5g.git
    cd gtp5g
    make
    sudo make install
    ```

3. Build the UPF (you may skip this step if you built all network functions above):

    * to build using make:

        ```bash
        cd ~/free5gc
        make upf
        ```

4. Customize the UPF as desired. The UPF configuration file in `run.sh` is `free5gc/config/upfcfg.yaml`.

## D. Install WebConsole

1. Before building WebConsole, install nodejs first:

    ```bash
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
    sudo apt update
    sudo apt install -y nodejs
    sudo corepack enable # setup yarn automatically
    ```

2. Build WebConsole

    * to build using make:

        ```bash
        cd ~/free5gc
        make webconsole
        ```

    * **(Alternatively)** to build manually:

        ```bash
        cd ~/free5gc/webconsole/frontend
        yarn install
        yarn build
        rm -rf ../public
        cp -R build ../public
        cd ..
        go build -o bin/webconsole server.go
        ```

   **Note: An OS with 2GB or more of RAM is recommended. WebConsole may fail to build if available RAM is below 1GB.**
