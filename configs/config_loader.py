import json
from .config_editor import edit_config
from configs.path import SETTINGS_PATH
from protocols.logging import get_logger

logger = get_logger(__name__)

# ============================================================
#load config function
# ============================================================
def load_configs():

    try:
        with open(SETTINGS_PATH, "r") as file:
            config = json.load(file)

        return config

    except FileNotFoundError:

        logger.warning("Configuration file not found.")

        return False
