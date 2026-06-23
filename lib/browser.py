import os
import shlex
import shutil
import subprocess
import sys

from .display import format_browser_line, format_card
from .fzf_util import run_fzf as exec_fzf
from .history import record
from .i18n import t
from .lookup import browser_entries, related_cards, resolve


def _preview_script():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "main.py")


def _build_fzf_input(entries):
    return [format_browser_line(entry) for entry in entries]


def pick_command_fzf(entries, silent=False):
    lines = _build_fzf_input(entries)
    if not lines:
        if not silent:
            print(t("browser.no_commands"))
        return None

    py = shlex.quote(sys.executable)
    script = shlex.quote(_preview_script())
    preview_cmd = f"{py} {script} --preview {{2}}"
    pick_example_cmd = f"{py} {script} --pick-example {{2}}"

    cmd = [
        "fzf",
        "--delimiter=\t",
        "--with-nth=1",
        f"--header={t('browser.fzf_header')}",
        f"--preview={preview_cmd}",
        "--preview-window=right:55%:wrap",
        "--height=85%",
        "--layout=reverse",
        "--bind=enter:accept",
        f"--bind=ctrl-e:execute({pick_example_cmd})+abort",
    ]

    try:
        line = exec_fzf(cmd, lines)
    except FileNotFoundError:
        if silent:
            return None
        return run_fallback(entries)

    if not line:
        if not silent:
            print(t("browser.closed"))
        return None

    parts = line.split("\t")
    return parts[1].strip() if len(parts) > 1 else None


def run_fallback(entries):
    print(f"\n{t('browser.fallback_title')}\n")
    shown = 0
    indexed = []

    for entry in entries:
        print(f"  [{shown}] {format_browser_line(entry).split(chr(9))[0]}")
        indexed.append(entry)
        shown += 1
        if shown >= 60:
            break

    try:
        choice = input(f"\n{t('browser.fallback_prompt')}").strip()
    except (EOFError, KeyboardInterrupt):
        return None

    if not choice.isdigit() or int(choice) >= len(indexed):
        return None
    return indexed[int(choice)]["name"]


def browse(recent_names, show_all=False, silent=False):
    entries = browser_entries(recent_names, show_all=show_all)
    if not entries:
        if not silent:
            print(t("browser.empty"))
        return None

    use_fzf = shutil.which("fzf") is not None
    name = pick_command_fzf(entries, silent=silent) if use_fzf else run_fallback(entries)
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
        print(t("browser.related_none", name=name))
        return

    use_fzf = shutil.which("fzf") is not None
    if not use_fzf:
        print(f"\n{t('browser.fallback_title')}\n")
        for i, card in enumerate(cards):
            print(f"  [{i}] {format_browser_line(card).split(chr(9))[0]}")
        try:
            choice = input(f"\n{t('browser.fallback_prompt')}").strip()
        except (EOFError, KeyboardInterrupt):
            return
        if not choice.isdigit() or int(choice) >= len(cards):
            return
        picked = cards[int(choice)]["name"]
    else:
        py = shlex.quote(sys.executable)
        script = shlex.quote(_preview_script())
        preview_cmd = f"{py} {script} --preview {{2}}"

        lines = [format_browser_line(c) for c in cards]
        cmd = [
            "fzf",
            "--delimiter=\t",
            "--with-nth=1",
            f"--header={t('browser.related_header', name=name)}",
            f"--preview={preview_cmd}",
            "--preview-window=right:55%:wrap",
            "--height=50%",
            "--layout=reverse",
            "--bind=enter:accept",
        ]

        line = exec_fzf(cmd, lines)
        if not line:
            return
        picked = line.split("\t")[1].strip() if "\t" in line else None

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
        print(t("browser.not_found", name=name))