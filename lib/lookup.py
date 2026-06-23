import json
import os
import re
import subprocess

from .paths import (
    CATEGORIES_PATH,
    CUSTOM_PATH,
    DATA_DIR,
    ESSENTIAL_PATH,
    INDEX_PATH,
)
from .index import load_index

TIER_ORDER = {"essential": 0, "recent": 1, "useful": 2, "system": 3}


def _load_json(path, default=None):
    if default is None:
        default = {}
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_categories():
    return _load_json(CATEGORIES_PATH)


def load_essential():
    return _load_json(ESSENTIAL_PATH, default=[])


def load_custom():
    data = _load_json(CUSTOM_PATH, default=[])
    return data if isinstance(data, list) else []


def load_useful_system():
    path = os.path.join(DATA_DIR, "useful_system.json")
    return _load_json(path, default=[])


def _meta(category_id, subcategory_id=""):
    cats = load_categories()
    cat = cats.get(category_id, {"order": 99, "title": category_id, "subs": {}})
    subs = cat.get("subs", {})
    sub = subs.get(subcategory_id, {"order": 0, "title": ""})
    return {
        "category": category_id,
        "category_title": cat.get("title", category_id),
        "category_order": cat.get("order", 99),
        "subcategory": subcategory_id,
        "subcategory_title": sub.get("title", ""),
        "subcategory_order": sub.get("order", 0),
    }


def all_cards():
    by_name = {c["name"].lower(): dict(c) for c in load_essential()}
    for card in load_custom():
        by_name[card["name"].lower()] = dict(card)
    return list(by_name.values())


def get_card(name):
    name = name.lower()
    for card in all_cards():
        if card["name"].lower() == name:
            meta = _meta(card.get("category", ""), card.get("subcategory", ""))
            return {**card, **meta, "tier": "essential"}
    return None


