from typing import List
import time
import win32con
import win32gui
import utils.window_utils as win_util


class Window:
    def __init__(self, hwnd):
        self._hwnd = hwnd
        self._rect = win_util.get_window_rect(hwnd)
        win32gui.SetWindowPlacement(self._hwnd, (2, -1, (-1, -1), (-1, -1), self._rect))

    def reset_world(self):
        win_util.send_key(self._hwnd, win32con.VK_F6)

    def active(self):
        win_util.activate_hwnd(self._hwnd, True)

    def resume(self):
        win32gui.ShowWindow(self._hwnd, 4)
        # time.sleep(0.2)
        # win_util.move_hwnd(self._hwnd, self._rect[0], self._rect[1], self._rect[2] - self._rect[0], self._rect[3] - self._rect[1])

    def __eq__(self, value: object) -> bool:
        return self._hwnd == value._hwnd


def get_all_mc_windows() -> List[Window]:
    hwnds = win_util.get_all_mc_hwnds()
    windows = []
    for hwnd in hwnds:
        window = Window(hwnd)
        windows.append(window)
    return windows


def get_current_window() -> Window:
    return Window(win_util.get_current_hwnd())