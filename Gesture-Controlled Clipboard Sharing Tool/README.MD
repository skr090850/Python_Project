# 🖐️ Gesture-Controlled Clipboard Sharing Tool 📋

This project enables seamless sharing of clipboard content (text and images) between two devices on a local network using intuitive hand gestures. It combines real-time hand detection with network communication to provide a unique and efficient way to transfer data.

---

## ✨ Features

* **Gesture-Controlled Copy**: Use a specific hand gesture to trigger a copy action on the source device.
* **Network-Based Transfer**: Securely send copied text or images over your local network to a peer device.
* **Automatic Paste**: Automatically paste the received content into the clipboard of the destination device.
* **Cross-Platform Compatibility**: Designed to work across different operating systems (requires Python and specific libraries).

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed on both your source and destination devices:

* **Python 3.x**
* **pip** (Python package installer)
* **Webcam** (for gesture detection on the source device)

---

## 🚀 Setup

Follow these steps to get the project up and running on both your source and destination machines.

### 1. Project Files

Place all the provided Python and JSON files (`copy_paste.py`, `settings.json`, `settings.py`, `detect.py`, `keyboard_mouse.py`, `socket_client.py`, `socket_server.py`, `transfer.py`, `helpers.py`, `config.json`) into a single directory on both devices.

### 2. Install Dependencies

Open your terminal or command prompt and navigate to the project directory. Then, install the required Python libraries:

```bash
pip install opencv-python mediapipe pyautogui keyboard pyperclip
```

### 3. Configure Network Settings

Edit the `config.json` file in your project directory on **both** devices:

```json
{
  "this_device_ip": "YOUR_DEVICE_IP",
  "peer_device_ip": "PEER_DEVICE_IP",
  "port": 9999
}
```

* Replace `"YOUR_DEVICE_IP"` with the actual IP address of the device you are currently configuring.
* Replace `"PEER_DEVICE_IP"` with the IP address of the other device on your network.
* `"port"`: You can keep the default `9999` or choose another available port. Ensure it's the same on both devices.

**Example:**
If Device A has IP `192.168.1.100` and Device B has IP `192.168.1.101`:

**`config.json` on Device A:**
```json
{
  "this_device_ip": "192.168.1.100",
  "peer_device_ip": "192.168.1.101",
  "port": 9999
}
```

**`config.json` on Device B:**
```json
{
  "this_device_ip": "192.168.1.101",
  "peer_device_ip": "192.168.1.100",
  "port": 9999
}
```

---

## 🚀 Usage

### 1. Start the Receiver (Destination Device)

On the device that will *receive* the clipboard content, run the server script:

```bash
python socket_server.py
```
You should see output similar to `[Receiver Ready] Listening on port 9999`.

### 2. Start the Gesture Detector (Source Device)

On the device that will *send* the clipboard content (the one with the webcam), you'll need to integrate the `detect.py` with `socket_client.py` and `keyboard_mouse.py` to trigger the copy and send actions. A simple way to test this would be to create a main script (e.g., `main.py`) that orchestrates these actions.

To run the gesture detection and sending functionality, you would typically create a main script (e.g., `main.py`) that imports and orchestrates the `HandGestureDetector`, `ClipboardManager`, `simulate_copy`, and `send_to_peer` functions. This script would continuously monitor for the "closed hand" gesture, trigger a copy, fetch the clipboard data, and send it to the configured peer.

### 3. Perform a Gesture to Copy and Send

On the source device, ensure your webcam is active and you are visible. Perform the "closed hand" gesture in front of the camera. The script will detect the gesture, simulate a `Ctrl+C` (copy) command, read the clipboard, and send the content to the peer device.

On the destination device, you should see messages indicating that data has been received and pasted.

---

## 📂 File Structure

* `config.json`: Network configuration settings.
* `settings.py`: Loads configuration from `settings.json`.
* `copy_paste.py`: Handles clipboard read/write operations.
* `detect.py`: Detects hand gestures using OpenCV and MediaPipe.
* `keyboard_mouse.py`: Simulates keyboard shortcuts (e.g., Ctrl+C, Ctrl+V).
* `socket_client.py`: Client-side network communication (sends data).
* `socket_server.py`: Server-side network communication (receives data).
* `transfer.py`: Contains both client and server logic for data transfer.
* `helpers.py`: Utility functions (e.g., checking data type, saving temporary files).

---

## ⚠️ Troubleshooting

* **Firewall Issues**: Ensure your firewall is not blocking the chosen `port` (e.g., `9999`). You might need to create an inbound/outbound rule for this port.
* **IP Address Mismatch**: Double-check that the `this_device_ip` and `peer_device_ip` in `config.json` are correct and that both devices are on the same local network.
* **Dependencies Not Found**: If you get `ModuleNotFoundError`, make sure all dependencies are installed using `pip install ...` as mentioned in the setup.
* **Webcam Access**: Ensure your webcam is not being used by another application and that your system grants Python access to the camera.
* **`pyautogui` Permissions**: On some systems (especially macOS), `pyautogui` might require accessibility permissions to simulate keyboard/mouse actions.
* **Image Transfer**: The current `socket_server.py` and `copy_paste.py` have `paste_image` which implies image handling. However, sending image data over JSON requires converting it to a base64 string first. For actual image transfer, you'd need to implement base64 encoding/decoding.

---
