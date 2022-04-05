#
import os
import ctypes
from ctypes.wintypes import BOOL, HWND, LPARAM
import pygame.display

class States:
    def __init__(self, states):
        for state in states:
            setattr(self, state, states[state])

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, item, value):
        setattr(self, item, value)

    def set(self, item):
        for attribute in vars(self):
            if attribute == item:
                self[attribute] = True
            else:
                self[attribute] = False

class WindowManager:
    user32 = ctypes.WinDLL('User32.dll', use_last_error=True)
    states = States({state: False for state in ['windowed', 'fullscreen', 'wallpaper']})
    states.set('windowed')
    worker_hwnd = None
    game_hwnd = None
    old_wallpaper = None
    old_screensize = pygame.display.get_window_size()

    def __new__(cls, *args, **kwargs):
        if cls is WindowManager:
            raise TypeError(f"Do not instantiate '{cls.__name__}'. Just use the class name.")

    @staticmethod
    def init(hwnd):
        WindowManager.game_hwnd = hwnd
        WindowManager.store_wallpaper()

    @staticmethod
    @ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)
    def get_worker(hwnd, _):
        if WindowManager.user32.FindWindowExW(hwnd, None, "SHELLDLL_DefView", None):
            child_hwnd = ctypes.windll.user32.FindWindowExW(None, hwnd, "WorkerW", None)
            if child_hwnd not in [None, 0]:
                WindowManager.worker_hwnd = child_hwnd
                return False
        return True

    @staticmethod
    def move_window(x, y, width, height, repaint=True):
        WindowManager.user32.MoveWindow(WindowManager.game_hwnd, x, y, width, height, repaint)

    @staticmethod
    def set_fullscreen():
        desktop_size = pygame.display.get_desktop_sizes()[0]
        screen = pygame.display.set_mode(desktop_size, flags=pygame.NOFRAME)
        WindowManager.move_window(0, 0, desktop_size[0], desktop_size[1])
        WindowManager.states.set('fullscreen')
        return screen

    @staticmethod
    def set_windowed():
        desktop_size = pygame.display.get_desktop_sizes()[0]
        x = desktop_size[0] // 2 - WindowManager.old_screensize[0] // 2
        y = desktop_size[1] // 2 - WindowManager.old_screensize[1] // 2
        screen = pygame.display.set_mode(WindowManager.old_screensize)
        WindowManager.move_window(x, y, WindowManager.old_screensize[0], WindowManager.old_screensize[1])
        WindowManager.states.set('windowed')
        return screen

    @staticmethod
    def toggle_fullscreen():
        if not WindowManager.states['fullscreen']:
            screen = WindowManager.set_fullscreen()
        else:
            screen = WindowManager.set_windowed()
        return screen

    @staticmethod
    def store_wallpaper():
        if os.name == 'nt':
            path = ctypes.create_unicode_buffer(512)
            WindowManager.user32.SystemParametersInfoW(0x0073, len(path), path, 0)
            WindowManager.old_wallpaper = path.value

    @staticmethod
    def set_wallpaper():
        progman = ctypes.windll.user32.FindWindowW('Progman', None)
        WindowManager.user32.SendMessageW(progman, 0x052C, 0xD, 0)
        WindowManager.user32.SendMessageW(progman, 0x052C, 0xD, 1)
        WindowManager.user32.EnumWindows(WindowManager.get_worker)
        if WindowManager.game_hwnd and WindowManager.worker_hwnd:
            screen = WindowManager.set_fullscreen()
            WindowManager.user32.SetParent(WindowManager.game_hwnd, WindowManager.worker_hwnd)
            WindowManager.states.set('wallpaper')
            return screen
        else:
            raise Exception("Failed to get progman/worker")

    @staticmethod
    def toggle_wallpaper():
        if os.name == 'nt':
            if not WindowManager.states['wallpaper']:
                screen = WindowManager.set_wallpaper()
                return screen
            else:
                WindowManager.restore_window()
        else:
            raise Exception("Only supported on Windows.")

    @staticmethod
    def quit():
        if WindowManager.old_wallpaper:
            WindowManager.user32.SystemParametersInfoW(0x0014, 0, WindowManager.old_wallpaper, 2)
        if WindowManager.states['wallpaper']:
            WindowManager.restore_window()

    @staticmethod
    def restore_window():
        # Might not work if window already closed
        WindowManager.user32.SetParent(WindowManager.game_hwnd, None)
        WindowManager.states.set('fullscreen')




