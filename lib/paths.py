import os

import json

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PACKAGE_DIR, "data")
LOCALES_DIR = os.path.join(DATA_DIR, "locales")
USEFUL_PATH = os.path.join(DATA_DIR, "useful_system.json")
def _user_home():
    override = os.environ.get("CMD_HOME")
    if override:
        return os.path.expanduser(override)
    return os.path.join(os.path.expanduser("~"), ".cmd")


USER_DIR = _user_home()
_LEGACY_DIR = os.path.join(os.path.expanduser("~"), ".findcmd")

# Legacy fallbacks (ru)
ESSENTIAL_PATH = os.path.join(DATA_DIR, "essential.json")
CATEGORIES_PATH = os.path.join(DATA_DIR, "categories.json")
INDEX_PATH = os.path.join(USER_DIR, "index.json")
CUSTOM_PATH = os.path.join(USER_DIR, "custom.json")
HISTORY_PATH = os.path.join(USER_DIR, "history.json")
CONFIG_PATH = os.path.join(USER_DIR, "config.json")


def locale_data_path(filename, locale="ru"):
    path = os.path.join(LOCALES_DIR, locale, filename)
    if os.path.exists(path):
        return path
    if locale != "en":
        en_path = os.path.join(LOCALES_DIR, "en", filename)
        if os.path.exists(en_path):
            return en_path
    legacy = os.path.join(DATA_DIR, filename)
    return legacy if os.path.exists(legacy) else path


def ensure_user_dir():
    if not os.path.exists(USER_DIR) and os.path.isdir(_LEGACY_DIR):
        os.rename(_LEGACY_DIR, USER_DIR)
    os.makedirs(USER_DIR, exist_ok=True)