import pyperclip

class ClipboardManager:
    @staticmethod
    def get_clipboard_data():
        try:
            return pyperclip.paste()
        except Exception as e:
            print(f"[ERROR] Reading clipboard: {e}")
            return ""

    @staticmethod
    def set_clipboard_data(data):
        try:
            pyperclip.copy(data)
            print("[Clipboard] Data set successfully.")
        except Exception as e:
            print(f"[ERROR] Writing clipboard: {e}")
