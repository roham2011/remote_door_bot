import requests
from config import TOKEN , SET_WEBHOOK_URL

def set_webh(webhook):
    return requests.post(SET_WEBHOOK_URL, data={"url": webhook})