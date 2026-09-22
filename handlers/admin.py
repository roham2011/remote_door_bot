import json
from configs.config_loader import load_configs
from configs.general_config import SETTINGS_PATH
from protocols.logging import get_logger

logger = get_logger(__name__)

def add_admin(user_id: int) -> bool:
    config = load_configs(SETTINGS_PATH)

    try:
        if user_id in config["admins"]:
            return False

        config["admins"].append(user_id)

        with open (SETTINGS_PATH , "w") as file:
            json.dump(config , file , indent=4)
            return True
        
    except Exception as e :
        logger.error(e)
        return False