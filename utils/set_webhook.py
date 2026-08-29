import requests
from config import TOKEN , URL

def set_webh(webhook):
    return requests.post(URL, data={"url": webhook})