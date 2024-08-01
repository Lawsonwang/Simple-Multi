try:
    import os
    import json
    import threading
    import traceback
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox

    from utils.key_utils import *
    from utils.window_utils import *
    from window import *
except:
    import tkinter as tk
    import tkinter.messagebox as tkMessageBox
    tk.Tk().withdraw()
    print('Error during imports.')
    tkMessageBox.showerror('Error', 'Error during imports. Dependencies missing?')


_VERSION = '1.0.0'

DEFAULT_CONFIG = {
    'atum_key': 'F6',
    'reset_key': 'U',
    'resetall_key': 'T',
}


def resource_path(relative_path):
    try:
        from sys import _MEIPASS
        base_path = _MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class MainApp(tk.Tk):
    LOOP_MSPT = 500

    def __init__(self):
        super().__init__()

        self.title(f'SimpleMulti v{_VERSION}')
        self.resizable(False, False)

        self.iconbitmap(resource_path('SimpleMulti_Icon.ico'))

        self._changing = False
        self._active = False
        self._active_button_var: tk.StringVar = tk.StringVar(self, value='Start Resetting')

        self._info_var: tk.StringVar = tk.StringVar(self, value=f'SimpleMulti v{_VERSION}\nby Lawson563')

        self._total_var: tk.StringVar = tk.StringVar(self, value='Current Instances:\n0')
        self._atum_key_var: tk.StringVar = tk.StringVar(self, value='Atum Reset Key:\n...')
        self._reset_key_var: tk.StringVar = tk.StringVar(self, value='Reset Key:\n...')
        self._resetall_key_var: tk.StringVar = tk.StringVar(self, value='Reset All Key:\n...')

        self._init_widgets()

        self._config = self._load_config()
        self._handle_config()

        self._current = -1
        self._hwnd_self = None

        self._windows = []

        self.after(0, self._loop)

    def _loop(self):
        threading.Thread(target=self._loop_thread).start()

    def _loop_thread(self):
        try:
            if self._active and self._current == -1:
                fgh = get_current_hwnd()
                for i in range(len(self._windows)):
                    if self._windows[i]._hwnd == fgh:
                        self._current = i
                        break
                if self._current != -1:
                    self._windows[self._current].active()
        except:
            error = traceback.format_exc()
            print(error)
            tkMessageBox.showerror("Error during eventloop", "Error during eventloop:\n" + error)
        self.after(self.LOOP_MSPT, self._loop)

    def _init_widgets(self) -> None:
        # Control pannel
        control_frame = tk.LabelFrame(self, text='Control')
        control_frame.grid(row=0, column=0, padx=10, pady=5, sticky='N')

        self._detect_button = tk.Button(control_frame, text='Detect Instances', command=self._detect_instances)
        self._detect_button.grid(row=0, column=0, padx=10, pady=5, sticky='NESW')
        self._start_button = tk.Button(control_frame, textvariable=self._active_button_var, command=self._toggle_status)
        self._start_button.grid(row=1, column=0, padx=10, pady=5, sticky='NESW')
        tk.Label(control_frame, textvariable=self._total_var).grid(row=2, column=0, padx=10, pady=5, sticky='NESW')

        tk.Label(self, textvariable=self._info_var).grid(row=1, column=0)

        config_frame = tk.LabelFrame(self, text='Config')
        config_frame.grid(row=0, column=1, rowspan=2, padx=10, pady=5, sticky='N')

        self._atum_key_button = tk.Button(config_frame, textvariable=self._atum_key_var, command=self._set_atum_key_button)
        self._atum_key_button.grid(row=0, column=0, padx=10, pady=5, sticky='NESW')
        self._reset_key_button = tk.Button(config_frame, textvariable=self._reset_key_var, command=self._set_reset_key_button)
        self._reset_key_button.grid(row=1, column=0, padx=10, pady=5, sticky='NESW')
        self._resetall_key_button = tk.Button(config_frame, textvariable=self._resetall_key_var, command=self._set_resetall_key_button)
        self._resetall_key_button.grid(row=2, column=0, padx=10, pady=5, sticky='NESW')

    def _detect_instances(self):
        try:
            self._windows = get_all_mc_windows()
            self._total_var.set(f'Current Instances:\n{len(self._windows)}')
            if len(self._windows) == 0:
                tkMessageBox.showwarning('No instances found', 'Found no Minecraft instances open.')
            else:
                pass
        except:
            error = traceback.format_exc()
            print(error)
            tkMessageBox.showerror("Error during setup", "Error during setup:\n" + error)

    def _toggle_status(self):
        self._hwnd_self = get_current_hwnd()
        if self._active:
            self._active_button_var.set('Start Resetting')
            self._atum_key_button.config(state=tk.NORMAL)
            self._reset_key_button.config(state=tk.NORMAL)
            self._resetall_key_button.config(state=tk.NORMAL)
            self._detect_button.config(state=tk.NORMAL)
            if self._current != -1:
                self._windows[self._current].resume()
                activate_hwnd(self._hwnd_self, False)
            self._current = -1
            self._active = False
            self._info_var.set('')
        else:
            self._active_button_var.set('Stop Resetting')
            self._atum_key_button.config(state=tk.DISABLED)
            self._reset_key_button.config(state=tk.DISABLED)
            self._resetall_key_button.config(state=tk.DISABLED)
            self._detect_button.config(state=tk.DISABLED)
            self._active = True
            self._info_var.set('Running...')

    def _handle_config(self):
        # Hotkeys
        stop_hotkey_checker()

        self._atum_key = self._get_config('atum_key')
        self._reset_key = self._get_config('reset_key')
        self._resetall_key = self._get_config('resetall_key')

        # Register hotkeys
        register_hotkey(self._atum_key, self._on_atum_keypress)
        register_hotkey(self._reset_key, self._on_reset_keypress)
        register_hotkey(self._resetall_key, self._on_resetall_keypress)

        self._atum_key_var.set('Atum Reset Key:\n' + self._atum_key)
        self._reset_key_var.set('Reset Key:\n' + self._reset_key)
        self._resetall_key_var.set('Reset All Key:\n' + self._resetall_key)

        start_hotkey_checker()

        self._save_config(self._config)

    def _check_key_conflict(self, cfg_id: str, key: str):
        for each in DEFAULT_CONFIG:
            if each == cfg_id:
                continue
            if self._get_config(each) == key:
                return True
        return False

    def _set_key_thread(self, var: tk.StringVar, var_text: str, cfg_id: str):
        if self._changing:
            return
        self._changing = True
        self._info_var.set('Setting hotkey...\nPress ESC to cancel.')
        self._detect_button.config(state=tk.DISABLED)
        self._start_button.config(state=tk.DISABLED)
        stop_hotkey_checker()

        var.set(var_text + ':\n...')
        key: str = wait_keypress()
        if self._check_key_conflict(cfg_id, key):
            tkMessageBox.showwarning('Key conflict!', f'"{key}" conflict with other keys.')
        elif key.lower().find('escape') == -1:
            self._config[cfg_id] = key

        self._handle_config()
        self._detect_button.config(state=tk.NORMAL)
        self._start_button.config(state=tk.NORMAL)
        self._info_var.set('')
        self._changing = False

    _set_atum_key_button = lambda self: threading.Thread(target=self._set_key_thread, args=(self._atum_key_var, 'Atum Reset Key', 'atum_key')).start()
    _set_reset_key_button = lambda self: threading.Thread(target=self._set_key_thread, args=(self._reset_key_var, 'Reset Key', 'reset_key')).start()
    _set_resetall_key_button = lambda self: threading.Thread(target=self._set_key_thread, args=(self._resetall_key_var, 'Reset All Key', 'resetall_key')).start()

    def _on_atum_keypress(self):
        if not self._active or self._current == -1:
            return
        self._windows[self._current].resume()
        activate_hwnd(self._hwnd_self, False)
        self._current = -1

    def _on_reset_keypress(self):
        if not self._active or self._current == -1:
            return
        self._windows[self._current].reset_world()
        self._windows[self._current].resume()
        activate_hwnd(self._hwnd_self, False)
        self._current = -1

    def _on_resetall_keypress(self):
        if not self._active or self._current != -1:
            return
        for win in self._windows:
            win.reset_world()

    def _get_config(self, key: str):
        return self._config.get(key, DEFAULT_CONFIG.get(key))

    def _load_config(self) -> dict | None:
        try:
            if not os.path.isfile('config.json'):
                return {}
            config = {}
            with open('config.json', 'r') as f:
                config = json.load(f)
            return config
        except:
            return {}

    def _save_config(self, config: dict) -> None:
        with open('config.json', 'w') as f:
            json.dump(config, f)


def main():
    try:
        app = MainApp()
        app.mainloop()
        stop_hotkey_checker()
    except KeyboardInterrupt:
        pass
    except Exception:
        error = traceback.format_exc()
        print(error)
        tkMessageBox.showerror("Error", error)

if __name__ == '__main__':
    main()