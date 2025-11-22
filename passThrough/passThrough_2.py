import sys
import os
import atexit

# 현재 파일의 디렉토리를 기준으로 상위 디렉토리 경로를 계산하여 추가
current_file_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_file_dir)
sys.path.append(parent_dir)

# 이제 상대 경로 `..` 대신 절대 경로처럼 임포트할 수 있습니다.
# from ..common.common import release_all  <-- 이 줄은 주석 처리하거나 삭제
from common.common import release_all 

import evdev
from evdev import ecodes

#종료 시 동작 정의
def exit_print():
    print('프로그램이 종료됩니다!')
    release_all()

#종료 레지스터 등록    
atexit.register(exit_print)    

DEVICE_PATH = '/dev/input/event2'
HID_PATH = '/dev/hidg0'

KEY_MAP = {
    # 알파벳
    'KEY_A': 0x04, 'KEY_B': 0x05, 'KEY_C': 0x06, 'KEY_D': 0x07, 'KEY_E': 0x08,
    'KEY_F': 0x09, 'KEY_G': 0x0A, 'KEY_H': 0x0B, 'KEY_I': 0x0C, 'KEY_J': 0x0D,
    'KEY_K': 0x0E, 'KEY_L': 0x0F, 'KEY_M': 0x10, 'KEY_N': 0x11, 'KEY_O': 0x12,
    'KEY_P': 0x13, 'KEY_Q': 0x14, 'KEY_R': 0x15, 'KEY_S': 0x16, 'KEY_T': 0x17,
    'KEY_U': 0x18, 'KEY_V': 0x19, 'KEY_W': 0x1A, 'KEY_X': 0x1B, 'KEY_Y': 0x1C,
    'KEY_Z': 0x1D,

    # 숫자 및 기호
    'KEY_1': 0x1E, 'KEY_2': 0x1F, 'KEY_3': 0x20, 'KEY_4': 0x21, 'KEY_5': 0x22,
    'KEY_6': 0x23, 'KEY_7': 0x24, 'KEY_8': 0x25, 'KEY_9': 0x26, 'KEY_0': 0x27,
    'KEY_MINUS': 0x2D, 'KEY_EQUAL': 0x2E,
    'KEY_LEFTBRACE': 0x2F, 'KEY_RIGHTBRACE': 0x30,
    'KEY_BACKSLASH': 0x31, 'KEY_SEMICOLON': 0x33,
    'KEY_APOSTROPHE': 0x34, 'KEY_GRAVE': 0x35,
    'KEY_COMMA': 0x36, 'KEY_DOT': 0x37, 'KEY_SLASH': 0x38,

    # 기능 키
    'KEY_ENTER': 0x28, 'KEY_ESC': 0x29, 'KEY_BACKSPACE': 0x2A, 'KEY_TAB': 0x2B,
    'KEY_SPACE': 0x2C, 'KEY_CAPSLOCK': 0x39,

    # F1~F12
    'KEY_F1': 0x3A, 'KEY_F2': 0x3B, 'KEY_F3': 0x3C, 'KEY_F4': 0x3D,
    'KEY_F5': 0x3E, 'KEY_F6': 0x3F, 'KEY_F7': 0x40, 'KEY_F8': 0x41,
    'KEY_F9': 0x42, 'KEY_F10': 0x43, 'KEY_F11': 0x44, 'KEY_F12': 0x45,

    # 방향키
    'KEY_RIGHT': 0x4F, 'KEY_LEFT': 0x50, 'KEY_DOWN': 0x51, 'KEY_UP': 0x52,

    # 탐색 키
    'KEY_INSERT': 0x49, 'KEY_HOME': 0x4A, 'KEY_PAGEUP': 0x4B,
    'KEY_DELETE': 0x4C, 'KEY_END': 0x4D, 'KEY_PAGEDOWN': 0x4E,

    # 숫자패드
    'KEY_NUMLOCK': 0x53,
    'KEY_KPSLASH': 0x54, 'KEY_KPASTERISK': 0x55, 'KEY_KPMINUS': 0x56,
    'KEY_KPPLUS': 0x57, 'KEY_KPENTER': 0x58, 'KEY_KP1': 0x59, 'KEY_KP2': 0x5A,
    'KEY_KP3': 0x5B, 'KEY_KP4': 0x5C, 'KEY_KP5': 0x5D, 'KEY_KP6': 0x5E,
    'KEY_KP7': 0x5F, 'KEY_KP8': 0x60, 'KEY_KP9': 0x61, 'KEY_KP0': 0x62,
    'KEY_KPDOT': 0x63,

    # 한/영, 한자
    'KEY_HANGUEL': 0x90,
    'KEY_HANJA': 0x91,

    # 수정키
    'KEY_LEFTCTRL': 0xE0, 'KEY_LEFTSHIFT': 0xE1, 'KEY_LEFTALT': 0xE2,
    'KEY_LEFTMETA': 0xE3, 'KEY_RIGHTCTRL': 0xE4, 'KEY_RIGHTSHIFT': 0xE5,
    'KEY_RIGHTALT': 0xE6, 'KEY_RIGHTMETA': 0xE7,
}

