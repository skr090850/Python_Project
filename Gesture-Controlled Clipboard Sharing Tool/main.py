import socket
import threading
import json
import os
import base64
import pyperclip
import pyautogui
import cv2
import mediapipe as mp
import subprocess
import time
import shutil
import win32clipboard
import win32con
import win32gui

# 🔧 Load config
with open("config.json", "r") as f:
    CONFIG = json.load(f)

PORT = CONFIG["port"]
PEER_IP = CONFIG["peer_device_ip"]
THIS_IP = CONFIG["this_device_ip"]
FALLBACK_FOLDER = "D:/Data_Transfer_AI"
os.makedirs(FALLBACK_FOLDER, exist_ok=True)

incoming_data = None

# ✋ Hand Gesture Detection
class HandGestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                tips = [8, 12, 16, 20]
                fingers = [hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y for tip in tips]
                return "open" if all(fingers) else "closed"
        return None

# 🧠 Clipboard: detect and encode content
def capture_clipboard():
    win32clipboard.OpenClipboard()
    if win32clipboard.IsClipboardFormatAvailable(win32con.CF_HDROP):  # Files
        files = win32clipboard.GetClipboardData(win32con.CF_HDROP)
        win32clipboard.CloseClipboard()
        payload_files = []
        for path in files:
            if os.path.isfile(path):
                with open(path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode()
                payload_files.append({
                    "filename": os.path.basename(path),
                    "data": encoded
                })
        return {"type": "files", "files": payload_files}

    win32clipboard.CloseClipboard()

    text = pyperclip.paste()
    if text.strip():
        return {"type": "text", "data": text}

    return None

# 📤 Send encoded data over socket
def send_data(payload):
    try:
        s = socket.socket()
        s.connect((PEER_IP, PORT))
        s.sendall(json.dumps(payload).encode())
        s.close()
        print("[✓] Sent data to peer.")
    except Exception as e:
        print("[X] Send failed:", e)

# 📥 Receive and prepare paste
def save_received_data(data):
    global incoming_data
    incoming_data = data
    print(f"[📨] Received data of type: {data['type']} — awaiting paste gesture...")

def get_focused_folder():
    hwnd = win32gui.GetForegroundWindow()
    length = win32gui.GetWindowTextLength(hwnd)
    title = win32gui.GetWindowText(hwnd)
    if "File Explorer" in title or "\\" in title:
        return title
    return None

# 🖨️ Paste and open received content
def perform_paste():
    global incoming_data
    if not incoming_data:
        print("[!] No data to paste.")
        return

    folder_path = get_focused_folder()
    if not folder_path or not os.path.exists(folder_path):
        folder_path = FALLBACK_FOLDER
        print(f"[→] No folder open. Using default: {folder_path}")

    data_type = incoming_data.get("type")

    if data_type == "text":
        subprocess.Popen(["notepad.exe"])
        time.sleep(1)
        pyperclip.copy(incoming_data["data"])
        pyautogui.hotkey("ctrl", "v")
        print("[📝] Text pasted to Notepad.")

    elif data_type == "files":
        for file in incoming_data["files"]:
            filename = file.get("filename", "file.unknown")
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "wb") as f:
                f.write(base64.b64decode(file["data"]))
            os.startfile(filepath)
            print(f"[📁] File saved and opened: {filename}")

    incoming_data = None

# 🌐 Listener for peer data
def socket_listener():
    s = socket.socket()
    s.bind((THIS_IP, PORT))
    s.listen(5)
    print(f"[🔌] Listening on {THIS_IP}:{PORT} ...")
    while True:
        client, addr = s.accept()
        data = b""
        while True:
            chunk = client.recv(1024 * 1024)
            if not chunk:
                break
            data += chunk
        try:
            payload = json.loads(data.decode())
            save_received_data(payload)
        except:
            print("[!] Received invalid data.")
        client.close()

# 🖐 Gesture → trigger copy or paste
def monitor_gestures():
    detector = HandGestureDetector()
    cap = cv2.VideoCapture(0)
    prev = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gesture = detector.detect(frame)
        if gesture != prev:
            print(f"[🖐] Gesture: {prev} ➝ {gesture}")
            if prev == "open" and gesture == "closed":
                pyautogui.hotkey("ctrl", "a")
                pyautogui.hotkey("ctrl", "c")
                time.sleep(0.5)
                payload = capture_clipboard()
                if payload:
                    print("[📤] Sending clipboard content...")
                    send_data(payload)
                else:
                    print("[!] Nothing to send.")

            elif prev == "closed" and gesture == "open":
                print("[📥] Performing paste...")
                perform_paste()

            prev = gesture

        cv2.imshow("Gesture", frame)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# ▶️ Entry Point
if __name__ == "__main__":
    threading.Thread(target=socket_listener, daemon=True).start()
    monitor_gestures()
