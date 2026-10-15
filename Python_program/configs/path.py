from pathlib import Path

# Resolve project paths independently of the process working directory.
APP_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = APP_DIR.parent
RUNTIME_DIR = ROOT_DIR / "runtime"
SETTINGS_PATH = APP_DIR / "settings.json"
