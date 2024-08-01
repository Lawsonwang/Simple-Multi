import time
import win32api
import global_hotkeys
from global_hotkeys.keycodes import vk_key_names

MODIFIER_KEYS = ["left_control", "right_control", "left_shift", "right_shift", "left_menu", "right_menu"]
BASIC_MODIFIER_KEYS = ["control", "shift", "alt"]


def _get_nm_keys():
    nm_keys = []
    for key in vk_key_names.keys():
        if key not in MODIFIER_KEYS and key not in BASIC_MODIFIER_KEYS:
            nm_keys.append(key)
    return nm_keys


NM_KEYS = _get_nm_keys()


def is_pressed(key: str) -> bool:
    if key == 'window':
        return False  # lol
    return win32api.GetAsyncKeyState(vk_key_names[key]) < 0


def wait_keypress() -> str:
    while True:
        time.sleep(0.01)
        for nm_key in NM_KEYS:
            if not is_pressed(nm_key):
                continue
            result = []
            for md_key in BASIC_MODIFIER_KEYS:
                if not is_pressed(md_key):
                    continue
                result.append(md_key)
            result.append(nm_key)
            return ' + '.join(map(str.title, result))


start_hotkey_checker = global_hotkeys.start_checking_hotkeys
register_hotkey = lambda hotkey, callback: global_hotkeys.register_hotkey(hotkey, callback, None)


def stop_hotkey_checker():
    global_hotkeys.stop_checking_hotkeys()
    global_hotkeys.clear_hotkeys()
