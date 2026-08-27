from pathlib import Path 
APP_PORT = 5000

TEST_ROUTE = "/test" 
MAIN_ROUTE = "/main"

DEBUG = True

HOST = "127.0.0.1"

TOKEN = "1796130842:u0sYHYixJ_7fS2ra6lOvySNzw3WD9EA3CJ4"
URL = f"https://tapi.bale.ai/bot{TOKEN}/setWebhook"

# import URL from tunneled Host
TUNNEL_URL_FILE = Path("runtime/tunnel_url.txt")

if TUNNEL_URL_FILE.exists():
    Global_URL = TUNNEL_URL_FILE.read_text().strip()
else:
    Global_URL = ""

Webhook_URL= f"{Global_URL}{MAIN_ROUTE}"