def whatis(name):
    try:
        out = subprocess.check_output(
            ["whatis", name], stderr=subprocess.DEVNULL, text=True, timeout=5
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
        return None
    for line in out.splitlines():
        match = re.match(r"^(.+?)\s+-\s+(.+)$", line)
        if match and name.lower() in match.group(1).lower():
            return match.group(2).strip()
    return out.splitlines()[0] if out.strip() else None


def system_entry(name):
    index = load_index()
    if not index:
        return None
    name = name.lower()
    for entry in index.get("commands", []):
        if entry["name"].lower() == name:
            return entry
    return None


def resolve(name):
    card = get_card(name)
    if card:
        return card

    useful = next(
        (u for u in load_useful_system() if u["name"].lower() == name.lower()),
        None,
    )
    if useful:
        entry = system_entry(name)
        desc = (
            (entry or {}).get("man_desc")
            or useful.get("title")
            or whatis(name)
            or "Системная команда"
        )
        meta = _meta(useful.get("category", "system"), useful.get("subcategory", ""))
        return {
            "name": useful["name"],
            "title": useful.get("title", useful["name"]),
            "what": desc,
            "when": f"Полезная команда macOS. Подробности: man {useful['name']}",
            "when_not": None,
            "examples": [{"cmd": f"man {useful['name']}", "desc": "Полная документация"}],
            "danger": False,
            "related": [],
            "tags": [],
            "tier": "useful",
            **meta,
        }

    entry = system_entry(name)
    if entry:
        meta = _meta("system", "info")
        return {
            "name": entry["name"],
            "title": entry.get("man_desc") or entry["name"],
            "what": entry.get("man_desc") or whatis(entry["name"]) or "Описание недоступно",
            "when": f"Системная команда macOS. Подробности: man {entry['name']}",
            "when_not": None,
            "examples": [{"cmd": f"man {entry['name']}", "desc": "Полная документация"}],
            "danger": False,
            "related": [],
            "tags": [],
            "tier": "system",
            "source": entry.get("source"),
            **meta,
        }

    desc = whatis(name)
    if desc:
        meta = _meta("system", "info")
        return {
            "name": name,
            "title": name,
            "what": desc,
            "when": f"Подробности: man {name}",
            "when_not": None,
            "examples": [{"cmd": f"man {name}", "desc": "Полная документация"}],
            "danger": False,
            "related": [],
            "tags": [],
            "tier": "system",
            **meta,
        }
    return None


def related_cards(name, limit=8):
    card = resolve(name)
    if not card:
        return []
    related = card.get("related", [])
    results = []
    for rel in related[:limit]:
        if item := resolve(rel):
            results.append(item)
    return results


def _matches(card, query):
    q = query.lower()
    fields = [
        card.get("name", ""),
        card.get("title", ""),
        card.get("what", ""),
        card.get("when", ""),
        card.get("category_title", ""),
        card.get("subcategory_title", ""),
        " ".join(card.get("tags", [])),
    ]
    return q in " ".join(fields).lower()


def search(query, include_system=False):
    results = []
    seen = set()

    for card in all_cards():
        if _matches(card, query):
            key = card["name"].lower()
            if key not in seen:
                seen.add(key)
                meta = _meta(card.get("category", ""), card.get("subcategory", ""))
                results.append({**card, **meta, "tier": "essential"})

    for useful in load_useful_system():
        key = useful["name"].lower()
        if key in seen:
            continue
        text = f"{useful['name']} {useful.get('title', '')}".lower()
        if query.lower() in text:
            seen.add(key)
            meta = _meta(useful.get("category", "system"), useful.get("subcategory", ""))
            results.append(
                {
                    "name": useful["name"],
                    "title": useful.get("title", useful["name"]),
                    "what": useful.get("title"),
                    "tier": "useful",
                    **meta,
                }
            )

    if include_system or len(results) < 5:
        index = load_index()
        if index:
            q = query.lower()
            for entry in index.get("commands", []):
                key = entry["name"].lower()
                if key in seen:
                    continue
                desc = (entry.get("man_desc") or "").lower()
                if q in key or q in desc:
                    seen.add(key)
                    meta = _meta("system", "info")
                    results.append(
                        {
                            "name": entry["name"],
                            "title": entry.get("man_desc") or entry["name"],
                            "what": entry.get("man_desc"),
                            "tier": "system",
                            **meta,
                        }
                    )

    if not results and not include_system:
        try:
            apropos_out = subprocess.check_output(
                ["apropos", "-s", "1", query],
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=10,
            )
            for line in apropos_out.splitlines()[:15]:
                match = re.match(r"^(.+?)\s+-\s+(.+)$", line)
                if not match:
                    continue
                primary = re.sub(
                    r"\(\d+[a-z]*\)$",
                    "",
                    match.group(1).split(",")[0].strip(),
                )
                if primary.lower() in seen:
                    continue
                seen.add(primary.lower())
                meta = _meta("system", "info")
                results.append(
                    {
                        "name": primary,
                        "title": match.group(2).strip(),
                        "what": match.group(2).strip(),
                        "tier": "system",
                        **meta,
                    }
                )
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            pass

    return results


def _sort_key(entry):
    return (
        TIER_ORDER.get(entry.get("tier", "system"), 9),
        entry.get("category_order", 99),
        entry.get("subcategory_order", 0),
        entry["name"].lower(),
    )


def browser_entries(recent_names, show_all=False):
    entries = []
    seen = set()

    def add(card, tier):
        key = card["name"].lower()
        if key in seen:
            return
        seen.add(key)
        if "category_title" not in card:
            meta = _meta(card.get("category", "system"), card.get("subcategory", ""))
            card = {**card, **meta}
        entries.append({**card, "tier": tier})

    for card in all_cards():
        add(card, "essential")

    for name in recent_names:
        if card := get_card(name):
            add(card, "recent")
        elif resolve(name):
            add(resolve(name), "recent")

    for useful in load_useful_system():
        if useful["name"].lower() in seen:
            continue
        entry = system_entry(useful["name"])
        meta = _meta(useful.get("category", "system"), useful.get("subcategory", ""))
        desc = (entry or {}).get("man_desc") or useful.get("title") or useful["name"]
        add(
            {
                "name": useful["name"],
                "title": useful.get("title", desc),
                "what": desc,
                **meta,
            },
            "useful",
        )

    if show_all:
        index = load_index()
        if index:
            for entry in index.get("commands", []):
                if entry["name"].lower() in seen:
                    continue
                meta = _meta("system", "info")
                add(
                    {
                        "name": entry["name"],
                        "title": entry.get("man_desc") or entry["name"],
                        "what": entry.get("man_desc"),
                        **meta,
                    },
                    "system",
                )

    entries.sort(key=_sort_key)
    return entries