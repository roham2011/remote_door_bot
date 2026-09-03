from flask import Flask, request , jsonify
from config.config import APP_PORT, MAIN_ROUTE,TEST_DUE_ROUTE, DEBUG,HOST, webhook_url ,TOKEN, NUM_OF_DOORS
from utils.set_webhook import set_webh
from database.database import sessionLocal
from core.handle_commands import handle_command
from protocols.logging import get_logger , separator_log


# ============================================================
# Logger
# ============================================================
logger = get_logger(__name__)


# ============================================================
# Flask Application
# ============================================================
app = Flask(__name__)


# ============================================================
# Webhook
# ============================================================
set_webh(webhook_url)


# ============================================================
# Main Webhook Route
# ============================================================
@app.route(MAIN_ROUTE, methods=["POST"])
def main_webhook():

    update = request.get_json(silent=True) or {}

    update_id = update.get("update_id")

    text = None
    bale_user_id = None
    first_name = None


    # --------------------------------------------------------
    # Message Update
    # --------------------------------------------------------
    if "message" in update:

        message = update["message"]

        text = message.get("text")

        user = message.get("from", {})

        bale_user_id = user.get("id")

        first_name = user.get("first_name")


    # --------------------------------------------------------
    # Callback Query Update
    # --------------------------------------------------------
    elif "callback_query" in update:

        callback_query = update["callback_query"]

        text = callback_query.get("data")

        user = callback_query.get("from", {})

        bale_user_id = user.get("id")

        first_name = user.get("first_name")


    # --------------------------------------------------------
    # Invalid Update
    # -------------------------------------------------------
    if text is None or bale_user_id is None:

        logger.warning("Invalid update received | update_id=%s",update_id)

        return "ok"


    # ========================================================
    # Update Log
    # ========================================================
    separator_log(logger,f"UPDATE {update_id}",state=True)

    logger.info("Text: %s", text)
    logger.info("Bale User ID: %s", bale_user_id)
    logger.info("Name: %s", first_name)


    # ========================================================
    # Command Handling
    # =======================================================
    with sessionLocal() as session:

        try:

            logger.info("Handling update | update_id=%s",update_id)

            handle_command(session=session,text=text,user_id=bale_user_id,first_name=first_name)

            logger.info("Update handled successfully | update_id=%s",update_id)


        except Exception:

            logger.exception("Error while handling update | update_id=%s",update_id)


    # ========================================================
    # End Update
    # ========================================================
    logger.info("Finished update | update_id=%s",update_id)

    separator_log(logger,state=False)

    return "App_OK", 200


# ============================================================
# Test Route
# ============================================================

@app.route(TEST_DUE_ROUTE, methods=["POST"])
def test_webhook():
    body_update = request.get_json(silent=True)
    logger.info("TEST ROUTE REACHED")
    logger.info("Raw body: %s", request.data)
    logger.info("JSON body: %s",body_update)

    return jsonify({"connected": True}), 200


# ============================================================
# Application Startup
# ============================================================
if __name__ == "__main__":

    separator_log( logger, "Configuration loaded", state=True )

    logger.info("Port = %s", APP_PORT)
    logger.info("Host = %s", HOST)
    logger.info("Number of Doors = %s", NUM_OF_DOORS)
    logger.info("Debug = %s", DEBUG)
    separator_log(logger)

    logger.info("Starting Flask application")
    separator_log(logger)

    app.run(host=HOST,port=APP_PORT,debug=DEBUG)

