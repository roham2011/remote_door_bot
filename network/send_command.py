from configs.general_config import ARDUINO_IP , ARDUINO_PORT
import requests

def send_command(command):
    """this function sends http request to Arduino Path and returns Arduino response 

    Args:
        command (dict): it is a own command send

    Returns:
        dict: the arduino response
    """

    url = f"http://{ARDUINO_IP}:{ARDUINO_PORT}/api/v1/command"

    payload = command

    try:
        response = requests.post(url,json=payload,timeout=3)
        return response 
    except requests.RequestException as error:
        print("Request failed:", error)