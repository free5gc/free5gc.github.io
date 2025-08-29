# 利用 Custom eBPF-based Schedulers 改善網路效能

>[!NOTE]
> Author: [Ian Chen](https://www.linkedin.com/in/ian-chen-88b70b1aa/)
> Date: 2025/07/26
---

Linux Kernel 自 v6.12 開始支援 sched_ext，它允許使用者藉由 eBPF 程式來定義自訂的 CPU 排程器。這個功能使得開發者能夠創建更靈活和高效的排程策略，以滿足特定的性能需求。
筆者深受 scx 專案的啟發，並且參考 [scx_rustland](https://github.com/sched-ext/scx/tree/main/scheds/rust/scx_rustland) 的概念，實作了讓開發者能夠使用 golang 語言來撰寫自訂排程器的框架 [scx_goland_core](https://github.com/Gthulhu/scx_goland_core)。

## scx 與 5G 領域結合的可能性

對於 5G 與 scx 的結合，已經有些許討論 [[1]](https://free5gc.org/blog/20250305/20250305/) [[2]](https://free5gc.org/blog/20250509/20250509/) [[3]](https://lwn.net/Articles/1027096/)。然而，考慮到現代 Cloud-Native App (5G Core Network) 的特性，目前尚沒有相關案例探討 scx 如何在雲原生架構上運作。

![alt text](https://github.com/free5gc/free5gc.github.io/blob/main/docs/blog/20250726/fig1.png?raw=true)
*圖一：API 架構*

對此，筆者提出了一個初步的想法，基於 scx_goland_core 框架開發了一個可在雲原生環境中運行的自訂排程器 [Gthulhu](https://gthulhu.github.io/docs/)，它可以部署於 Kubernetes 群集中，透過部署的方式管理叢集中大量節點的排程策略。

我們可以透過 Restful API 對 Gthulhu API server 下達排程策略，讓 API server 為我們找出需要調整的 workloads。與此同時，Gthulhu 會定期向 API server 發送心跳訊息，並在必要時更新排程策略。

> 關於 Gthulhu 的詳細資訊，請參考 [Gthulhu Docs](https://gthulhu.github.io/docs/how-it-works.en/)。

## 牛刀小試：觀察 Gthulhu 載入後資料層的效能差異

在本次實驗中，筆者的機器運作 在 Ubuntu 24.04 LTS 上，使用 Linux Kernel 6.12。實驗的目的是觀察 Gthulhu 在載入後對資料層效能的影響。

試驗環境如下：

- VM1 (Ubuntu 24.04 LTS, Linux Kernel 6.12)
    - 部署 free5GC v4.0.1
- VM2 (Ubuntu 20.04 LTS, Linux Kernel 5.4.0)
    - 部署 UERANSIM

![alt text](https://github.com/free5gc/free5gc.github.io/blob/main/docs/blog/20250726/fig2.png?raw=true)

待 PDU Session 建立後，筆者使用 `ping` 工具對 UPF N6 介面進行測試，並觀察在載入 Gthulhu 前後的延遲變化。

![alt text](https://github.com/free5gc/free5gc.github.io/blob/main/docs/blog/20250726/fig3.png?raw=true)

載入前，Linux 預設的排程器為 EEVDF，RTT 相關參數如下：

- rtt min = 1.263 ms
- rtt avg = 1.907 ms
- rtt max = 6.405 ms
- rtt mdev = 0.657 ms

rtt min/avg/max/mdev = 1.222/1.864/3.771/0.433 ms
載入 Gthulhu 後，RTT 參數變化如下：

- rtt min = 1.222 ms
- rtt avg = 1.864 ms
- rtt max = 3.771 ms
- rtt mdev = 0.433 ms

由此可見，載入 Gthulhu 後，RTT 的平均值和最大值均有所下降，顯示出 Gthulhu 在資料層的排程上確實有助於降低延遲。

## 對 GTP5G 進行最佳化排程

根據前面的實驗結果可以得知，在不對排程器進行任何調整的前提下，Gthulhu 確實有效的降低 RTT 的表現。那麼，我們有機會利用網路子系統的知識結合 Gthulhu 更進一步對 GTP5G 進行調教嗎？

>[!Note]
> 實驗環境如下：
> - 5GC on kubernetes
> - N3/N6 使用 [Multus CNI](https://github.com/k8snetworkplumbingwg/multus-cni) 建立 macvlan interfaces（N6 綁定 enp7s0，N3 介面綁定 dummy interface）

### 觀察 Downlink 由哪一個 cpu 負責處理

```
$ grep enp7s0 /proc/interrupts

 159:     116096     131508     763166     532207    4697697    3924514   24589811    5660340   29315073   11862910   25971964    8494127    1935719    2420802    5149765     948266    6835920    2126158    1825640    1044404  IR-PCI-MSIX-0000:07:00.0    0-edge      enp7s0
```

透過上方執行的命令可以得知 enp7s0 對應的 IRQ 為 159，接著利用 `cat /proc/irq/${IRQ}/smp_affinity_list` 可以得知 IRQ 159 綁定的 CPU：
```
$ cat /proc/irq/159/smp_affinity_list
11
```
當 enp7s0 收到來自 Data Network 的封包，會接封包送往 UPF Container 對應的 n6 interface，而 N6 interface 會將 downlink 封包轉送至虛擬介面 gtp5g 內。
因此，處理 gtp5g downlink 流量的 CPU 應該是 CPU 11，這一點可以透過 eBPF program 驗證。

在筆者先前撰寫的 [Debug gtp5g kernel module using stacktrace and eBPF](https://free5gc.org/blog/20241224/) 一文中已經探討過使用 eBPF 追蹤 kernel module 的可能性，只要追蹤一下 gtp5g 的 source code 便可以得知 downlink 封包最後會進入 `gtp5g_xmit_skb_ipv4`，使用 `sudo cat /sys/kernel/tracing/available_filter_functions | grep gtp5g` 也可得知該函式在 available_filter_functions 清單內。

```c
SEC("fentry/gtp5g_xmit_skb_ipv4")
int BPF_PROG(capture_skb, struct sk_buff *skb, struct gtp5g_pktinfo *pktinfo)
{
    __u64 pid_tgid = bpf_get_current_pid_tgid();
    __u32 pid = pid_tgid & 0xFFFFFFFF;
    __u32 tgid = pid_tgid >> 32;
    __u32 cpu = bpf_get_smp_processor_id();
    
    bpf_printk("gtp5g_xmit_skb_ipv4: PID=%u, TGID=%u, CPU=%u", pid, tgid, cpu);
    return 0;
}
```

將上述的 eBPF 程式載入到核心後，利用 UERANSIM 建立 PDU Session 向 `8.8.8.8` 發送 ICMP 封包時，我們即可觀察 eBPF 程式的輸出：

```
gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=11
          <idle>-0       [011] b.s31 6156182.987076: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=11
          <idle>-0       [011] b.s31 6156183.987343: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=11
          <idle>-0       [011] b.s31 6156184.986858: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=11
          <idle>-0       [011] b.s31 6156185.987004: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=11
          <idle>-0       [011] b.s31 6156186.987574: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=11
          <idle>-0       [011] b.s31 6156187.987330: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=11
          <idle>-0       [011] b.s31 6156188.987722: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=11
          <idle>-0       [011] b.s31 6156189.988054: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=11
          <idle>-0       [011] b.s31 6156190.988038: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=11
        kubelite-3377186 [011] b.s21 6156191.987614: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=3377186, TGID=3376931, CPU=11
          <idle>-0       [011] b.s31 6156192.987963: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=11
          <idle>-0       [011] b.s31 6156193.987763: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=11
          <idle>-0       [011] b.s31 6156194.988095: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=11
```

從 eBPF 程式的輸出可得知，gtp5g 的 downlink 流量確實由 CPU 11 負責處理，與先前的猜測相同。
當我使用 `echo "12" | sudo tee /proc/irq/159/smp_affinity_list` 修改 IRQ 159 綁定的 CPU 後，eBPF 程式的輸出也會馬上改變：

```
gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=12
          <idle>-0       [012] b.s31 6156445.013125: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=12
          <idle>-0       [012] b.s31 6156446.012413: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=12
          <idle>-0       [012] b.s31 6156447.012498: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=12
          <idle>-0       [012] b.s31 6156448.013280: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=12
          <idle>-0       [012] b.s31 6156449.012909: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=12
          <idle>-0       [012] b.s31 6156450.013119: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=12
          <idle>-0       [012] b.s31 6156451.013496: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=12
```

> 補充：
> IRQ 綁定的 CPU 有可能會被 irqbalance 動態的更新，建議可以用 `$ sudo systemctl stop irqbalance` 暫時關閉 irqbalance。

話說回來，即使將 irqbalance 關閉，eBPF 程式的輸出仍有可能出現非預期情況。
當我將 ICMP 的目標從外部 IP 改為 UPF container 本身 N6 網卡的 IP 時，eBPF 程式的輸出如下：

```
          nr-gnb-168420  [016] b.s41 6158463.012636: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=168420, TGID=168410, CPU=16
          nr-gnb-168420  [016] b.s41 6158464.012282: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=168420, TGID=168410, CPU=16
          nr-gnb-168420  [017] b.s41 6158465.012408: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=168420, TGID=168410, CPU=17
          nr-gnb-168420  [017] b.s41 6158466.012551: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=168420, TGID=168410, CPU=17
          nr-gnb-168420  [016] b.s41 6158467.012401: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=168420, TGID=168410, CPU=16
          nr-gnb-168420  [006] b.s41 6158468.012565: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=168420, TGID=168410, CPU=6
          nr-gnb-168420  [006] b.s41 6158469.012700: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=168420, TGID=168410, CPU=6
          nr-gnb-168420  [006] b.s41 6158470.012549: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=168420, TGID=168410, CPU=6
          nr-gnb-168420  [006] b.s41 6158471.012763: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=168420, TGID=168410, CPU=6
          nr-gnb-168420  [006] b.s41 6158472.012862: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=168420, TGID=168410, CPU=6
```

基本上執行 `gtp5g_xmit_skb_ipv4` 的 CPU 一定會是 scheduler 為 `nr-gnb` process 分配的 CPU。原因也很簡單，因為送往 N6 網卡的封包會在 Container 內處理完畢，不會經過 enp7s0 網卡，所以封包從 UERANSIM 傳出一路到 N6 返回都會在同一個上下文內處理完畢。

了解 Linux 核心處理封包的行為後，我們可以實驗看看當系統滿載的情況下，UERANSIM 透過 uesimtun0 向 UPF N6 IP 發送 ICMP echo request 的表現。

### Gthulhu 的組態設定

在本次實驗中，組態的設定固定如下：

```yaml
# Gthulhu Scheduler Configuration
# This configuration file allows you to adjust scheduler parameters before eBPF program loading

scheduler:
  # Default time slice in nanoseconds (default: 5000000 = 5ms)
  slice_ns_default: 2000000
  
  # Minimum time slice in nanoseconds (default: 500000 = 0.5ms)
  slice_ns_min: 500000
api:
  enabled: false
  url: http://127.0.0.1:8080
  interval: 5
debug: false
early_processing: false
builtin_idle: false
```

### 使用 `stress-ng` 產生負載

```shell
$ stress-ng -c 20 --timeout 60s --metrics-brief
```

### 使用 `ping` 進行測試

Gthulhu scheduler 借鑑了 scx_rustland 的設計，因此，在本實驗中我們使用 scx_rustland 作為對照組：

```shell
/UERANSIM # taskset -c 5 ping 10.10.2.60 -I uesimtun0 -c 10
PING 10.10.2.60 (10.10.2.60): 56 data bytes
64 bytes from 10.10.2.60: seq=0 ttl=64 time=75.589 ms
64 bytes from 10.10.2.60: seq=1 ttl=64 time=75.917 ms
64 bytes from 10.10.2.60: seq=2 ttl=64 time=63.919 ms
64 bytes from 10.10.2.60: seq=3 ttl=64 time=71.934 ms
64 bytes from 10.10.2.60: seq=4 ttl=64 time=72.005 ms
64 bytes from 10.10.2.60: seq=5 ttl=64 time=64.108 ms
64 bytes from 10.10.2.60: seq=6 ttl=64 time=83.945 ms
64 bytes from 10.10.2.60: seq=7 ttl=64 time=100.525 ms
64 bytes from 10.10.2.60: seq=8 ttl=64 time=59.987 ms
64 bytes from 10.10.2.60: seq=9 ttl=64 time=63.940 ms

--- 10.10.2.60 ping statistics ---
10 packets transmitted, 10 packets received, 0% packet loss
round-trip min/avg/max = 59.987/73.186/100.525 ms
```

我們可以觀察出：當系統的每個 CPU 滿載時，scx_rustland 在處理封包的效率上非常糟糕。這個問題在 Gthulhu 排程器上亦然：

```shell
/UERANSIM # taskset -c 5 ping 10.10.2.60 -I uesimtun0 -c 10
PING 10.10.2.60 (10.10.2.60): 56 data bytes
64 bytes from 10.10.2.60: seq=0 ttl=64 time=22.085 ms
64 bytes from 10.10.2.60: seq=1 ttl=64 time=59.904 ms
64 bytes from 10.10.2.60: seq=2 ttl=64 time=96.299 ms
64 bytes from 10.10.2.60: seq=3 ttl=64 time=20.349 ms
64 bytes from 10.10.2.60: seq=4 ttl=64 time=71.244 ms
64 bytes from 10.10.2.60: seq=5 ttl=64 time=28.001 ms
64 bytes from 10.10.2.60: seq=6 ttl=64 time=74.964 ms
64 bytes from 10.10.2.60: seq=7 ttl=64 time=59.977 ms
64 bytes from 10.10.2.60: seq=8 ttl=64 time=32.617 ms
64 bytes from 10.10.2.60: seq=9 ttl=64 time=90.945 ms

--- 10.10.2.60 ping statistics ---
10 packets transmitted, 10 packets received, 0% packet loss
round-trip min/avg/max = 20.349/55.638/96.299 ms
```

接著，讓我們嘗試以下做法，看能不能降低 round-trip-time：

- 將某個 CPU（這裡使用 CPU 5）給 UERANSIM、`icmp` 工具
- 若其他任務被分配到 CPU 5，則隨機為它分配其他 CPU

相關改動請參考：

```diff
    // ...
    log.Println("scheduler started")
+   var specialPid int32 = 168420 // Special case for PID 168420
+   var specialPidCpu int32 = 5

	for true {
		select {
		case <-ctx.Done():
			log.Println("context done, exiting scheduler loop")
			return
		default:
		}
		sched.DrainQueuedTask(bpfModule)
		t = sched.GetTaskFromPool()
		if t == nil {
			bpfModule.BlockTilReadyForDequeue(ctx)
		} else if t.Pid != -1 {
			task = core.NewDispatchedTask(t)
			err, cpu = bpfModule.SelectCPU(t)
			if err != nil {
				log.Printf("SelectCPU failed: %v", err)
			}

+   		if t.Pid == specialPid {
+   			if specialPidCpu == -1 && cpu != core.RL_CPU_ANY {
+   				specialPidCpu = cpu
+   			} else {
+   				cpu = specialPidCpu
+   			}
+   		} else {
+   			if cpu == core.RL_CPU_ANY {
+   				// ramdom select cpu 0-19
+   				cpu = int32(rand.Intn(20))
+   			}
+   			if specialPidCpu == cpu {
+   				if (cpu & 1) == 1 {
+   					cpu = cpu - 1
+   				} else {
+   					cpu = cpu + 1
+   				}
+   			}
+   		}

			// Evaluate used task time slice.
			nrWaiting := core.GetNrQueued() + core.GetNrScheduled() + 1
			task.Vtime = t.Vtime
```

Special pid `168420` 是透過 eBPF 程式觀察出負責執行 `gtp5g_xmit_skb_ipv4()` 的 process id：

```
          nr-gnb-770208  [005] b.s41 6233538.456200: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=770208, TGID=770198, CPU=5
          nr-gnb-770208  [005] bNs41 6233711.301750: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=770208, TGID=770198, CPU=5
          nr-gnb-770208  [005] bNs41 6233712.346565: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=770208, TGID=770198, CPU=5
          nr-gnb-770208  [005] bNs41 6233713.312931: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=770208, TGID=770198, CPU=5
          nr-gnb-770208  [005] bNs41 6233714.314609: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=770208, TGID=770198, CPU=5
          nr-gnb-770208  [005] bNs41 6233715.340537: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=770208, TGID=770198, CPU=5
          nr-gnb-770208  [005] b.s41 6233716.337300: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=770208, TGID=770198, CPU=5
          nr-gnb-770208  [005] b.s41 6233717.389852: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=770208, TGID=770198, CPU=5
          nr-gnb-770208  [005] b.s41 6233718.387986: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=770208, TGID=770198, CPU=5
          nr-gnb-770208  [005] b.s41 6233719.368526: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=770208, TGID=770198, CPU=5
          nr-gnb-770208  [005] bNs41 6233720.396073: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=770208, TGID=770198, CPU=5
```

完成修改後，讓我們嘗試重新執行 Gthulhu 並再次測試：

```shell
/UERANSIM # taskset -c 5 ping 10.10.2.60 -I uesimtun0 -c 10
PING 10.10.2.60 (10.10.2.60): 56 data bytes
64 bytes from 10.10.2.60: seq=0 ttl=64 time=0.767 ms
64 bytes from 10.10.2.60: seq=1 ttl=64 time=1.150 ms
64 bytes from 10.10.2.60: seq=2 ttl=64 time=1.120 ms
64 bytes from 10.10.2.60: seq=3 ttl=64 time=0.968 ms
64 bytes from 10.10.2.60: seq=4 ttl=64 time=1.002 ms
64 bytes from 10.10.2.60: seq=5 ttl=64 time=0.601 ms
64 bytes from 10.10.2.60: seq=6 ttl=64 time=1.132 ms
64 bytes from 10.10.2.60: seq=7 ttl=64 time=0.833 ms
64 bytes from 10.10.2.60: seq=8 ttl=64 time=0.666 ms
64 bytes from 10.10.2.60: seq=9 ttl=64 time=0.795 ms

--- 10.10.2.60 ping statistics ---
10 packets transmitted, 10 packets received, 0% packet loss
round-trip min/avg/max = 0.601/0.903/1.150 ms
```

從結果來看，修改後的 Gthulhu 排程器在高負載的情況下使 UPF 能在短時間內處理來自 UERANSIM 的封包。這樣的表現與我們預期的一致。

### 透過自定義組態降低 RTT

前面的的實驗中，我們為特定的 process 分配了專用的 CPU，這樣的做法確實能夠在高負載的情況下提升 RTT 的表現。然而，這種方法並不通用，因為每個系統的負載情況和工作負載可能會有所不同。
因此，Gthulhu 發展出一套自定義的組態設定，讓使用者能夠根據自己的需求調整排程策略，專案原始碼請參考 [Gthulhu/api](https://github.com/Gthulhu/api)。

```json
{
  "server": {
    "port": ":8080",
    "read_timeout": 15,
    "write_timeout": 15,
    "idle_timeout": 60
  },
  "logging": {
    "level": "info",
    "format": "text"
  },
  "jwt": {
    "private_key_path": "./config/jwt_private_key.key",
    "token_duration": 24
  },
  "strategies": {
    "default": [
      {
        "priority": true,
        "execution_time": 20000,
        "selectors": [
          {
            "key": "app",
            "value": "ueransim-macvlan"
          }
        ],
        "command_regex": "nr-gnb|nr-ue|ping"
      }
    ]
  }
}
```

透過上方的 json 檔案，api server 能夠找出對應的 processes，並將這些 process 的排程策略更新至 Gthulhu。
如果該任務的 `"priority": true`，則該任務本身能夠搶佔其他非 `"priority": true` 的任務，大大的降低任務從 `runnable` 到 `running` 的時間。
在 free5GC 的整合案例中，降低 ueransim 的排程延遲代表著 UPF 能夠更快的處理來自 RAN 的封包，進而降低整體的 RTT。

<iframe width="560" height="315" src="https://www.youtube.com/embed/MfU64idQcHg?si=1tiZax9q0iLmONOE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

上方影片展示了在高負載的情況下，Gthulhu 如何透過自定義的排程策略顯著降低 RTT 的表現。

<iframe width="560" height="315" src="https://www.youtube.com/embed/R4EmZ18P954?si=9q3Y-Ess4SRZBzmn" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

此外，Gthulhu 也支援簡易的 WEB GUI，讓使用者能夠更直觀地管理和監控排程策略。


## 結論

5G 提出了網路切片的概念，期待透過將實體網路切分成多個虛擬網路來提供不同的服務品質。有了 Gthulhu 這樣的自訂排程器，我們可以更靈活地管理和優化這些虛擬網路的性能，將不同業務需求的 UPF 部署在不同的節點上，並根據實際需求調整排程策略。

## 關於作者

Ian Chen 是一名熱衷於開源技術的開發者，專注於 5G 和雲原生架構的研究。他發起了 [Gthulhu](https://gthulhu.github.io/docs/) 專案，同時也是 free5GC 的主要貢獻者，致力於推廣和實現 5G 網路的開源解決方案。