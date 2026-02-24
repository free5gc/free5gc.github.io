# Deploy free5GC in Minutes: The Ultimate One-Script Setup Guide

Welcome to the free5GC quick setup guide! If you are new to free5GC or just want the fastest way to get a 5G core network up and running, you are in the right place.

This guide uses our `quick-setup.sh` script to automatically install dependencies, configure your network, and build the free5GC core elements.

---

## Prerequisites

Before you begin, please ensure your system meets the following requirements:

- **CPU**: AMD or Intel CPU with **AVX** instruction set support (required for MongoDB).
- **OS**: Ubuntu 20.04, 22.04, 24.04, or 25.04.
- **Tools**: The `git` command must be installed on your system.

> [!Warning]
> **CPU AVX Support:** If your CPU does not support the AVX instruction set, the automated MongoDB installation will fail. In this case, please follow the [Manual Installation Guide](./3-install-free5gc.md) to install a compatible MongoDB version manually.

---

## Quick Setup

### Step 1. Clone the free5GC Repository

First, download the source code from our official GitHub repository. Open your terminal and run:

```bash
git clone https://github.com/free5gc/free5gc.git
cd free5gc
```

### Step 2. Find Your Network Interface Name

The setup script needs to know which network interface connects your machine to the internet. To find your interface name (such as `eth0`, `ens33`, or `enp3s0`), run:

```bash
ip a
```

*Look for the interface that has your machine's primary IP address connected to the internet.*

### Step 3. Run the Quick Setup Script

Now, run the setup script and replace `<network interface>` with the name you found in Step 2.

> [!Warning]
> **CRITICAL:** You **must** use the `source` command. Do not use `./` or `bash` or `sh` to execute the script.

```bash
# Example: source quick-setup.sh -i eth0
source quick-setup.sh -i <network interface>
```

> [!Tip]
> **Optional Parameters for Developers:**
> If you need extra development tools, you can install them by appending parameters:
>
> - **Install Golang-lint**: `source quick-setup.sh -i <interface> -l`
> - **Install Docker**: `source quick-setup.sh -i <interface> -d`
> - **Install Both Golang-lint and Docker**: `source quick-setup.sh -i <interface> -l -d`

*Note: The script might take a few minutes to download packages, configure the network, and compile the code. You can take a break while it runs!*

### Curious what the script does behind the scenes?

The script automates the tedious parts of the installation:

- Configures your network interface and enables IP forwarding (for the N6 interface).
- Installs **Golang** to compile the source code.
- Installs **MongoDB** (the database for subscriber profiles).
- Installs **GTP5G** (kernel module for the User Plane Function - UPF).
- Installs **Node.js/Yarn** to build the Webconsole frontend.
- Compiles a binary executable file for every Network Function (NF).
- Automatically updates configuration files (like AMF, SMF, UPF) with your N2 and N3 IP addresses.

---

## Running free5GC

Once the setup is complete, you need to start the Core Network and the Webconsole. **You will need two separate terminal windows for this.**

### Terminal 1: Start the Core Network

In your first terminal (inside the `free5gc` directory), start all the 5G core network functions:

```bash
./run.sh
```

*Leave this terminal open and running in the background.*

### Terminal 2: Start the Webconsole

Open a new terminal window, navigate to the Webconsole directory, and start the web interface:

```bash
cd free5gc/webconsole
./bin/webconsole
```

> **Next Step:** You can now open your web browser and access the Webconsole to create and manage subscribers. For a detailed guide on how to use it, see [Create Subscriber via Webconsole](./Webconsole/Create-Subscriber-via-webconsole.md).

---

## Testing with a Simulator

Congratulations! Your free5GC core is now successfully running.

To actually test the 5G network traffic, you will need a RAN (Radio Access Network) and UE (User Equipment) simulator. We highly recommend using the **free-ran-ue** simulator.

**Follow the simulator testing guide here**: [free-ran-ue User Guide](https://free-ran-ue.github.io/doc-user-guide/02-free-ran-ue/)

---

## Need More Control?

If you prefer to install components step-by-step or need a highly customized environment, you can skip the quick setup script and follow our [Manual Build and Install Guide](./3-install-free5gc.md).
