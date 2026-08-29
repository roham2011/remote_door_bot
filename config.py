from pathlib import Path 
import json

with open("settings.json", "r") as file:
    config = json.load(file)

    APP_PORT = config["app_port"]

    TOKEN = config["token"]

    DEBUG = config["debug"]

    HOST = config["host"]

TEST_ROUTE = "/test" 
MAIN_ROUTE = "/main"

URL = f"https://tapi.bale.ai/bot{TOKEN}/setWebhook"

# import URL from tunneled Host
TUNNEL_URL_FILE = Path("runtime/tunnel_url.txt")

if TUNNEL_URL_FILE.exists():
    Tunnel_URL = TUNNEL_URL_FILE.read_text().strip()
else:
    Tunnel_URL = ""

# database location
DATABASE_URL = "sqlite:///database/RAG.db"

Webhook_URL= f"{Tunnel_URL}{MAIN_ROUTE}"

if __name__ == "__main__":

    print ("="*70,f"\nURL   = {Webhook_URL}\nToken = {TOKEN}\nPort  = {APP_PORT}\nHost  = {HOST}\n","="*70 , sep = "")
    state = input("you want to reconfig this? [Y]es [N]o : ").upper()

    if state == "Y" :
        # PORT
        APP_PORT = int(input("select flask-port: "))

        # DEBUG
        debug_choice = input("select debug state [1]True [2]False: ").split()

        if debug_choice == "1":
            DEBUG = True
        elif debug_choice == "2":
            DEBUG = False
        else :
            print("invalid debug select!")

        # TOKEN
        TOKEN = str(input("select token: "))
        URL = f"https://tapi.bale.ai/bot{TOKEN}/setWebhook"

        with open("settings.json", "w") as file :
            # write log for config
            config = {
                "app_port": APP_PORT,
                "debug": DEBUG,
                "host": HOST,
                "token": TOKEN
            }
    
            json.dump(config, file, indent = 4)

    elif state == "N" :
        print("OK , no change")

    else :
        print("invalid choice!")