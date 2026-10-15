import requests
from configs.general_config import SET_WEBHOOK_URL

def set_webh(webhook):
    try:
        response = requests.post(
            SET_WEBHOOK_URL,
            data={"url": webhook},
            timeout=10,
        )

        print("Webhook URL:", webhook)
        print("HTTP Status:", response.status_code)
        print("Bale Response:", response.text)

        response.raise_for_status()
        return response

    except requests.RequestException as error:
        print("Webhook registration failed:", error)
        return None
