import json
import os
from datetime import datetime, timezone

from .paths import HISTORY_PATH, ensure_user_dir


def _load():
    ensure_user_dir()
    if not os.path.exists(HISTORY_PATH):
        return {}
    with open(HISTORY_PATH, encoding="utf-8") as f:
        return json.load(f)


def _save(data):
    ensure_user_dir()
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def record(name: str):
    data = _load()
    key = name.lower()
    entry = data.get(key, {"count": 0, "last": None})
    entry["count"] = entry.get("count", 0) + 1
    entry["last"] = datetime.now(timezone.utc).isoformat()
    data[key] = entry
    _save(data)


def recent(limit=20):
    data = _load()
    items = sorted(
        data.items(),
        key=lambda x: (x[1].get("count", 0), x[1].get("last") or ""),
        reverse=True,
    )
    return [name for name, _ in items[:limit]]