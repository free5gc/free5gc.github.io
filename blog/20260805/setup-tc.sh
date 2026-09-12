#!/usr/bin/env bash
set -Eeuo pipefail

usage() {
    cat <<'USAGE'
Usage:
  sudo ./setup-tc.sh uplink baseline
  sudo ./setup-tc.sh uplink qfi
  sudo ./setup-tc.sh downlink baseline
  sudo ./setup-tc.sh downlink qfi

Arguments:
  direction
    uplink    Apply TC to the UPF N6 egress interface.
    downlink  Apply TC to the UPF N3 egress interface.

  mode
    baseline  HTB bottleneck with one shared fq_codel.
    qfi       HTB bottleneck with Default, Stable, and Normal classes.

Environment variables:
  N3_IF                 UPF N3 interface. Default: enp0s8
  N6_IF                 UPF N6 interface. Default: enp0s9
  BOTTLENECK_RATE       Per-direction HTB bottleneck. Default: 10mbit

  STABLE_MARK           Stable Flow skb mark. Default: 2
  NORMAL_MARK           Normal Flow skb mark. Default: 3

  STABLE_CLASS_RATE     Stable class guaranteed rate. Default: 5mbit
  NORMAL_CLASS_RATE     Normal class guaranteed rate. Default: 1mbit
  DEFAULT_CLASS_RATE    Default class guaranteed rate. Default: 128kbit

  FQ_LIMIT              fq_codel packet limit. Default: 10240
  FQ_FLOWS              fq_codel flow buckets. Default: 1024
  FQ_QUANTUM            fq_codel DRR quantum. Default: 1514
  FQ_TARGET             fq_codel target delay. Default: 5ms
  FQ_INTERVAL           fq_codel interval. Default: 100ms
USAGE
}

log() {
    printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"
}

fail() {
    printf '[ERROR] %s\n' "$*" >&2
    exit 1
}

require_root() {
    if (( EUID != 0 )); then
        fail "Run this script as root, for example: sudo $0 uplink baseline"
    fi
}

require_command() {
    local command_name="$1"
    command -v "${command_name}" >/dev/null 2>&1 \
        || fail "Required command not found: ${command_name}"
}

require_interface() {
    local iface="$1"
    ip link show dev "${iface}" >/dev/null 2>&1 \
        || fail "Network interface does not exist: ${iface}"
}

add_fq_codel() {
    local iface="$1"
    local parent="$2"
    local handle="$3"

    tc qdisc add dev "${iface}" parent "${parent}" handle "${handle}" fq_codel \
        limit "${FQ_LIMIT}" \
        flows "${FQ_FLOWS}" \
        quantum "${FQ_QUANTUM}" \
        target "${FQ_TARGET}" \
        interval "${FQ_INTERVAL}" \
        ecn
}

clear_existing_tc() {
    local iface="$1"

    # Deleting a missing root qdisc is expected on a clean interface.
    tc qdisc del dev "${iface}" root 2>/dev/null || true
}

apply_baseline() {
    local iface="$1"

    log "Applying baseline TC to ${iface}"

    # HTB only enforces the per-direction 10 Mbit/s bottleneck.
    # Both experiment flows share one fq_codel instance.
    tc qdisc add dev "${iface}" root handle 1: htb default 10

    tc class add dev "${iface}" parent 1: classid 1:10 htb \
        rate "${BOTTLENECK_RATE}" \
        ceil "${BOTTLENECK_RATE}"

    add_fq_codel "${iface}" 1:10 10:
}