# 제조사 특이 키 → F키로 재매핑
CUSTOM_FKEY_MAP = {
    'KEY_BRIGHTNESSDOWN': 'KEY_F1',
    'KEY_BRIGHTNESSUP': 'KEY_F2',
    'KEY_SCALE': 'KEY_F3',
    'KEY_ALL_APPLICATIONS': 'KEY_F4',
    'KEY_KBDILLUMDOWN': 'KEY_F5',
    'KEY_KBDILLUMUP': 'KEY_F6',
    'KEY_PREVIOUSSONG': 'KEY_F7',
    'KEY_PLAYPAUSE': 'KEY_F8',
    'KEY_NEXTSONG': 'KEY_F9',
    'KEY_MIN_INTERESTING': 'KEY_F10',
    'KEY_VOLUMEDOWN': 'KEY_F11',
    'KEY_VOLUMEUP': 'KEY_F12',
}

device = evdev.InputDevice(DEVICE_PATH)
if "DURGOD" in device.name :
    MODIFIER_KEYS = {
        'KEY_LEFTCTRL': 0x01, 'KEY_LEFTSHIFT': 0x02, 'KEY_LEFTMETA': 0x04, 'KEY_LEFTALT': 0x08,
        'KEY_RIGHTCTRL': 0x10, 'KEY_RIGHTSHIFT': 0x20, 'KEY_RIGHTALT': 0x80, 'KEY_RIGHTMETA': 0x40,
    }
else :
    MODIFIER_KEYS = {
        'KEY_LEFTCTRL': 0x01, 'KEY_LEFTSHIFT': 0x02, 'KEY_LEFTALT': 0x04, 'KEY_LEFTMETA': 0x08,
        'KEY_RIGHTCTRL': 0x10, 'KEY_RIGHTSHIFT': 0x20, 'KEY_RIGHTALT': 0x40, 'KEY_RIGHTMETA': 0x80,
    }

pressed_keys = set()
pressed_modifiers = 0

def send_hid_report():
    report = bytearray(8)
    report[0] = pressed_modifiers
    keys = list(pressed_keys)[:6]
    for i, key in enumerate(keys):
        report[2 + i] = KEY_MAP.get(key, 0)
    with open(HID_PATH, 'wb') as fd:
        fd.write(report)

def listen_for_events():
    global pressed_modifiers
    device = evdev.InputDevice(DEVICE_PATH)
    print(f"Listening on {device.name} ({DEVICE_PATH})")

    for event in device.read_loop():
        if event.type != ecodes.EV_KEY:
            continue

        key = evdev.categorize(event)
        keycode = key.keycode if isinstance(key.keycode, str) else key.keycode[0]

        # 제조사 커스텀 F키 매핑 보정
        if keycode in CUSTOM_FKEY_MAP:
            keycode = CUSTOM_FKEY_MAP[keycode]

        if keycode not in KEY_MAP:
            print(f"[INFO] Unknown key detected: {keycode}")
            continue

        if key.keystate == key.key_down:
            if keycode in MODIFIER_KEYS:
                pressed_modifiers |= MODIFIER_KEYS[keycode]
            else:
                pressed_keys.add(keycode)
        elif key.keystate == key.key_up:
            if keycode in MODIFIER_KEYS:
                pressed_modifiers &= ~MODIFIER_KEYS[keycode]
            else:
                pressed_keys.discard(keycode)

        send_hid_report()

if __name__ == "__main__":
    listen_for_events()
