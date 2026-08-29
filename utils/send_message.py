import requests
from config import SEND_MESSAGE_URL

def post_message (payload):

    print("Sending payload:")
    print(payload)

    response = requests.post(
        SEND_MESSAGE_URL,
        json=payload
    )

    print("Bale Status Code:", response.status_code)
    print("Bale Response:")
    print(response.text)

    return response 
    