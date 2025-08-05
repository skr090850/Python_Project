import socket
import json
from config.settings import CONFIG

def send_to_peer(data):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((CONFIG['peer_ip'], CONFIG['port']))
            s.sendall(json.dumps(data).encode('utf-8'))
    except Exception as e:
        print(f"[ERROR] Sending data failed: {e}")

