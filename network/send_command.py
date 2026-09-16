from config.config import ARDUINO_IP , ARDUINO_PORT
import requests

def send_command(command):


    url = f"http://{ARDUINO_IP}:{ARDUINO_PORT}/api/v1/command"

    payload = command

    try:
        response = requests.post(url,json=payload,timeout=3)
        return response 
    except requests.RequestException as error:
        print("Request failed:", error)