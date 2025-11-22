import os
import time
import random

DEVICE = "/dev/hidg0"

# HID 키코드 매핑 (표준 Keyboard/Keypad Page)
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
    'KEY_LEFTCTRL': 0x01, 'KEY_LEFTSHIFT': 0x02, 'KEY_LEFTALT': 0x04, 'KEY_LEFTMETA': 0x08,
    'KEY_RIGHTCTRL': 0x10, 'KEY_RIGHTSHIFT': 0x20, 'KEY_RIGHTALT': 0x40, 'KEY_RIGHTMETA': 0x80,
}


# 현재 눌려있는 상태 추적
active_modifiers = 0
active_keys = set()

# 랜덤 지연 (ms)
def sleep_random(base_ms=100, randomMin = 100, randomMax = 100):
    base_ms  = base_ms / 1000
    delay_ms = random.randint(randomMin, randomMax) / 1000
    time.sleep((base_ms + delay_ms))

# HID 보고
def send_report(report):
    with open(DEVICE, "wb") as fd:
        fd.write(bytearray(report))


def build_report():
    """현재 상태 기반으로 HID report 생성"""
    report = [active_modifiers, 0]
    keys = list(active_keys)[:6]  # 동시에 6키까지 가능
    report += keys + [0] * (6 - len(keys))
    return report

# 키 누르기
def key_down(key, basetime = 100, randomMin = 100, randomMax = 100):
    global active_modifiers, active_keys
    
    sleep_random(basetime, randomMin, randomMax)

    if key in ['KEY_LEFTCTRL', 'KEY_LEFTALT', 'KEY_LEFTSHIFT']:
        active_modifiers |= KEY_MAP[key]
    elif key in KEY_MAP:
        active_keys.add(KEY_MAP[key])
    else:
        print(f"⚠️ Unknown key: {key}")
        return

    send_report(build_report())
    

# 키 떼기
def key_up(key, basetime = 100, randomMin = 100, randomMax = 100):
    global active_modifiers, active_keys
    
    sleep_random(basetime, randomMin, randomMax)

    if key in ['KEY_LEFTCTRL', 'KEY_LEFTALT', 'KEY_LEFTSHIFT']:
        active_modifiers &= ~KEY_MAP[key]
    elif key in KEY_MAP:
        active_keys.discard(KEY_MAP[key])
    else:
        print(f"⚠️ Unknown key: {key}")
        return

    send_report(build_report())

# 키 클릭(down, up)
def key_click(key, basetime = 100, randomMin = 100, randomMax = 100):
    key_down(key, basetime, randomMin, randomMax);
    key_up(key, basetime, randomMin, randomMax);

# 전체 초기화 (모든 키 떼기)
def release_all():
    global active_modifiers, active_keys
    active_modifiers = 0
    active_keys.clear()
    send_report([0x00] * 8)
    sleep_random()

# 문자열 입력
def type_text(text):
    for ch in text:
        if ch == " ":
            key_down("SPACE")
        else:
            key_down(ch)
        key_up(ch)
    release_all()
