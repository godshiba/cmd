import shutil
import subprocess
import sys

from .clipboard import copy_text
from .display import format_card
from .fzf_util import run_fzf
from .lookup import resolve


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

    if not shutil.which("fzf"):
        print("Установи fzf: brew install fzf", file=sys.stderr)
        return lines[0].split("\t", 1)[1]

    header = "Enter — вставить | Ctrl-Y — копировать | Esc — отмена"
    cmd = [
        "fzf",
        "--delimiter=\t",
        "--with-nth=1",
        f"--header={header}",
        "--height=40%",
        "--layout=reverse",
        "--bind=enter:accept",
        "--bind=ctrl-y:execute-silent(echo -n {2} | pbcopy;"
        " printf '\\nСкопировано: %s\\n' {2} >/dev/tty)+abort",
    ]

    selected = run_fzf(cmd, lines)
    if not selected:
        return None

    example_cmd = selected.split("\t", 1)[1] if "\t" in selected else selected

    if action == "run":
        if card.get("danger"):
            try:
                answer = input(f"⚠️  Запустить: {example_cmd}? [y/N] ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                return None
            if answer != "y":
                print("Отменено.")
                return None
        subprocess.run(example_cmd, shell=True)
        return None

    return example_cmd


def copy_first_example(name) -> bool:
    card = resolve(name)
    if not card or not card.get("examples"):
        return False
    cmd = card["examples"][0]["cmd"]
    return copy_text(cmd)