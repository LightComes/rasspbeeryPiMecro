#!/usr/bin/env python3
import dbus
import dbus.mainloop.glib
from gi.repository import GLib
import os
import time

TARGET_MAC = ""  # XX:XX:XX:XX:XX:XX

def property_changed(interface, changed, invalidated, path):
    if "Connected" in changed:
        connected = changed["Connected"]
        device_mac = path.split("/")[-1].replace("dev_", "").replace("_", ":")
        print("변경")

        # 타겟맥 등록 안했으면 ㄱㅊ
        if TARGET_MAC and device_mac != TARGET_MAC:
            return

        if connected:
            print(f"[+] Device Connected: {device_mac}")
            os.system("/usr/local/bin/on_bt_connected.sh")
        else:
            print(f"[-] Device Disconnected: {device_mac}")
            os.system("/usr/local/bin/on_bt_disconnected.sh")

def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()

    bus.add_signal_receiver(
        property_changed,
        dbus_interface="org.freedesktop.DBus.Properties",
        signal_name="PropertiesChanged",
        path_keyword="path"
    )

    loop = GLib.MainLoop()
    loop.run()

if __name__ == "__main__":
    main()
    time.sleep(5)
    os.system("/home/dsd2115/rasspbeeryPiMecro/macro/pass_throug.sh")
