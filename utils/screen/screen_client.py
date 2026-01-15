from typing import Optional

import win32gui
import numpy as np
import mss

class ScreenClient:
    def __init__(self):
        pass

    def find_window_by_title(self, title_keyword: str) -> Optional[int]:
        """Find a window handle by matching a keyword in the window title.
        returns the window handle if found, otherwise None.
        """
        matched_hwnd = None
        def enum_handler(hwnd, _):
            nonlocal matched_hwnd
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title_keyword.lower() in title.lower():
                    matched_hwnd = hwnd
        win32gui.EnumWindows(enum_handler, None)
        return matched_hwnd
    
    def get_all_window_titles(self) -> list[str]:
        """Get a list of all visible window titles.
        returns a list of window titles.
        """
        titles = []
        def enum_handler(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    titles.append((title, hwnd))
        win32gui.EnumWindows(enum_handler, None)
        return titles
    
    def find_window_by_title_strict(self, exact_title: str) -> Optional[int]:
        """Find a window handle by exact matching the window title.
        returns the window handle if found, otherwise None.
        """
        for each_title, hwnd in self.get_all_window_titles():
            if each_title == exact_title:
                return hwnd
        return None

    def get_window_rect(self, hwnd: int) -> tuple[int, int, int, int]:
        """Get the rectangle (left, top, right, bottom) of the specified window handle.
        returns a tuple of (left, top, right, bottom) if the window exists, otherwise None.
        """
        if hwnd and win32gui.IsWindow(hwnd):
            return win32gui.GetWindowRect(hwnd)
        return None

    def bring_window_to_front(self, hwnd: int) -> bool:
        """Bring the specified window to the front.
        returns True if successful, otherwise False.
        """
        if hwnd and win32gui.IsWindow(hwnd):
            win32gui.SetForegroundWindow(hwnd)
            return True
        return False
    
    def get_window_title(self, hwnd: int) -> Optional[str]:
        """Get the title of the specified window handle.
        returns the window title if the window exists, otherwise None.
        """
        if hwnd and win32gui.IsWindow(hwnd):
            return win32gui.GetWindowText(hwnd)
        return None
    
    def list_all_windows(self) -> list[tuple[int, str]]:
        """List all visible windows with their handles and titles.
        returns a list of tuples containing (hwnd, title).
        """
        windows = []
        def enum_handler(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                windows.append((hwnd, title))
        win32gui.EnumWindows(enum_handler, None)
        return windows

    def get_screenshot(self, hwnd: int) -> np.ndarray:
        """Capture a screenshot by hwnd.
        """
        with mss.mss() as sct:
            if hwnd and win32gui.IsWindow(hwnd):
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                monitor = {"top": top, "left": left, "width": right - left, "height": bottom - top}
            else:
                monitor = sct.monitors[1]  # Primary monitor
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            return img
        
    def get_full_screenshot(self) -> np.ndarray:
        """Capture a full screenshot of the primary monitor.
        """
        print("Capturing full screenshot of the primary monitor.")
        with mss.mss() as sct:
            monitor = sct.monitors[0]  # Primary monitor
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            return img