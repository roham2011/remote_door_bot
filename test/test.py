import requests
import threading


def send_command():
    ARDUINO_IP = "192.168.0.120"
    ARDUINO_PORT = 8080

    url = f"http://{ARDUINO_IP}:{ARDUINO_PORT}/api/v1/command"

    payload = {
        "command": "open"
    }

    try:
        requests.post(
            url,
            json=payload,
            timeout=3
        )
    except requests.RequestException as error:
        print("Request failed:", error)


def test_http_server():
    thread = threading.Thread(
        target=send_command,
        daemon=True
    )

    thread.start()

    print("Command sent.")
