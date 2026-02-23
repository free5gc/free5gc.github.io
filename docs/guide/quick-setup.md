# free5GC Single Host Mode Quick Setup

## Env Requirement

- AMD CPU
- AUX supported CPU (for mongoDB)
- Ubuntu 20.04/22.04/24.04/25.04
- `git` command

> [!Warning]
> If your CPU does not support AUX, please install manually with correct and compatible mongoDB version: [Build and Install free5GC](./3-install-free5gc.md).

## Steps

### 1. Clone free5GC

```bash
git clone https://github.com/free5gc/free5gc
```

### 2. Quick Setup Script

```bash
cd free5gc
source quick-setup.sh -i <network interface>
```

> [!Warning]
> It is required to use `source` command to run the script, not `./`.

The script supports installing other package tools via configurable parameters for development.

| Package | Args | Example |
| - | - | - |
| Golang-lint | `-l`/`--lint` | `source quick-setup.sh --lint` |
| Docker | `-d`/`--docker` | `source quick-setup.sh --docker` |

The script may a few minutes to finish setup.

### 3. Run free5GC

- Core network

```bash
./run.sh
```

- Webconsole

```bash
cd webconsole && ./bin/webconsole
```

Webconsole usage: [Webconsole](./Webconsole/Create-Subscriber-via-webconsole.md).

### 4. Test with RAN/UE simulator

Please refer to: [https://free-ran-ue.github.io/doc-user-guide/02-free-ran-ue/](https://free-ran-ue.github.io/doc-user-guide/02-free-ran-ue/).

## Script Description

The `quick-setup.sh` script will do these tasks.

- Configure the network interface, including IP forward setting (N6 interface)
- Install Golang for compiling source code
- Install MongoDB
- Install GTP5G for UPF
- Install YARN for webconsole frontend building
- Make the binary executable file for each NF
- Update N2 IP address in AMF configuration, N3 IP address in SMF/UPF configurations

## Manual Installation

Please refer to [Build and Install free5GC](./3-install-free5gc.md).
