from flask import Flask , request
from config import APP_PORT , MAIN_ROUTE ,TEST_ROUTE , DEBUG , HOST , Webhook_URL
from utils.set_webhook import set_webh
from database.database import sessionLocal
from core.handle_commands import handle_command

app = Flask(__name__)

set_webh(Webhook_URL)

@app.route(MAIN_ROUTE,methods=["POST"])
def test ():
    update = request.get_json(silent=True) or {}
    update_id = update["update_id"]
    
    text = None
    bale_user_id = None
    first_name = None


    if "message" in update:
        text = update["message"].get("text")
        bale_user_id = update["message"]["from"]["id"]
        first_name = update["message"]["from"].get("first_name")
    
    if "callback_query" in update:
        text = update["callback_query"].get("data")
        bale_user_id = update["callback_query"]["from"]["id"]
        first_name = update["callback_query"]["from"].get("first_name")

    if text is None or bale_user_id is None:
        return "ok"
    
    print ("\n\n","-"*20,f"[update_id={update_id}]","-"*20)
    print ("text:",text)
    print ("bale_user_id:",bale_user_id)
    print ("Name:",first_name)

    with sessionLocal() as session : 
        try:
            handle_command(session = session , text = text, user_id = bale_user_id, first_name = first_name)
        except Exception as Error :
            print(Error)

    return "App_OK", 200

@app.route(TEST_ROUTE)
def test_webhook(name: str):
    """Test route."""
    return f"Hello {name}, webhook is OK!"


if __name__ == "__main__":
   app.run(host=HOST, port=APP_PORT, debug=DEBUG)