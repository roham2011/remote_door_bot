import requests
from configs.general_config import SEND_MESSAGE_URL
from protocols.logging import get_logger

logger = get_logger(__name__)

def post_message(payload):
    """Send a message to the Bale Bot API.

    Args:
        payload: Message payload containing chat ID, text,
            and optional reply markup.

    Returns:
        The HTTP response returned by the Bale API.

    Raises:
        requests.RequestException: If the API request fails.
    """

    chat_id = payload.get("chat_id")
    text = payload.get("text")
    reply_markup = payload.get("reply_markup")

    # ========================================================
    # Sending message
    # ========================================================
    logger.debug("Sending message | chat_id=%s",chat_id)

    logger.debug("Message text | %s",text)

    if reply_markup:
        logger.debug("Reply markup | %s",reply_markup)

    # ========================================================
    # HTTP request
    # ========================================================
    try:
        response = requests.post(SEND_MESSAGE_URL,json=payload)

    except requests.RequestException:
        logger.exception("Failed to connect to Bale API | chat_id=%s", chat_id)

        raise

    # ========================================================
    # Response
    # ========================================================
    logger.debug("Bale API response | status=%s",response.status_code)

    try:
        data = response.json()

    except ValueError:
        logger.error("Bale API returned invalid JSON | status=%s",response.status_code)

        return response

    # ========================================================
    # Result
    # ========================================================
    if data.get("ok"):
        result = data.get("result", {})

        message_id = result.get("message_id")

        logger.debug("Message sent successfully | chat_id=%s | message_id=%s",chat_id,message_id)

    else:
        logger.error("Bale API request failed | status=%s | response=%s",response.status_code,data)

    return response