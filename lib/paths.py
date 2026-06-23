import os

PACKAGE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PACKAGE_DIR, "data")
USEFUL_PATH = os.path.join(DATA_DIR, "useful_system.json")
USER_DIR = os.path.join(os.path.expanduser("~"), ".findcmd")

ESSENTIAL_PATH = os.path.join(DATA_DIR, "essential.json")
CATEGORIES_PATH = os.path.join(DATA_DIR, "categories.json")
INDEX_PATH = os.path.join(USER_DIR, "index.json")
CUSTOM_PATH = os.path.join(USER_DIR, "custom.json")
HISTORY_PATH = os.path.join(USER_DIR, "history.json")


def ensure_user_dir():
    os.makedirs(USER_DIR, exist_ok=True)