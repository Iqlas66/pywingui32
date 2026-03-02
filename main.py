import os
import win32api
import win32gui
import win32con
import win32process

class PyWinGUI32:
    @staticmethod
    def _get_internal_owner():
        """Finds the hWnd of the process running this script."""
        current_pid = os.getpid()
        found_hwnd = [0] # Use a list to allow mutation inside the local function

        def enum_callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if pid == current_pid:
                    found_hwnd[0] = hwnd
                    return False # Found it, stop searching
            return True

        win32gui.EnumWindows(enum_callback, None)
        return found_hwnd[0]

    @classmethod
    def show_message(cls, text, title="Notification", style="info", owner=None):
        """
        Displays a native Windows message box.
        :param style: 'info', 'warn', 'error', 'question'
        :param owner: Specific hWnd. If None, it finds the script's window.
        """
        # 1. Map user-friendly strings to Win32 Constants
        styles = {
            "info": win32con.MB_ICONINFORMATION | win32con.MB_OK,
            "warn": win32con.MB_ICONWARNING | win32con.MB_OK,
            "error": win32con.MB_ICONERROR | win32con.MB_OK,
            "question": win32con.MB_ICONQUESTION | win32con.MB_YESNO
        }
        flags = styles.get(style, win32con.MB_OK)

        # 2. Automatically detect owner if not provided
        if owner is None:
            owner = cls._get_internal_owner()
            # Fallback to foreground window if no script window found (e.g. background process)
            if not owner:
                owner = win32gui.GetForegroundWindow()

        # 3. Trigger the Box
        result_code = win32api.MessageBox(owner, text, title, flags)

        # 4. Convert Win32 integer returns to friendly strings
        responses = {
            win32con.IDOK: "ok",
            win32con.IDYES: "yes",
            win32con.IDNO: "no",
            win32con.IDCANCEL: "cancel"
        }
        return responses.get(result_code, "unknown")


