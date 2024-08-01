import re
import time
from typing import List
import win32api
import win32con
import win32gui
import win32process
from win32com import client

shell = client.Dispatch("WScript.Shell")


def get_current_hwnd() -> int:
    return win32gui.GetForegroundWindow()


def get_hwnd_title(hwnd: int) -> str:
    return win32gui.GetWindowText(hwnd)


def _win_enum_handler(hwnd: int, hwnd_list: List[str]) -> None:
    hwnd_list.insert(0, hwnd)


def get_all_hwnds() -> List[int]:
    hwnd_list = []
    win32gui.EnumWindows(_win_enum_handler, hwnd_list)
    return hwnd_list


def get_all_mc_hwnds() -> List[int]:
    hwnds = []
    mc_match = re.compile(r"^Minecraft\*? 1\.[1-9]\d*(\.[1-9]\d*)?( .*)?$").match
    for hwnd in get_all_hwnds():
        if mc_match(get_hwnd_title(hwnd)):
            hwnds.append(hwnd)
    return hwnds


def activate_hwnd(hwnd: int, maximize: bool) -> None:
    global shell
    shell.SendKeys('%')
    win32gui.ShowWindow(hwnd, 5 - 2 * maximize)
    win32gui.SetForegroundWindow(hwnd)


def move_hwnd(hwnd: int, x: int, y: int, w: int, h: int):
    # win32gui.SetWindowPos(hwnd, None, x, y, w, h, 0)
    win32gui.MoveWindow(hwnd, x, y, w, h, True)


def get_pid_from_hwnd(hwnd: int) -> int:
    return win32process.GetWindowThreadProcessId(hwnd)[1]


def _vk2sc(vk: int):
    sc = win32api.MapVirtualKey(vk, 0)
    return sc


def create_lparam(vk: int, repeat_count: int, trans_state: bool, prev_key_state: bool, context_code: bool):
    sc = _vk2sc(vk)
    return (trans_state << 31) | (prev_key_state << 30) | (context_code << 29) | (sc << 16) | (repeat_count)


def create_lp_keydown(vk: int):
    return create_lparam(vk, 1, False, False, False)


def create_lp_keyup(vk: int):
    return create_lparam(vk, 1, True, True, False)


def send_keydown(hwnd: int, vk: int) -> None:
    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, vk, create_lp_keydown(vk))


def send_keyup(hwnd: int, vk: int) -> None:
    win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, vk, create_lp_keyup(vk))


def send_key(hwnd: int, keycode: int) -> None:
    send_keydown(hwnd, keycode)
    send_keyup(hwnd, keycode)


def get_window_rect(hwnd: int):
    return win32gui.GetWindowRect(hwnd)
