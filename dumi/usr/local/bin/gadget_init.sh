#!/bin/bash
set -e

# USB HID Keyboard Gadget Setup
G=/sys/kernel/config/usb_gadget/keyboard

# 필요한 모듈 로드
sudo modprobe libcomposite

# 가젯 디렉터리 생성
sudo mkdir -p $G
cd $G

# USB 장치 정보 설정
echo 0x1d6b | sudo tee idVendor      # Linux Foundation
echo 0x0104 | sudo tee idProduct     # HID Keyboard

# 문자열 정보
sudo mkdir -p strings/0x409
echo "fedcba9876543210" | sudo tee strings/0x409/serialnumber
echo "Raspberry Pi" | sudo tee strings/0x409/manufacturer
echo "F104Pro Dongle" | sudo tee strings/0x409/product

# HID Function 설정
sudo mkdir -p functions/hid.usb0
echo 1 | sudo tee functions/hid.usb0/protocol
echo 1 | sudo tee functions/hid.usb0/subclass
echo 8 | sudo tee functions/hid.usb0/report_length

# HID Report Descriptor (키보드)
echo -ne \
'\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x03\x95\x05\x75\x01\x05\x08\x19\x01\x29\x05\x91\x02\x95\x01\x75\x03\x91\x03\x95\x06\x75\x08\x15\x00\x25\x65\x05\x07\x19\x00\x29\x65\x81\x00\xc0' \
| sudo tee functions/hid.usb0/report_desc > /dev/null

# Config 설정
sudo mkdir -p configs/c.1/strings/0x409
echo "Config 1: HID Keyboard" | sudo tee configs/c.1/strings/0x409/configuration

# Function 연결
sudo ln -s functions/hid.usb0 configs/c.1/

# USB 컨트롤러 활성화
echo 3f980000.usb | sudo tee UDC
