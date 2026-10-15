import json
from .config_editor import edit_config
from .path import SETTINGS_PATH
from protocols.logging import get_logger

logger = get_logger(__name__)

# ============================================================
#load config function
# ============================================================
def load_configs():
    try:
        with open(SETTINGS_PATH, "r", encoding="utf-8") as file:
            config = json.load(file)

        return config

    except FileNotFoundError:
        logger.warning("Configuration file not found. Starting setup.")
        return edit_config()
