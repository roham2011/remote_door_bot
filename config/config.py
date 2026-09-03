from pathlib import Path 
from .config_loader import load_configs
from .config_editor import edit_config

#====================
#settings
#====================
SETTINGS_PATH = Path("settings.json")

config = load_configs(SETTINGS_PATH) 

APP_PORT = config["app_port"] 
DEBUG = config["debug"] 
HOST = config["host"] 
TOKEN = config["token"] 
NUM_OF_DOORS = config["num_of_doors"]


#====================
#Flask routs
#====================
TEST_DUE_ROUTE = "/due/test" 
MAIN_ROUTE = "/main"


#====================
#Tunnels and URL(s)
#====================
SET_WEBHOOK_URL = f"https://tapi.bale.ai/bot{TOKEN}/setWebhook"

SEND_MESSAGE_URL = f"https://tapi.bale.ai/bot{TOKEN}/sendMessage"

# import URL from tunneled Host
TUNNEL_URL_FILE = Path("runtime/tunnel_url.txt")

if TUNNEL_URL_FILE.exists():
    Tunnel_URL = TUNNEL_URL_FILE.read_text().strip()
else:
    Tunnel_URL = ""


webhook_url= f"{Tunnel_URL}{MAIN_ROUTE}"


#====================
#database location
#====================
DATABASE_URL = "sqlite:///database/RAG.db"

#====================
#if this file was run
#====================
if __name__ == "__main__":
    edit_config(SETTINGS_PATH)