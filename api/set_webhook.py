import requests
from core.config import TOKEN , URL



def set_webh(webhook):
    return requests.post(URL, data={"url": webhook})