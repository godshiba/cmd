import shutil
import subprocess
import sys

from .clipboard import copy_text
from .display import format_card
from .fzf_util import run_fzf
from .i18n import t
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
            print(t("example.none"))
        return None

    if len(lines) == 1 and silent:
        return lines[0].split("\t", 1)[1]

    if not shutil.which("fzf"):
        print(t("example.install_fzf"), file=sys.stderr)
        return lines[0].split("\t", 1)[1]

    cmd = [
        "fzf",
        "--delimiter=\t",
        "--with-nth=1",
        f"--header={t('example.fzf_header')}",
        "--height=40%",
        "--layout=reverse",
        "--bind=enter:accept",
        "--bind=ctrl-y:execute-silent(echo -n {2} | pbcopy;"
        " printf '\\nCopied: %s\\n' {2} >/dev/tty)+abort",
    ]

    selected = run_fzf(cmd, lines)
    if not selected:
        return None

    example_cmd = selected.split("\t", 1)[1] if "\t" in selected else selected

    if action == "run":
        if card.get("danger"):
            try:
                answer = input(t("example.run_confirm", cmd=example_cmd)).strip().lower()
            except (EOFError, KeyboardInterrupt):
                return None
            if answer != "y":
                print(t("example.cancelled"))
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