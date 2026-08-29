import requests
from config import URL

def post_message (payload):

    print("Sending payload:")
    print(payload)

    response = requests.post(
        url=URL,
        json=payload
    )

    print("Bale Status Code:", response.status_code)
    print("Bale Response:")
    print(response.text)

    return response 
    