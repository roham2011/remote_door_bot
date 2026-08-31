import requests
from config.config import SET_WEBHOOK_URL

def set_webh(webhook):
    return requests.post(SET_WEBHOOK_URL, data={"url": webhook})