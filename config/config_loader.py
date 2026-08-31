import json
from .config_editor import edit_config

# ============================================================
#load config function
# ============================================================
def load_configs(settings_path):

    try:
        with open(settings_path, "r") as file:
            config = json.load(file)

        return config

    except FileNotFoundError:

        print("Configuration file not found.")

        config = edit_config(settings_path)
