import shutil
import subprocess
import sys

from .clipboard import copy_text
from .display import format_card
from .lookup import resolve


def _run_fzf(lines, header, expect=None):
    if not shutil.which("fzf"):
        return None, None

    cmd = [
        "fzf",
        "--delimiter=\t",
        "--with-nth=1",
        f"--header={header}",
        "--height=40%",
        "--layout=reverse",
    ]
    if expect:
        for key in expect:
            cmd.append(f"--expect={key}")

    result = subprocess.run(
        cmd,
        input="\n".join(lines),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None, None

    if expect:
        parts = result.stdout.strip().split("\n", 1)
        key = parts[0]
        selected = parts[1] if len(parts) > 1 else ""
        return key, selected

    return None, result.stdout.strip()


def example_lines(card):
    lines = []
    for ex in card.get("examples", []):
        cmd = ex["cmd"]
        desc = ex.get("desc", "")
        display = f"$ {cmd}"
        if desc:
            display += f"  — {desc}"
        lines.append(f"{display}\t{cmd}")
    return lines


def pick_example(name, silent=False, action="insert"):
    card = resolve(name)
    if not card:
        return None

    lines = example_lines(card)
    if not lines:
        if not silent:
            print(format_card(card))
            print("Нет примеров для этой команды.")
        return None

    if len(lines) == 1 and silent:
        return lines[0].split("\t", 1)[1]

    header = "Enter — вставить | Ctrl-Y — копировать | Esc — отмена"
    key, selected = _run_fzf(lines, header, expect=["ctrl-y", "enter"])
    if not selected:
        return None

    cmd = selected.split("\t", 1)[1] if "\t" in selected else selected

    if key == "ctrl-y":
        if copy_text(cmd):
            print(f"Скопировано: {cmd}", file=sys.stderr)
        else:
            print(f"Копирование недоступно. Команда: {cmd}", file=sys.stderr)
        return None

    if action == "run":
        if card.get("danger"):
            try:
                answer = input(f"⚠️  Запустить: {cmd}? [y/N] ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                return None
            if answer != "y":
                print("Отменено.")
                return None
        subprocess.run(cmd, shell=True)
        return None

    return cmd


def copy_first_example(name) -> bool:
    card = resolve(name)
    if not card or not card.get("examples"):
        return False
    cmd = card["examples"][0]["cmd"]
    return copy_text(cmd)