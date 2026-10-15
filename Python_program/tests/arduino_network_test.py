from network.send_command import send_command
from protocols.commands import Commands
from protocols.logging import get_logger , separator_log
import json
logger = get_logger(__name__)

def test_http_server():
    response = send_command(Commands.TEST)

    separator_log(logger=logger , text = "Test Command sent!" , level = 2)

    if response is not None:
        try:
            data = response.json()
            logger.debug("Response Status Code: %s",response.status_code)
            logger.debug("Response Body: %s",response.text)
            if "test" in data:
                logger.debug("First step is True!")
            elif "flask_test" in data["test"]:
                logger.debug("Response True!")
            else :
                logger.debug("Response not True!")

        except ValueError:
            logger.error("Response is not valid JSON!")
            logger.error("Response body: %s", response.text)
            return





    
