import socket
import json
from config.settings import CONFIG


def send_data(data: dict):
    s = socket.socket()
    s.connect((CONFIG["peer_ip"], CONFIG["port"]))
    s.send(json.dumps(data).encode())
    s.close()


# transfer_file_ai/network_module/socket_server.py
import socket
import threading
import json
from clipboard_module.copy_paste import ClipboardManager
from config.settings import CONFIG


def handle_client(conn):
    data = conn.recv(CONFIG["file_buffer_size"])
    msg = json.loads(data.decode())
    clip = ClipboardManager()
    if msg["type"] == "text":
        clip.paste_text(msg["data"])
    elif msg["type"] == "image":
        clip.paste_image(msg["data"])
    conn.close()


def start_server():
    s = socket.socket()
    s.bind(("", CONFIG["port"]))
    s.listen(5)
    print(f"[LISTENING] on port {CONFIG['port']}")

    while True:
        conn, _ = s.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

