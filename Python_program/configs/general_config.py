from .path import RUNTIME_DIR
from .config_loader import load_configs
from .config_editor import edit_config
from pathlib import Path
from .path import ROOT_DIR

#====================
#settings
#====================


config = load_configs() 

if config is False :
    config = edit_config()
    
APP_PORT = config["app_port"] 
DEBUG = config["debug"] 
HOST = config["host"] 
TOKEN = config["token"] 
NUM_OF_DOORS = config["num_of_doors"]
ORIGIN_ADMIN = config["admins"][0]


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
TUNNEL_URL_FILE = RUNTIME_DIR / "tunnel_url.txt"

if TUNNEL_URL_FILE.exists():
    Tunnel_URL = TUNNEL_URL_FILE.read_text().strip()
else:
    Tunnel_URL = ""


webhook_url= f"{Tunnel_URL}{MAIN_ROUTE}"


#====================
#database location
#====================
DATABASE_DIR = ROOT_DIR / "database"
DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{(DATABASE_DIR / 'Remote_Door_DB.db').as_posix()}"

#====================
#arduino server
#====================
ARDUINO_IP = "192.168.0.120"
ARDUINO_PORT = 8080

#====================
#if this file was run
#====================
if __name__ == "__main__":
    edit_config()