from flask import Flask , request
from core.config import PORT , MAIN_ROUTE ,TEST_ROUTE , DEBUG , HOST , Webhook_URL
from api.set_webhook import set_webh

app = Flask(__name__)

set_webh(Webhook_URL)

@app.route(MAIN_ROUTE,methods=["POST"])
def test ():
    update = request.get_json(silent=True) or {}

@app.route(TEST_ROUTE)
def test_webhook(name: str):
    """Test route."""
    return f"Hello {name}, webhook is OK!"


if __name__ == "__main__":
   app.run(host=HOST, port=PORT, debug=DEBUG)