from pathlib import Path 
PORT = 5000

TEST_ROUTE = "/test" 
MAIN_ROUTE = "/main"

DEBUG = True

HOST = "127.0.0.1"

# import URL from tunneled Host
TUNNEL_URL_FILE = Path("runtime/tunnel_url.txt")

if TUNNEL_URL_FILE.exists():
    Global_URL = TUNNEL_URL_FILE.read_text().strip()
else:
    Global_URL = ""

Webhook_URL= f"{Global_URL}{MAIN_ROUTE}"