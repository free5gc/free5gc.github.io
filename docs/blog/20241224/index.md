# Debug gtp5g kernel module using stacktrace and eBPF
>[!NOTE]
> Author: [Ian Chen](https://www.linkedin.com/in/ian-chen-88b70b1aa/)
> Date: 2024/12/24
---

## Case Study - kernel panic caused by the online charging PDU Session

free5GC is highly rely on the infrastructures provided by the Linux Kernel, especially the gtp5g kernel module.

[@andy89923](https://github.com/andy89923) found a reproducible kernel panic issue.
Follow the actions below can always produce the kernel panic:

- Create online charging PDU Session
- Ping the Data Network (should match the ip filter of the charging configuration)

Please also note that, the case of kernel panic will only happens if the version of gtp5g greater than v0.8.x.

### Figure out the problem

Although we can get the panic log by using the dmesg. However, the stack dumps are not useful enough for kernel debugging at all.

However, we can use the [decode_stacktrace.sh](https://github.com/torvalds/linux/blob/master/scripts/decode_stacktrace.sh) can find the specific line in source code by leveraging the vmlinux.

The original panic logs:
```
[  +0.004968] ------------[ cut here ]------------
[  +0.000002] kernel BUG at mm/slub.c:307!
[  +0.000109] invalid opcode: 0000 [#1] SMP PTI
[  +0.000056] CPU: 3 PID: 191301 Comm: nrf Tainted: G           OE     5.4.0-131-generic #147-Ubuntu
[  +0.000068] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS rel-1.16.3-0-ga6ed6b701f0a-prebuilt.qemu.org 04/01/2014
[  +0.000047] RIP: 0010:kfree+0x236/0x250
[  +0.000048] Code: e7 e8 9e 71 fd ff e9 ef fe ff ff 4d 89 f1 41 b8 01 00 00 00 48 89 d9 48 89 da 4c 89 e6 4c 89 ef e8 6f fa ff ff e9 d0 fe ff ff <0f> 0b 48 8b 05 d1 51 77 01 e9 ff fd ff ff 66 66 2e 0f 1f 84 00 00
[  +0.000108] RSP: 0000:ffffa104c015c7f0 EFLAGS: 00010246
[  +0.000018] RAX: ffff93e58bc98000 RBX: ffff93e58bc98000 RCX: ffff93e58bc98000
[  +0.000017] RDX: 0000000000039962 RSI: bdd6aff4c23d967a RDI: ffff93e58bc98000
[  +0.000017] RBP: ffffa104c015c810 R08: ffff93e58bc98000 R09: ffffa104c015c8d8
[  +0.000018] R10: ffff93e5d302c680 R11: 0000000000000001 R12: fffffc7d8c2f2600
[  +0.000018] R13: ffff93e6adc06bc0 R14: ffffffff99edcf25 R15: ffff93e565a70600
[  +0.000017] FS:  000000c000580090(0000) GS:ffff93e6afac0000(0000) knlGS:0000000000000000
[  +0.000020] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[  +0.000014] CR2: 00007fac6fecf160 CR3: 000000034857c001 CR4: 0000000000760ee0
[  +0.000026] DR0: 0000000000000000 DR1: 0000000000000000 DR2: 0000000000000000
[  +0.000018] DR3: 0000000000000000 DR6: 00000000fffe0ff0 DR7: 0000000000000400
[  +0.000021] PKRU: 55555554
[  +0.000007] Call Trace:
[  +0.000014]  <IRQ>
[  +0.000031]  skb_free_head+0x25/0x30
[  +0.000018]  skb_release_data+0x11d/0x180
[  +0.000015]  skb_release_all+0x26/0x30
[  +0.000015]  consume_skb+0x2c/0xb0
[  +0.000046]  gtp5g_dev_xmit+0xc3/0x170 [gtp5g]
[  +0.000016]  ? update_load_avg+0x7c/0x670
[  +0.000017]  dev_hard_start_xmit+0x91/0x1f0
[  +0.000019]  __dev_queue_xmit+0x75f/0x990
[  +0.000016]  ? nfnetlink_has_listeners+0x15/0x20 [nfnetlink]
[  +0.000016]  dev_queue_xmit+0x10/0x20
[  +0.000014]  neigh_direct_output+0x11/0x20
[  +0.000019]  ip_finish_output2+0x17e/0x580
[  +0.000016]  __ip_finish_output+0xf3/0x270
[  +0.000017]  ip_finish_output+0x2d/0xb0
[  +0.000018]  ip_output+0x75/0xf0
[  +0.000010]  ? __ip_finish_output+0x270/0x270
[  +0.000013]  ip_forward_finish+0x58/0x90
[  +0.000012]  ip_forward+0x3b9/0x4c0
[  +0.000010]  ? ip4_key_hashfn+0xb0/0xb0
[  +0.000012]  ip_sublist_rcv_finish+0x3d/0x50
[  +0.000021]  ip_sublist_rcv+0x1c5/0x270
[  +0.000956]  ? ip_rcv_finish_core.isra.0+0x3c0/0x3c0
[  +0.000637]  ip_list_rcv+0x10b/0x130
[  +0.000678]  __netif_receive_skb_list_core+0x228/0x250
[  +0.000576]  netif_receive_skb_list_internal+0x1a1/0x2b0
[  +0.000572]  gro_normal_list.part.0+0x1e/0x40
[  +0.000524]  napi_complete_done+0x91/0x130
[  +0.000557]  virtnet_poll+0x30d/0x450 [virtio_net]
[  +0.000558]  net_rx_action+0x142/0x390
[  +0.000598]  __do_softirq+0xd1/0x2c1
[  +0.000559]  irq_exit+0xae/0xb0
[  +0.000500]  do_IRQ+0x5a/0xf0
[  +0.000504]  common_interrupt+0xf/0xf
[  +0.000488]  </IRQ>
[  +0.000467] RIP: 0033:0x423172
[  +0.000467] Code: 23 4c 89 44 24 38 e8 8d 46 ff ff 48 85 f6 0f 84 a0 00 00 00 48 8b 94 24 88 00 00 00 49 89 f1 48 8b 74 24 48 4d 89 c8 4d 8b 09 <49> 29 d0 4d 85 c9 74 b0 4d 89 ca 49 29 d1 4c 39 ce 77 a5 4c 89 44
[  +0.001066] RSP: 002b:000000c000593e90 EFLAGS: 00000202 ORIG_RAX: ffffffffffffffdb
[  +0.000517] RAX: 000000c000387200 RBX: 0000000000018e00 RCX: 5000000000000000
[  +0.000461] RDX: 000000c000380000 RSI: 0000000000020000 RDI: 0000000000000040
[  +0.000590] RBP: 000000c000593f08 R08: 000000c0003873d0 R09: 0000000000d17b82
[  +0.000601] R10: 0000000000d1ce8e R11: 0000000000018e00 R12: 0000000000000001
[  +0.000619] R13: 13679e0f6eacd19f R14: 000000c0005821a0 R15: 0000000000000000
[  +0.000461] Modules linked in: sctp vxlan xt_multiport xt_set ipt_rpfilter iptable_raw ip_set_hash_ip ip_set_hash_net ip_set wireguard ip6_udp_tunnel veth xfrm_user xfrm_algo nf_conntrack_netlink xt_addrtype xt_nat xt_tcpudp xt_MASQUERADE xt_mark xt_conntrack iptable_mangle ip6table_filter ip6table_mangle ip6table_nat ip6_tables iptable_nat nf_nat br_netfilter bridge stp llc nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 nft_counter nft_compat nf_tables nfnetlink iptable_filter xt_comment bpfilter aufs overlay dummy dm_multipath scsi_dh_rdac scsi_dh_emc scsi_dh_alua binfmt_misc intel_rapl_msr intel_rapl_common isst_if_common nfit kvm_intel kvm rapl joydev input_leds serio_raw mac_hid qemu_fw_cfg sch_fq_codel gtp5g(OE) sunrpc ramoops udp_tunnel reed_solomon efi_pstore ip_tables x_tables autofs4 btrfs zstd_compress raid10 raid456 async_raid6_recov async_memcpy async_pq async_xor async_tx xor raid6_pq libcrc32c raid1 raid0 multipath linear hid_generic usbhid hid bochs_drm drm_vram_helper ttm
[  +0.000189]  drm_kms_helper crct10dif_pclmul crc32_pclmul syscopyarea sysfillrect ghash_clmulni_intel sysimgblt aesni_intel crypto_simd cryptd glue_helper fb_sys_fops virtio_net psmouse net_failover drm failover virtio_scsi i2c_piix4 pata_acpi floppy
[  +0.005947] ---[ end trace e017af78fce65824 ]---
```

You can follow the commands below to make the panic logs more human-friendly:
```
$ sudo apt install linux-source-5.4.0
$ cd /usr/src/linux-source-5.4.0
$ sudo make -j$(nproc) vmlinux // if you don't have vmlinux file
$ sudo ./scripts/decode_stacktrace.sh ./vmlinux ./ ~/gtp5g/ < ~/panic.log  > ~/out.log
```
The output will looks like:
```
[  +0.004968] ------------[ cut here ]------------
[  +0.000002] kernel BUG at mm/slub.c:307!
[  +0.000109] invalid opcode: 0000 [#1] SMP PTI
[  +0.000056] CPU: 3 PID: 191301 Comm: nrf Tainted: G           OE     5.4.0-131-generic #147-Ubuntu
[  +0.000068] Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS rel-1.16.3-0-ga6ed6b701f0a-prebuilt.qemu.org 04/01/2014
[   +0.000047] RIP: 0010:kfree (/usr/src/linux-source-5.4.0/mm/slub.c:307 /usr/src/linux-source-5.4.0/mm/slub.c:302 /usr/src/linux-source-5.4.0/mm/slub.c:3035 /usr/src/linux-source-5.4.0/mm/slub.c:3060 /usr/src/linux-source-5.4.0/mm/slub.c:4027)
[ +0.000048] Code: e7 e8 9e 71 fd ff e9 ef fe ff ff 4d 89 f1 41 b8 01 00 00 00 48 89 d9 48 89 da 4c 89 e6 4c 89 ef e8 6f fa ff ff e9 d0 fe ff ff <0f> 0b 48 8b 05 d1 51 77 01 e9 ff fd ff ff 66 66 2e 0f 1f 84 00 00
All code
========
   0:	e7 e8                	out    %eax,$0xe8
   2:	9e                   	sahf
   3:	71 fd                	jno    0x2
   5:	ff                   	(bad)
   6:	e9 ef fe ff ff       	jmpq   0xfffffffffffffefa
   b:	4d 89 f1             	mov    %r14,%r9
   e:	41 b8 01 00 00 00    	mov    $0x1,%r8d
  14:	48 89 d9             	mov    %rbx,%rcx
  17:	48 89 da             	mov    %rbx,%rdx
  1a:	4c 89 e6             	mov    %r12,%rsi
  1d:	4c 89 ef             	mov    %r13,%rdi
  20:	e8 6f fa ff ff       	callq  0xfffffffffffffa94
  25:	e9 d0 fe ff ff       	jmpq   0xfffffffffffffefa
  2a:*	0f 0b                	ud2    		<-- trapping instruction
  2c:	48 8b 05 d1 51 77 01 	mov    0x17751d1(%rip),%rax        # 0x1775204
  33:	e9 ff fd ff ff       	jmpq   0xfffffffffffffe37
  38:	66                   	data16
  39:	66                   	data16
  3a:	2e                   	cs
  3b:	0f                   	.byte 0xf
  3c:	1f                   	(bad)
  3d:	84 00                	test   %al,(%rax)
	...

Code starting with the faulting instruction
===========================================
   0:	0f 0b                	ud2
   2:	48 8b 05 d1 51 77 01 	mov    0x17751d1(%rip),%rax        # 0x17751da
   9:	e9 ff fd ff ff       	jmpq   0xfffffffffffffe0d
   e:	66                   	data16
   f:	66                   	data16
  10:	2e                   	cs
  11:	0f                   	.byte 0xf
  12:	1f                   	(bad)
  13:	84 00                	test   %al,(%rax)
	...
[  +0.000108] RSP: 0000:ffffa104c015c7f0 EFLAGS: 00010246
[  +0.000018] RAX: ffff93e58bc98000 RBX: ffff93e58bc98000 RCX: ffff93e58bc98000
[  +0.000017] RDX: 0000000000039962 RSI: bdd6aff4c23d967a RDI: ffff93e58bc98000
[  +0.000017] RBP: ffffa104c015c810 R08: ffff93e58bc98000 R09: ffffa104c015c8d8
[  +0.000018] R10: ffff93e5d302c680 R11: 0000000000000001 R12: fffffc7d8c2f2600
[  +0.000018] R13: ffff93e6adc06bc0 R14: ffffffff99edcf25 R15: ffff93e565a70600
[  +0.000017] FS:  000000c000580090(0000) GS:ffff93e6afac0000(0000) knlGS:0000000000000000
[  +0.000020] CS:  0010 DS: 0000 ES: 0000 CR0: 0000000080050033
[  +0.000014] CR2: 00007fac6fecf160 CR3: 000000034857c001 CR4: 0000000000760ee0
[  +0.000026] DR0: 0000000000000000 DR1: 0000000000000000 DR2: 0000000000000000
[  +0.000018] DR3: 0000000000000000 DR6: 00000000fffe0ff0 DR7: 0000000000000400
[  +0.000021] PKRU: 55555554
[  +0.000007] Call Trace:
[  +0.000014]  <IRQ>
[   +0.000031] skb_free_head (/usr/src/linux-source-5.4.0/net/core/skbuff.c:602)
[   +0.000018] skb_release_data (/usr/src/linux-source-5.4.0/net/core/skbuff.c:622)
[   +0.000015] skb_release_all (/usr/src/linux-source-5.4.0/net/core/skbuff.c:676)
[   +0.000015] consume_skb (/usr/src/linux-source-5.4.0/net/core/skbuff.c:690 /usr/src/linux-source-5.4.0/net/core/skbuff.c:848)
[   +0.000046] gtp5g_dev_xmit (/home/ianchen0119/gtp5g/src/gtpu/dev.c:136) gtp5g
[   +0.000016] ? update_load_avg (/usr/src/linux-source-5.4.0/kernel/sched/fair.c:3388 /usr/src/linux-source-5.4.0/kernel/sched/fair.c:3602)
[   +0.000017] dev_hard_start_xmit (/usr/src/linux-source-5.4.0/./include/linux/prandom.h:58 /usr/src/linux-source-5.4.0/net/core/dev.c:3216 /usr/src/linux-source-5.4.0/net/core/dev.c:3234)
[   +0.000019] __dev_queue_xmit (/usr/src/linux-source-5.4.0/./include/net/sch_generic.h:179 /usr/src/linux-source-5.4.0/net/core/dev.c:3453 /usr/src/linux-source-5.4.0/net/core/dev.c:3765)
[   +0.000016] ? nfnetlink_has_listeners+0x15/0x20 nfnetlink
[   +0.000016] dev_queue_xmit (/usr/src/linux-source-5.4.0/net/core/dev.c:3834)
[   +0.000014] neigh_direct_output (/usr/src/linux-source-5.4.0/net/core/neighbour.c:1548)
[   +0.000019] ip_finish_output2 (/usr/src/linux-source-5.4.0/./include/net/neighbour.h:510 /usr/src/linux-source-5.4.0/net/ipv4/ip_output.c:236)
[   +0.000016] __ip_finish_output (/usr/src/linux-source-5.4.0/net/ipv4/ip_output.c:317)
[   +0.000017] ip_finish_output (/usr/src/linux-source-5.4.0/net/ipv4/ip_output.c:326)
[   +0.000018] ip_output (/usr/src/linux-source-5.4.0/net/ipv4/ip_output.c:444)
[   +0.000010] ? __ip_finish_output (/usr/src/linux-source-5.4.0/net/ipv4/ip_output.c:320)
[   +0.000013] ip_forward_finish (/usr/src/linux-source-5.4.0/net/ipv4/ip_forward.c:84)
[   +0.000012] ip_forward (/usr/src/linux-source-5.4.0/./include/linux/netfilter.h:300 /usr/src/linux-source-5.4.0/net/ipv4/ip_forward.c:157)
[   +0.000010] ? ip4_key_hashfn (/usr/src/linux-source-5.4.0/net/ipv4/ip_forward.c:66)
[   +0.000012] ip_sublist_rcv_finish (/usr/src/linux-source-5.4.0/net/ipv4/ip_input.c:539)
[   +0.000021] ip_sublist_rcv (/usr/src/linux-source-5.4.0/net/ipv4/ip_input.c:588)
[   +0.000956] ? ip_rcv_finish_core.isra.0 (/usr/src/linux-source-5.4.0/net/ipv4/ip_input.c:407)
[   +0.000637] ip_list_rcv (/usr/src/linux-source-5.4.0/net/ipv4/ip_input.c:622)
[   +0.000678] __netif_receive_skb_list_core (/usr/src/linux-source-5.4.0/net/core/dev.c:5014 /usr/src/linux-source-5.4.0/net/core/dev.c:5062)
[   +0.000576] netif_receive_skb_list_internal (/usr/src/linux-source-5.4.0/net/core/dev.c:5116 /usr/src/linux-source-5.4.0/net/core/dev.c:5209)
[   +0.000572] gro_normal_list.part.0 (/usr/src/linux-source-5.4.0/./include/linux/compiler.h:295 /usr/src/linux-source-5.4.0/./include/linux/list.h:28 /usr/src/linux-source-5.4.0/net/core/dev.c:5321)
[   +0.000524] napi_complete_done (/usr/src/linux-source-5.4.0/net/core/dev.c:6063 (discriminator 1) /usr/src/linux-source-5.4.0/net/core/dev.c:6051 (discriminator 1))
[   +0.000557] virtnet_poll+0x30d/0x450 virtio_net
[   +0.000558] net_rx_action (/usr/src/linux-source-5.4.0/net/core/dev.c:6366 /usr/src/linux-source-5.4.0/net/core/dev.c:6436)
[   +0.000598] __do_softirq (/usr/src/linux-source-5.4.0/./arch/x86/include/asm/jump_label.h:25 /usr/src/linux-source-5.4.0/./include/linux/jump_label.h:200 /usr/src/linux-source-5.4.0/./include/trace/events/irq.h:142 /usr/src/linux-source-5.4.0/kernel/softirq.c:293)
[   +0.000559] irq_exit (/usr/src/linux-source-5.4.0/kernel/softirq.c:373 /usr/src/linux-source-5.4.0/kernel/softirq.c:413)
[   +0.000500] do_IRQ (/usr/src/linux-source-5.4.0/arch/x86/kernel/irq.c:267 (discriminator 42))
[   +0.000504] common_interrupt (/usr/src/linux-source-5.4.0/arch/x86/entry/entry_64.S:613)
[  +0.000488]  </IRQ>
[  +0.000467] RIP: 0033:0x423172
[ +0.000467] Code: 23 4c 89 44 24 38 e8 8d 46 ff ff 48 85 f6 0f 84 a0 00 00 00 48 8b 94 24 88 00 00 00 49 89 f1 48 8b 74 24 48 4d 89 c8 4d 8b 09 <49> 29 d0 4d 85 c9 74 b0 4d 89 ca 49 29 d1 4c 39 ce 77 a5 4c 89 44
All code
========
   0:	23 4c 89 44          	and    0x44(%rcx,%rcx,4),%ecx
   4:	24 38                	and    $0x38,%al
   6:	e8 8d 46 ff ff       	callq  0xffffffffffff4698
   b:	48 85 f6             	test   %rsi,%rsi
   e:	0f 84 a0 00 00 00    	je     0xb4
  14:	48 8b 94 24 88 00 00 	mov    0x88(%rsp),%rdx
  1b:	00
  1c:	49 89 f1             	mov    %rsi,%r9
  1f:	48 8b 74 24 48       	mov    0x48(%rsp),%rsi
  24:	4d 89 c8             	mov    %r9,%r8
  27:	4d 8b 09             	mov    (%r9),%r9
  2a:*	49 29 d0             	sub    %rdx,%r8		<-- trapping instruction
  2d:	4d 85 c9             	test   %r9,%r9
  30:	74 b0                	je     0xffffffffffffffe2
  32:	4d 89 ca             	mov    %r9,%r10
  35:	49 29 d1             	sub    %rdx,%r9
  38:	4c 39 ce             	cmp    %r9,%rsi
  3b:	77 a5                	ja     0xffffffffffffffe2
  3d:	4c                   	rex.WR
  3e:	89                   	.byte 0x89
  3f:	44                   	rex.R

Code starting with the faulting instruction
===========================================
   0:	49 29 d0             	sub    %rdx,%r8
   3:	4d 85 c9             	test   %r9,%r9
   6:	74 b0                	je     0xffffffffffffffb8
   8:	4d 89 ca             	mov    %r9,%r10
   b:	49 29 d1             	sub    %rdx,%r9
   e:	4c 39 ce             	cmp    %r9,%rsi
  11:	77 a5                	ja     0xffffffffffffffb8
  13:	4c                   	rex.WR
  14:	89                   	.byte 0x89
  15:	44                   	rex.R
[  +0.001066] RSP: 002b:000000c000593e90 EFLAGS: 00000202 ORIG_RAX: ffffffffffffffdb
[  +0.000517] RAX: 000000c000387200 RBX: 0000000000018e00 RCX: 5000000000000000
[  +0.000461] RDX: 000000c000380000 RSI: 0000000000020000 RDI: 0000000000000040
[  +0.000590] RBP: 000000c000593f08 R08: 000000c0003873d0 R09: 0000000000d17b82
[  +0.000601] R10: 0000000000d1ce8e R11: 0000000000018e00 R12: 0000000000000001
[  +0.000619] R13: 13679e0f6eacd19f R14: 000000c0005821a0 R15: 0000000000000000
[  +0.000461] Modules linked in: sctp vxlan xt_multiport xt_set ipt_rpfilter iptable_raw ip_set_hash_ip ip_set_hash_net ip_set wireguard ip6_udp_tunnel veth xfrm_user xfrm_algo nf_conntrack_netlink xt_addrtype xt_nat xt_tcpudp xt_MASQUERADE xt_mark xt_conntrack iptable_mangle ip6table_filter ip6table_mangle ip6table_nat ip6_tables iptable_nat nf_nat br_netfilter bridge stp llc nf_conntrack nf_defrag_ipv6 nf_defrag_ipv4 nft_counter nft_compat nf_tables nfnetlink iptable_filter xt_comment bpfilter aufs overlay dummy dm_multipath scsi_dh_rdac scsi_dh_emc scsi_dh_alua binfmt_misc intel_rapl_msr intel_rapl_common isst_if_common nfit kvm_intel kvm rapl joydev input_leds serio_raw mac_hid qemu_fw_cfg sch_fq_codel gtp5g(OE) sunrpc ramoops udp_tunnel reed_solomon efi_pstore ip_tables x_tables autofs4 btrfs zstd_compress raid10 raid456 async_raid6_recov async_memcpy async_pq async_xor async_tx xor raid6_pq libcrc32c raid1 raid0 multipath linear hid_generic usbhid hid bochs_drm drm_vram_helper ttm
[  +0.000189]  drm_kms_helper crct10dif_pclmul crc32_pclmul syscopyarea sysfillrect ghash_clmulni_intel sysimgblt aesni_intel crypto_simd cryptd glue_helper fb_sys_fops virtio_net psmouse net_failover drm failover virtio_scsi i2c_piix4 pata_acpi floppy
[  +0.005947] ---[ end trace e017af78fce65824 ]---

```

The kernel panic is caused by the kfree function, I believe that the root cause is the socket buffer [double-free](https://stackoverflow.com/questions/21057393/what-does-double-free-mean). Moreover, `gtp5g_dev_xmit` is the dowlink entry function in GTP5G, So I can narrow down the scope of the problem.

For the online charging session, the FAR (Forwarding Action Rule) action will be changed to PKT_DROP after the first uplink packet be sent to data network til the UPF get the quota from SMF. So the downlink packet for responding the first uplink packet will be freed twice before UPF het the new quota.

> The deatils of the charging system design can be found at [CHF design document](https://free5gc.org/doc/Chf/design/#usage-report).

The interesting thing is that the panic won't happens til the we upgrade the gtp5g to v0.9.0^.
I believe that the issue started to be visible is effected by [#101](https://github.com/free5gc/gtp5g/pull/101), because of it gives the more accurate packet counting (timing issue).

## The potentials of the eBPF for kernel debugging

The article: [Live-patching security vulnerabilities inside the Linux kernel with eBPF Linux Security Module](https://blog.cloudflare.com/live-patch-security-vulnerabilities-with-ebpf-lsm/), posted by CloudFlare, has well explained how they leverage the eBPF to detect critical events in the kernel, even make the kernel more secured!

It inspires me started thinking: is it possible to use eBPF to troubleshoot our own kernel module?

### [Optional] Compile the kernel with BTF enabled

In our testing environment, we build the kernel v6.12.4:
```
$ wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.12.4.tar.xz
$ tar xvf linux-6.12.4.tar.xz
```
Once you have downloaded the kernel source, you can started building the kernel by following the steps described in the article: [Building the Linux kernel with BTF](https://medium.com/@suruti94/building-the-linux-kernel-with-btf-1a617cfb4a24).

### What is BTF?


> The Extended Berkeley Packet Filter (eBPF) is esteemed for its portability, a primary attribute of which is due to the BPF Type Format (BTF). More details about BTF can be discovered in this comprehensive guide.
>
> Before the advent of Compile Once-Run Everywhere (CO-RE), developers working with eBPF had to compile an individual eBPF object for each kernel version they intended to support. This stipulation led toolkits, such as iovisor/bcc, to depend on runtime compilations to handle different kernel versions.
>
> However, the introduction of CO-RE facilitated a significant shift in eBPF portability, allowing a single eBPF object to be loaded into multiple differing kernels. This is achieved by the libbpf loader, a component within the eBPF's loader and verification architecture. The libbpf loader arranges the necessary infrastructure for an eBPF object, including eBPF map creation, code relocation, setting up eBPF probes, managing links, handling their attachments, among others.
>
> Here's the technical insight: both the eBPF object and the target kernel contain BTF information, generally embedded within their respective ELF (Executable and Linkable Format) files. The libbpf loader leverages this embedded BTF information to calculate the requisite changes such as relocations, map creations, probe attachments, and more for an eBPF object. As a result, this eBPF object can be loaded and have its programs executed across any kernel without the need for object modification, thus enhancing portability.
> -- [aquasecurity/btfhub](https://github.com/aquasecurity/btfhub)

### Generate BTF for GTP5G

Add the btf target in the Makefile like this:

```
diff --git a/Makefile b/Makefile
index bec4880..bab04d4 100644
--- a/Makefile
+++ b/Makefile
@@ -98,3 +98,6 @@ uninstall:
        $(DEPMOD)
        rm -f /etc/modules-load.d/gtp5g.conf
        rmmod -f  $(MODULE_NAME)
+
+btf:
+       pahole --btf_encode gtp5g.ko
+       pahole --btf_encode gtp5g.o
```

And run the commands below:

```sh
$ make
$ make btf
$ readelf -S gtp5g.ko | grep BTF
$ sudo make install
```

In this way, you will able to see the gtp5g btf by using btftool:

```sh
$ sudo bpftool btf list | grep gtp5g
410: name [gtp5g]  size 243774B
```

use the command below to dump vmlinux and gtp5g BTF to C file:
```sh
$ bpftool btf dump file /sys/kernel/btf/vmlinux format c > vmlinux/vmlinux.h
$ bpftool btf dump file /sys/kernel/btf/gtp5g format c > vmlinux/vmlinux.h
```

## Trace the function calls in GTP5G

The eBPF program type `BPF_PROG_TYPE_TRACING` are a newer alternative to kprobes and tracepoints since Linux Kernel v5.5, which provides practically zero overhead by leveraging the BPF trampoline.

The command below can be used to list all of available functions for tracing purpose:
```sh
$ sudo cat /sys/kernel/tracing/available_filter_functions | grep gtp5g
// ...
gtp5g_dbg_read [gtp5g]
proc_qos_write [gtp5g]
gtp5g_qos_read [gtp5g]
gtp5g_far_read [gtp5g]
proc_pdr_write [gtp5g]
proc_dbg_write [gtp5g]
gtp5g_pdr_read [gtp5g]
proc_qer_write [gtp5g]
proc_far_write [gtp5g]
proc_urr_write [gtp5g]
get_proc_gtp5g_dev_list_head [gtp5g]
init_proc_gtp5g_dev_list [gtp5g]
create_proc [gtp5g]
remove_proc [gtp5g]
```

If we want to trace the function entry of gtp5g_encap_recv, we can write a program like below:

```c
#include "vmlinux.h"
#include <bpf_tracing.h>
#include <bpf_helpers.h>

SEC("fentry/gtp5g_xmit_skb_ipv4")
int BPF_PROG(gtp5g_uplink, struct sk_buff *skb, struct gtp5g_pktinfo *pktinfo)
{
    __u64 pid_tgid = bpf_get_current_pid_tgid();
    __u32 pid = pid_tgid & 0xFFFFFFFF;
    __u32 tgid = pid_tgid >> 32;
    __u32 cpu = bpf_get_smp_processor_id();
    
    bpf_printk("gtp5g_xmit_skb_ipv4: PID=%u, TGID=%u, CPU=%u", pid, tgid, cpu);
    return 0;
}

char _license[] SEC("license") = "GPL";
```

- Any program with the `fentry` prefix will be executed before the execution of target function (in this case is `gtp5g_xmit_skb_ipv4()`), and can be identified as the `BPF_PROG_TYPE_TRACING` type by the kernel.
- The arguments of the `BPF_PROG` follows the kernel function you want to trace. for example:
```c
// The definition in the gtp5g, the BPF_PROG's args should be same with the target function
static int gtp5g_xmit_skb_ipv4(struct sk_buff *, struct gtp5g_pktinfo *);
```

### Load and attach eBPF program

Typically, we can load and attach the eBPF program into specific system hook by using bpftool. However, the bpftool does not support all of attachment types provided by the kernel.

Therefore, I use the [libbpfgo](github.com/aquasecurity/libbpfgo) and [libbpf](https://github.com/libbpf/libbpf) to implement the agent program for loading eBPF program:
```go
package main

import (
	"os"
	"time"

	bpf "github.com/aquasecurity/libbpfgo"
)

func main() {
	bpfModule, err := bpf.NewModuleFromFile("main.o")
	if err != nil {
		panic(err)
	}
	defer bpfModule.Close()

	if err := bpfModule.BPFLoadObject(); err != nil {
		panic(err)
	}

	prog, err := bpfModule.GetProgram("gtp5g_uplink")
	if err != nil {
		panic(err)
	}

	link, err := prog.AttachGeneric()
	if err != nil {
		panic(err)
	}
	if link.FileDescriptor() == 0 {
		os.Exit(-1)
	}

	for {
		time.Sleep(10 * time.Second)
	}
}
```

> INFO
> You will need to write a Makefile for building the BPF program and its agent.
> If you don't know how to get started, please refer to my side project: [tinyLB](https://github.com/ENSREG/tinyLB/blob/master/Makefile).

To see the output of the attached eBPF program:
```sh
sudo cat /sys/kernel/debug/tracing/trace_pipe
           <...>-236797  [009] b.s21 6141919.013036: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=236797, TGID=236797, CPU=9
          <idle>-0       [009] b.s31 6141920.013210: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=9
          <idle>-0       [009] b.s31 6141921.014070: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=9
          <idle>-0       [009] b.s31 6141922.013615: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=9
          <idle>-0       [009] b.s31 6141923.013975: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=9
          <idle>-0       [009] b.s31 6141924.014871: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=9
          <idle>-0       [009] b.s31 6141925.013730: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=9
        kubelite-3377186 [009] b.s21 6141926.013908: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=3377186, TGID=3376931, CPU=9
          <idle>-0       [009] b.s31 6141927.014084: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=9
          <idle>-0       [009] b.s31 6141928.015013: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=9
          <idle>-0       [009] b.s31 6141929.014465: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=9
          <idle>-0       [009] b.s31 6141930.014600: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=9
          <idle>-0       [009] b.s31 6141931.013976: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=9
          <idle>-0       [009] b.s31 6141932.014142: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=9
          <idle>-0       [009] b.s31 6141933.014331: bpf_trace_printk: gtp5g_xmit_skb_ipv4: PID=0, TGID=0, CPU=9
```

## Conclusion

This article shows how to troubleshoot the kernel panic by using the `decode_stacktrace.sh` script and how to trace the function calls in the kernel module by using eBPF.
The eBPF is a powerful tool for kernel debugging. It can be used to trace the function calls in the kernel module with low overhead and even make the kernel more secure by detecting critical events.


## References

- https://lwn.net/Articles/592724/
- [Make linux kernel function show in ftrace available_filter_function](https://stackoverflow.com/questions/38006485/make-linux-kernel-function-show-in-ftrace-available-filter-function)
- https://askubuntu.com/questions/1348250/skipping-btf-generation-xxx-due-to-unavailability-of-vmlinux-on-ubuntu-21-04
- https://github.com/aquasecurity/btfhub/blob/main/docs/how-to-use-pahole.md#tools-that-generate-btf-information

## About
Greetings! My name is [Ian](https://www.linkedin.com/in/ian-chen-88b70b1aa/). I'm currently a Technical Steering Committee member of the free5GC project. We're focusing on delevering a fully open-source 5G core network for academic and industry usage.
If you're interested in our project, the pull requests and issues are always welcome!
