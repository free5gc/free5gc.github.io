# free5gc-helm

## Prerequirements

- Install

    - MicroK8s

        ```bash
        sudo snap install microk8s --classic --channel=1.28/stable
        ```

    - kubectl

        ```bash
         sudo snap install kubectl --classic
        ```

    - helm

        ```bash
        sudo snap install helm --classic
        ```

- Set `sudo` group and join

    ```bash
    sudo groupadd microk8s
    sudo usermod -aG microk8s $USER
    newgrp microk8s
    ```

- Set [`microk8s` work with local `kubectl`](https://microk8s.io/docs/working-with-kubectl)

    ```bash
    mkdir -p ~/.kube
    chmod 0700 ~/.kube
    microk8s config > ~/.kube/config
    ```

## IP Forward Configuration

> [!NOTE]
> Reference: [Calico CNI Docs](https://docs.tigera.io/calico/latest/reference/configure-cni-plugins#container-settings).

- Starting from version 1.19, MicroK8s clusters use the **Calico CNI** by default.

    - To enable IP forwarding on UPF, Calico CNI needs some necessary configurations.
    - Some CNI plugin, like Flannel, kube-ovn, allow this funtionality by default.

- Setup Calico CNI for IP forwarding:

    - Edit `/var/snap/microk8s/current/args/cni-network/cni.yaml`

        ```yaml
        ...
        kind: ConfigMap
        ...
        data:
            ...
            cni_network_config: |-
                {
                    ...
                    "plugins": [
                        {
                            "type": "calico",
                            ...
                            "kubernetes": {
                                "kubeconfig": "__KUBECONFIG_FILEPATH__"
                            },
                            # append IP forwarding settings
                            "container_settings": {
                                "allow_ip_forwarding": true
                            },
                        }
                    ]
                }
        ```

- Setup kubelet args for IP fowarding:

    - Edit `/var/snap/microk8s/current/args/kubelet`

        ```bash
        # append this arg
        --allowed-unsafe-sysctls "net.ipv4.ip_forward"
        ```

- Apply settings and restart MicroK8s

    ```bash
    # apply cni configuration
    kubectl apply -f /var/snap/microk8s/current/args/cni-network/cni.yaml
    # restart MicroK8s
    microk8s stop
    microk8s start
    ```

## Addons Enable

> [!Note]
> Reference:
>
> - [MicroK8s multus addons](https://microk8s.io/docs/addon-multus)
> - [Multus - Create Network Definitions](https://github.com/k8snetworkplumbingwg/multus-cni/blob/v3.9/docs/how-to-use.md#create-network-attachment-definition)
> - [Multus - Tell pods to use those networks via annotations](https://github.com/k8snetworkplumbingwg/multus-cni/blob/v3.9/docs/how-to-use.md#run-pod-with-network-annotation)

```bash
microk8s enable community
microk8s enable multus
microk8s enable hostpath-storage
```

## Create Persistent Volumn

- Create two storage directories:

    - One for mongo: `/home/usr/mongo` <= just an example
    - One for cert: `/home/use/cert` <= just an example

- For mongodb

    - Create an storage directory: `/home/usr/mongo` <= just an example
    - Create an YAML file: `persistent-vol-for-mongodb.yaml`

        ```yaml
        apiVersion: v1
        kind: PersistentVolume
        metadata:
          name: free5gc-pv-mongo
          labels:
            project: free5gc
        spec:
          capacity:
            storage: 8Gi
          accessModes:
          - ReadWriteOnce
          persistentVolumeReclaimPolicy: Delete
          storageClassName: microk8s-hostpath
          local:
            path: <mongo_storage_dir> # edit to your own path, like: /home/use/mongo
          nodeAffinity:
            required:
              nodeSelectorTerms:
              - matchExpressions:
                - key: kubernetes.io/hostname
                  operator: In
                  values:
                  - <work_node_name> # edit to you node name
        ```

    - Apply via `kubectl`

        ```bash
        kubectl apply -f persistent-vol-for-mongodb.yaml
        ```

- For cert

    - Create an storage directory: `/home/usr/cert` <= just an example
    - Create an YAML file: `persistent-vol-for-cert.yaml`

        ```yaml
        apiVersion: v1
        kind: PersistentVolume
        metadata:
          name: free5gc-pv-cert
          labels:
            project: free5gc
        spec:
          capacity:
            storage: 2Mi
          accessModes:
          - ReadOnlyMany
          persistentVolumeReclaimPolicy: Retain
          storageClassName: microk8s-hostpath
          local:
            path: <cert_storage_dir> # edit to your own path, like: /home/use/cert
          nodeAffinity:
            required:
              nodeSelectorTerms:
              - matchExpressions:
                - key: kubernetes.io/hostname
                  operator: In
                  values:
                  - <work-node-name> # edit to you node name
        ```

    - Apply via `kubectl`

        ```bash
        kubectl apply -f persistent-vol-for-cert.yaml
        ```

- Check it

    ```bash
    kubectl get pv
    ```

## Helm Chart

- Clone from github

    ```bash
    git clone https://github.com/free5gc/free5gc-helm.git
    ```

## Network configuration

> [!Note]
> Reference: [Toward5Gs -- Network Configuration](https://github.com/Orange-OpenSource/towards5gs-helm/tree/main/charts/free5gc#networks-configuration)

- In summary, the `value.yaml` in each configuration should be set up correctly.

    - **free5gc-helm** offered a network configuration YAML file at `free5gc-helm/charts/free5gc/value.yaml`.
    - For `N2`/`N3`/`N4`/`N6`/`N9` interfaces, the `masterIf` and other `IP` field should be modified for customized deployment.

- **(Optional)** These values could also be setup by using `helm install --set`.

    ```bash
    helm install -n free5gc free5gc-helm ./free5gc/ \
        --set global.n6network.subnetIP="x.x.x.x" \
        --set global.n6network.gatewayIP="y.y.y.y" \
        --set free5gc-upf.upf.n6if.ipAddress="z.z.z.z"
    ```

## Install Chart

- Set working namespace for free5GC

    ```bash
    kubectl create ns free5gc
    ```

- Install free5GC charts

    ```bash
    cd free5gc-helm/charts
    helm install -n free5gc free5gc-helm ./free5gc/ 
    ```

- Install UERANSIM chart

    ```bash
    cd free5gc-helm/charts
    helm install -n free5gc ueransim ./ueransim/ 
    ```

- Check installation

    - Check installed charts

        ```bash
        helm ls -A
        ```

    - Check services, pods, replicates and deployments

        ```bash
        # status at each pod is expected as "Running"
        kubectl get all -n free5gc
        ```

- Check IP forwarding is available at UPF

    ```bash
    # output should be '1'
    kubectl exec -it -n free5gc deployment/free5gc-helm-free5gc-upf-upf \
        -- cat /proc/sys/net/ipv4/ip_forward
    ```

## Test

- Add subscribers via web console

    - Access ``<external_ip>:30500`

        ![7-2](./images/7-2.png)

- Ping external network with GTP-Tunnel

    ```bash
    kubectl exec -it -n free5gc deployment/ueransim-ue \
        -- ping -I uesimtun0 8.8.8.8
    ```

    ![7-3](./images/7-3.png)
