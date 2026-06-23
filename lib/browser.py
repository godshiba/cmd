import os
import shlex
import shutil
import subprocess
import sys

from .display import format_browser_line, format_card, format_group_header
from .examples import pick_example
from .history import record
from .lookup import browser_entries, related_cards, resolve


def _preview_script():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")


def _build_fzf_input(entries):
    lines = []
    last_group = None
    for entry in entries:
        group = (
            entry.get("tier", ""),
            entry.get("category_title", ""),
            entry.get("subcategory_title", ""),
        )
        if group != last_group:
            lines.append(format_group_header(entry))
            last_group = group
        lines.append(format_browser_line(entry))
    return lines


def run_fzf(entries, silent=False):
    lines = _build_fzf_input(entries)
    if not lines:
        if not silent:
            print("Нет команд. Запусти: findcmd index")
        return None

    py = shlex.quote(sys.executable)
    script = shlex.quote(_preview_script())
    preview_cmd = f"{py} {script} --preview {{2}}"
    pick_example_cmd = f"{py} {script} --pick-example {{2}}"
    cmd = [
        "fzf",
        "--delimiter=\t",
        "--with-nth=1",
        "--disabled=#.*",
        "--header=⭐ Основные | 🕐 Недавние | ✦ Полезные | Enter: карточка | Ctrl-E: пример",
        f"--preview={preview_cmd}",
        "--preview-window=right:55%:wrap",
        "--height=85%",
        "--layout=reverse",
        f"--bind=ctrl-e:execute-silent({pick_example_cmd})+abort",
    ]

    try:
        result = subprocess.run(
            cmd,
            input="\n".join(lines),
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError:
        if silent:
            return None
        return run_fallback(entries)

    if result.returncode != 0 or not result.stdout.strip():
        return None

    line = result.stdout.strip()
    if line.startswith("#"):
        return None
    parts = line.split("\t")
    return parts[1].strip() if len(parts) > 1 else None


def run_fallback(entries):
    print("\n--- findcmd ---\n")
    last_group = None
    shown = 0
    indexed = []

    for entry in entries:
        group = (
            entry.get("tier", ""),
            entry.get("category_title", ""),
            entry.get("subcategory_title", ""),
        )
        if group != last_group:
            print(format_group_header(entry).split("\t")[0])
            last_group = group
        print(f"  [{shown}] {format_browser_line(entry).split(chr(9))[0]}")
        indexed.append(entry)
        shown += 1
        if shown >= 60:
            break

    try:
        choice = input("\nНомер (Enter — выход): ").strip()
    except (EOFError, KeyboardInterrupt):
        return None

    if not choice.isdigit() or int(choice) >= len(indexed):
        return None
    return indexed[int(choice)]["name"]


def browse(recent_names, show_all=False, silent=False):
    entries = browser_entries(recent_names, show_all=show_all)
    if not entries:
        if not silent:
            print("Пусто. Запусти: findcmd index")
        return None

    use_fzf = shutil.which("fzf") is not None
    name = run_fzf(entries, silent=silent) if use_fzf else run_fallback(entries)
    if not name:
        return None

    if silent:
        return name

    card = resolve(name)
    if card:
        record(name)
        print(format_card(card))
    return name


def browse_related(name):
    cards = related_cards(name)
    if not cards:
        print(f"Нет связанных команд для «{name}».")
        return

    entries = [{**c, "tier": c.get("tier", "essential")} for c in cards]
    picked = run_fzf(entries, silent=False)
    if picked:
        card = resolve(picked)
        if card:
            record(picked)
            print(format_card(card))


def preview(name):
    card = resolve(name.strip())
    if card:
        print(format_card(card, compact=True))
    else:
        print(f"Команда «{name}» не найдена")