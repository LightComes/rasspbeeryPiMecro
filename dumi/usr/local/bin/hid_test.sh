#!/bin/bash
# hid_test.sh - send "test" via /dev/hidg0

HID_DEVICE="/dev/hidg0"

send_key() {
    local key="$1"
    local mod=0
    local code=0

    case "$key" in
        a) code=0x04 ;;
        b) code=0x05 ;;
        c) code=0x06 ;;
        d) code=0x07 ;;
        e) code=0x08 ;;
        f) code=0x09 ;;
        g) code=0x0a ;;
        h) code=0x0b ;;
        i) code=0x0c ;;
        j) code=0x0d ;;
        k) code=0x0e ;;
        l) code=0x0f ;;
        m) code=0x10 ;;
        n) code=0x11 ;;
        o) code=0x12 ;;
        p) code=0x13 ;;
        q) code=0x14 ;;
        r) code=0x15 ;;
        s) code=0x16 ;;
        t) code=0x17 ;;
        u) code=0x18 ;;
        v) code=0x19 ;;
        w) code=0x1a ;;
        x) code=0x1b ;;
        y) code=0x1c ;;
        z) code=0x1d ;;
        " ") code=0x2c ;; # space
        *) echo "Unknown key: $key" >&2; return ;;
    esac

    # Key down
    printf "\\x$(printf '%02x' $mod)\\x00\\x$(printf '%02x' $code)\\x00\\x00\\x00\\x00\\x00" | sudo tee $HID_DEVICE > /dev/null
    sleep 0.05
    # Key up
    printf "\x00\x00\x00\x00\x00\x00\x00\x00" | sudo tee $HID_DEVICE > /dev/null
    sleep 0.05
}

# 실제로 "test" 전송
for k in t e s t; do
    send_key "$k"
done

# 마지막에 엔터 입력 (원하면)
# printf "\x00\x00\x28\x00\x00\x00\x00\x00" | sudo tee $HID_DEVICE > /dev/null

