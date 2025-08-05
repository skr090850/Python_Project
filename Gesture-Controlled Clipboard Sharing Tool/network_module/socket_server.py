# transfer_file_ai/network_module/socket_server.py

import socket
import json
from clipboard_module.copy_paste import ClipboardManager
from config.settings import CONFIG

def start_server():
    server = socket.socket()
    server.bind(('', CONFIG["port"]))
    server.listen(1)
    print(f"[Receiver Ready] Listening on port {CONFIG['port']}")

    clipboard = ClipboardManager()

    while True:
        client, addr = server.accept()
        print(f"[Connection] From {addr}")
        data = client.recv(10240).decode()
        client.close()

        try:
            parsed = json.loads(data)
            if parsed["type"] == "text":
                clipboard.paste_text(parsed["data"])
                print("[Pasted Text] Successfully pasted received text.")

            elif parsed["type"] == "image":
                clipboard.paste_image(parsed["data"])
                print("[Pasted Image] Successfully opened received image.")
        except Exception as e:
            print(f"[Error] Invalid data received: {e}")
