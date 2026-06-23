import json
import os
import re
import subprocess

from .paths import INDEX_PATH, ensure_user_dir


def _run(cmd, shell=False):
    try:
        return subprocess.check_output(
            cmd, shell=shell, stderr=subprocess.DEVNULL, text=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def _parse_apropos(output):
    entries = {}
    for line in output.splitlines():
        match = re.match(r"^(.+?)\s+-\s+(.+)$", line)
        if not match:
            continue
        names_part, desc = match.group(1).strip(), match.group(2).strip()
        primary = re.sub(r"\(\d+[a-z]*\)$", "", names_part.split(",")[0].strip())
        if not primary or primary.startswith("npm-") or primary.startswith("gh-"):
            continue
        if primary not in entries:
            entries[primary] = {
                "name": primary,
                "man_desc": desc,
                "source": "apropos",
            }
    return entries


def _zsh_list(array_name):
    script = f"print -l ${{(k){array_name}}}"
    return [line.strip() for line in _run(["zsh", "-c", script]).splitlines() if line.strip()]


def build_index():
    ensure_user_dir()
    entries = _parse_apropos(_run(["apropos", "-s", "1", "."]))

    for name in _zsh_list("commands"):
        if name not in entries:
            entries[name] = {"name": name, "man_desc": None, "source": "path"}
        entries[name]["available"] = True

    for name in _zsh_list("builtins"):
        if name not in entries:
            entries[name] = {"name": name, "man_desc": None, "source": "builtin"}
        entries[name]["builtin"] = True

    for name, entry in entries.items():
        entry.setdefault("available", False)
        entry.setdefault("builtin", False)

    data = {
        "version": 1,
        "count": len(entries),
        "commands": sorted(entries.values(), key=lambda x: x["name"].lower()),
    }

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return data


def load_index():
    if not os.path.exists(INDEX_PATH):
        return None
    with open(INDEX_PATH, encoding="utf-8") as f:
        return json.load(f)