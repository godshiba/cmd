import json
import os

from .paths import CONFIG_PATH, LOCALES_DIR, ensure_user_dir

SUPPORTED = ("en", "ru", "zh")
ALIASES = {
    "en": "en",
    "en_us": "en",
    "en_gb": "en",
    "ru": "ru",
    "ru_ru": "ru",
    "zh": "zh",
    "zh_cn": "zh",
    "zh_tw": "zh",
    "zh_hans": "zh",
}

_current_locale = None
_ui_cache = {}


def _normalize(code):
    if not code:
        return None
    key = code.strip().lower().replace("-", "_")
    if key in ALIASES:
        return ALIASES[key]
    base = key.split("_", 1)[0]
    return ALIASES.get(base)


def _read_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def _write_config(data):
    ensure_user_dir()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def detect_locale():
    env = os.environ.get("CMD_LANG") or os.environ.get("CMD_LOCALE")
    if loc := _normalize(env):
        return loc
    cfg = _read_config()
    if loc := _normalize(cfg.get("lang")):
        return loc
    for var in ("LC_ALL", "LC_MESSAGES", "LANG"):
        if loc := _normalize(os.environ.get(var, "").split(".", 1)[0]):
            if loc in SUPPORTED:
                return loc
    return "en"


def get_locale():
    global _current_locale
    env = os.environ.get("CMD_LANG") or os.environ.get("CMD_LOCALE")
    if env_loc := _normalize(env):
        if _current_locale != env_loc:
            _current_locale = env_loc
            _ui_cache.clear()
            from .lookup import clear_caches

            clear_caches()
        return env_loc

    detected = detect_locale()
    if _current_locale != detected:
        _current_locale = detected
        _ui_cache.clear()
        from .lookup import clear_caches

        clear_caches()
    return _current_locale


def set_locale(code):
    global _current_locale, _ui_cache
    loc = _normalize(code)
    if loc not in SUPPORTED:
        raise ValueError(f"Unsupported locale: {code}")
    cfg = _read_config()
    cfg["lang"] = loc
    _write_config(cfg)
    _current_locale = loc
    _ui_cache.clear()
    from .lookup import clear_caches

    clear_caches()
    return loc


def locale_path(locale, filename):
    return os.path.join(LOCALES_DIR, locale, filename)


def load_ui(locale=None):
    locale = locale or get_locale()
    if locale in _ui_cache:
        return _ui_cache[locale]
    path = locale_path(locale, "ui.json")
    fallback = locale_path("en", "ui.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    elif os.path.exists(fallback):
        with open(fallback, encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    _ui_cache[locale] = data
    return data


def t(key, **kwargs):
    ui = load_ui()
    text = ui.get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text


def tier_labels():
    ui = load_ui()
    return ui.get("tiers", {})


def tier_icons():
    return {"essential": "⭐", "recent": "🕐", "useful": "✦", "system": "💻"}


def language_choices():
    return [
        ("en", "English"),
        ("ru", "Русский"),
        ("zh", "中文"),
    ]