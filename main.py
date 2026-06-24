#!/usr/bin/env python3
import json
import os
import subprocess
import sys

from lib.browser import browse, browse_related, preview
from lib.display import format_card, format_search_results
from lib.examples import copy_first_example, pick_example
from lib.history import record, recent
from lib.i18n import get_locale, language_choices, load_ui, set_locale, t
from lib.lang_menu import pick_language
from lib.index import build_index, load_index
from lib.lookup import resolve, search
from lib.paths import CUSTOM_PATH, INDEX_PATH, ensure_user_dir
from lib.version import get_version


def build_help():
    usage = load_ui().get("help.usage_lines", [])
    if not usage:
        usage = [
            "  cmd                    fzf browser",
            "  cmd ls                 command card",
            "  cmd <query>            keyword search",
            "  cmd related ls         related commands",
            "  cmd --pick             pick command (shell widget)",
            "  cmd --pick-example ls  pick example (Enter/Ctrl-Y)",
            "  cmd --copy ls          copy first example",
            "  cmd --all              include all system commands",
            "  cmd index              rebuild macOS index",
            "  cmd edit docker        personal card",
            "  cmd lang               language menu (fzf)",
            "  cmd lang en|ru|zh      set language directly",
            "  cmd --version          show version",
        ]
    lines = [
        t("help.title"),
        "",
        t("help.usage_header"),
        *usage,
        "",
        t("help.hotkeys"),
        t("help.widget"),
    ]
    return "\n".join(lines)


def cmd_lang(arg=None):
    if not arg:
        return pick_language()
    try:
        code = set_locale(arg)
    except ValueError:
        print(t("lang.invalid", code=arg), file=sys.stderr)
        return 1
    name = next((n for c, n in language_choices() if c == code), code)
    print(t("lang.set", name=name, code=code))
    return 0


def cmd_index():
    print(t("index.building"))
    data = build_index()
    print(t("index.done", count=data["count"], path=INDEX_PATH))


def cmd_edit(name):
    ensure_user_dir()
    name = name.lower()
    custom = []
    if os.path.exists(CUSTOM_PATH):
        with open(CUSTOM_PATH, encoding="utf-8") as f:
            custom = json.load(f)

    existing = next((c for c in custom if c["name"].lower() == name), None)
    if not existing:
        base = resolve(name) or {}
        existing = {
            "name": name,
            "category": base.get("category", "system"),
            "subcategory": base.get("subcategory", ""),
            "title": base.get("title", name),
            "what": base.get("what", ""),
            "when": base.get("when", ""),
            "when_not": base.get("when_not", ""),
            "examples": base.get("examples", [{"cmd": name, "desc": ""}]),
            "danger": base.get("danger", False),
            "related": base.get("related", []),
            "tags": base.get("tags", []),
        }
        custom.append(existing)

    with open(CUSTOM_PATH, "w", encoding="utf-8") as f:
        json.dump(custom, f, ensure_ascii=False, indent=2)

    editor = os.environ.get("EDITOR", "nano")
    subprocess.call([editor, CUSTOM_PATH])
    print(t("edit.saved", path=CUSTOM_PATH))


def cmd_lookup(query, show_all=False):
    has_index = load_index() is not None

    if query:
        card = resolve(query)
        if card:
            record(query)
            print(format_card(card))
            return 0

        if show_all and not has_index:
            print(t("index.missing"))
            return 1

        results = search(query, include_system=show_all)
        if len(results) == 1:
            full = resolve(results[0]["name"])
            if full:
                record(results[0]["name"])
                print(format_card(full))
                return 0

        if results:
            print(format_search_results(results, query))
            return 0

        print(t("lookup.not_found", query=query))
        if not has_index:
            print(t("index.missing"))
        else:
            print(t("lookup.try_all", query=query))
        return 1

    if show_all and not has_index:
        print(t("index.missing"))
        return 1

    browse(recent(), show_all=show_all)
    return 0


def main():
    argv = sys.argv[1:]

    if "--preview" in argv:
        idx = argv.index("--preview")
        if idx + 1 < len(argv):
            preview(argv[idx + 1])
        return 0

    if "-h" in argv or "--help" in argv:
        print(build_help())
        return 0

    if "--version" in argv or "-v" in argv:
        print(f"cmd {get_version()}")
        return 0

    if "--verify-capture" in argv:
        import importlib.util

        os.environ.setdefault("CMD_GIT_PURE", "1")
        spec = importlib.util.spec_from_file_location(
            "capture_evidence",
            os.path.join(os.path.dirname(__file__), "scripts", "capture_evidence.py"),
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.capture_artifacts()

    if "--pick" in argv:
        name = browse(recent(), show_all=False, silent=True)
        if name:
            pick_out = os.environ.get("CMD_PICK_OUT") or os.environ.get("FINDCMD_PICK_OUT")
            if pick_out:
                with open(pick_out, "w", encoding="utf-8") as f:
                    f.write(name)
            else:
                print(name, flush=True)
        return 0

    show_all = "--all" in argv
    argv = [a for a in argv if a not in ("--all",)]

    if "--pick-example" in argv:
        idx = argv.index("--pick-example")
        if idx + 1 >= len(argv):
            print(t("pick_example.usage"), file=sys.stderr)
            return 1
        example = pick_example(argv[idx + 1], silent=False)
        if example:
            example_out = os.environ.get("CMD_EXAMPLE_OUT") or os.environ.get("FINDCMD_EXAMPLE_OUT")
            if example_out:
                with open(example_out, "w", encoding="utf-8") as f:
                    f.write(example)
            else:
                print(example, flush=True)
        return 0

    if "--copy" in argv:
        idx = argv.index("--copy")
        if idx + 1 >= len(argv):
            print(t("copy.usage"), file=sys.stderr)
            return 1
        if copy_first_example(argv[idx + 1]):
            card = resolve(argv[idx + 1])
            ex = card["examples"][0]["cmd"] if card and card.get("examples") else ""
            print(t("copy.done", cmd=ex))
        else:
            print(t("copy.none"))
            return 1
        return 0

    if not argv:
        return cmd_lookup(None, show_all=show_all) or 0

    if argv[0] == "index":
        cmd_index()
        return 0

    if argv[0] == "lang":
        return cmd_lang(argv[1] if len(argv) > 1 else None)

    if argv[0] == "edit":
        if len(argv) < 2:
            print(t("edit.usage"))
            return 1
        cmd_edit(argv[1])
        return 0

    if argv[0] == "related":
        if len(argv) < 2:
            print(t("related.usage"))
            return 1
        browse_related(argv[1])
        return 0

    query = " ".join(argv)
    return cmd_lookup(query, show_all=show_all) or 0


if __name__ == "__main__":
    sys.exit(main())