apply_qfi() {
    local iface="$1"

    log "Applying QFI-aware TC to ${iface}"

    # Unclassified or unmatched traffic enters Default class 1:10.
    tc qdisc add dev "${iface}" root handle 1: htb default 10

    # Shared parent enforces the per-direction bottleneck.
    tc class add dev "${iface}" parent 1: classid 1:1 htb \
        rate "${BOTTLENECK_RATE}" \
        ceil "${BOTTLENECK_RATE}"

    # Default / unmatched traffic: QFI 0 or any skb mark not matched below.
    tc class add dev "${iface}" parent 1:1 classid 1:10 htb \
        rate "${DEFAULT_CLASS_RATE}" \
        ceil "${BOTTLENECK_RATE}" \
        prio 2

    # Stable Flow: QFI 2 -> skb mark 2 -> class 1:20.
    # QFI identifies the flow; the HTB class assigns the scheduling policy.
    tc class add dev "${iface}" parent 1:1 classid 1:20 htb \
        rate "${STABLE_CLASS_RATE}" \
        ceil "${BOTTLENECK_RATE}" \
        prio 0

    # Normal Flow: QFI 3 -> skb mark 3 -> class 1:30.
    tc class add dev "${iface}" parent 1:1 classid 1:30 htb \
        rate "${NORMAL_CLASS_RATE}" \
        ceil "${BOTTLENECK_RATE}" \
        prio 1

    # Identical fq_codel parameters isolate the effect of class separation,
    # guaranteed rates, and the configured HTB scheduling policy.
    add_fq_codel "${iface}" 1:10 10:
    add_fq_codel "${iface}" 1:20 20:
    add_fq_codel "${iface}" 1:30 30:

    # Filter priority controls evaluation order only; it is separate from
    # the HTB class prio values above.
    tc filter add dev "${iface}" parent 1: protocol ip \
        prio 10 handle "0x${STABLE_MARK}" fw flowid 1:20

    tc filter add dev "${iface}" parent 1: protocol ip \
        prio 20 handle "0x${NORMAL_MARK}" fw flowid 1:30
}

show_summary() {
    local iface="$1"

    echo
    echo "========== qdisc: ${iface} =========="
    tc -s qdisc show dev "${iface}"

    echo
    echo "========== class: ${iface} =========="
    tc -s class show dev "${iface}"

    echo
    echo "========== filter: ${iface} =========="
    tc -s filter show dev "${iface}" parent 1: || true
}

main() {
    if (( $# != 2 )); then
        usage >&2
        exit 2
    fi

    local direction="$1"
    local mode="$2"
    local iface

    case "${direction}" in
        uplink)   iface="${N6_IF}" ;;
        downlink) iface="${N3_IF}" ;;
        *)
            printf '[ERROR] Invalid direction: %s\n' "${direction}" >&2
            usage >&2
            exit 2
            ;;
    esac

    case "${mode}" in
        baseline|qfi) ;;
        *)
            printf '[ERROR] Invalid mode: %s\n' "${mode}" >&2
            usage >&2
            exit 2
            ;;
    esac

    require_root
    require_command tc
    require_command ip
    require_interface "${iface}"

    log "Direction=${direction} Mode=${mode} Interface=${iface} Bottleneck=${BOTTLENECK_RATE}"
    clear_existing_tc "${iface}"

    case "${mode}" in
        baseline) apply_baseline "${iface}" ;;
        qfi)      apply_qfi "${iface}" ;;
    esac

    log "TC configuration applied successfully"
    show_summary "${iface}"
}

N3_IF="${N3_IF:-enp0s8}"
N6_IF="${N6_IF:-enp0s9}"
BOTTLENECK_RATE="${BOTTLENECK_RATE:-10mbit}"

STABLE_MARK="${STABLE_MARK:-2}"
NORMAL_MARK="${NORMAL_MARK:-3}"

STABLE_CLASS_RATE="${STABLE_CLASS_RATE:-5mbit}"
NORMAL_CLASS_RATE="${NORMAL_CLASS_RATE:-1mbit}"
DEFAULT_CLASS_RATE="${DEFAULT_CLASS_RATE:-128kbit}"

FQ_LIMIT="${FQ_LIMIT:-10240}"
FQ_FLOWS="${FQ_FLOWS:-1024}"
FQ_QUANTUM="${FQ_QUANTUM:-1514}"
FQ_TARGET="${FQ_TARGET:-5ms}"
FQ_INTERVAL="${FQ_INTERVAL:-100ms}"

main "$@"
