import shutil
import sys

from .fzf_util import run_fzf
from .i18n import get_locale, language_choices, set_locale, t


def pick_language():
    code = get_locale()
    name = next((n for c, n in language_choices() if c == code), code)
    print(t("lang.current", name=name, code=code))
    print()

    if not sys.stdin.isatty() or not shutil.which("fzf"):
        print(t("lang.available"))
        for c, n in language_choices():
            mark = " ←" if c == code else ""
            print(f"  {c}  {n}{mark}")
        print(f"\n{t('lang.usage')}")
        return 0

    lines = []
    for c, n in language_choices():
        mark = "✓ " if c == code else "  "
        lines.append(f"{mark}{n} ({c})\t{c}")

    header = t("lang.menu_header")
    selected = run_fzf(
        [
            "fzf",
            "--delimiter=\t",
            "--with-nth=1",
            f"--header={header}",
            "--height=40%",
            "--layout=reverse",
            "--bind=enter:accept",
        ],
        lines,
    )
    if not selected:
        print(t("lang.menu_cancelled"))
        return 0

    picked = selected.split("\t", 1)[1].strip() if "\t" in selected else selected.strip()
    try:
        new_code = set_locale(picked)
    except ValueError:
        print(t("lang.invalid", code=picked), file=sys.stderr)
        return 1

    new_name = next((n for c, n in language_choices() if c == new_code), new_code)
    print(t("lang.set", name=new_name, code=new_code))
    return 0