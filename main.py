#!/usr/bin/env python3
import json
import os
import subprocess
import sys

from lib.browser import browse, browse_related, preview
from lib.clipboard import copy_text
from lib.display import format_card, format_search_results
from lib.examples import copy_first_example, pick_example
from lib.history import record, recent
from lib.index import build_index, load_index
from lib.lookup import related_cards, resolve, search
from lib.paths import CUSTOM_PATH, INDEX_PATH, ensure_user_dir


HELP = """findcmd — личный навигатор по командам терминала

Использование:
  findcmd                    браузер с группировкой (fzf)
  findcmd ls                 карточка команды
  findcmd копир              поиск по ключевому слову
  findcmd related ls         связанные команды
  findcmd --pick             выбрать команду (для shell-виджета)
  findcmd --pick-example ls  выбрать пример (Enter/Ctrl-Y)
  findcmd --copy ls          скопировать первый пример
  findcmd --all              показать все системные команды
  findcmd index              обновить индекс macOS
  findcmd edit docker        своя карточка

Горячая клавиша (zsh):
  source ~/scripts/findcmd/shell/findcmd.widget.zsh
"""


def cmd_index():
    print("Строю индекс команд macOS...")
    data = build_index()
    print(f"Готово: {data['count']} команд → {INDEX_PATH}")


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
            "title": base.get("title", f"Команда {name}"),
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
    print(f"Сохранено в {CUSTOM_PATH}")


def cmd_lookup(query, show_all=False):
    if not load_index():
        print("Индекс не найден. Запусти: findcmd index")
        return 1

    if query:
        card = resolve(query)
        if card:
            record(query)
            print(format_card(card))
            return 0

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

        print(f"Команда «{query}» не найдена.")
        print(f"Попробуй: findcmd --all {query}")
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
        print(HELP)
        return 0

    if "--pick" in argv:
        name = browse(recent(), show_all=False, silent=True)
        if name:
            pick_out = os.environ.get("FINDCMD_PICK_OUT")
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
            print("Укажи команду: findcmd --pick-example ls", file=sys.stderr)
            return 1
        example = pick_example(argv[idx + 1], silent=False)
        if example:
            example_out = os.environ.get("FINDCMD_EXAMPLE_OUT")
            if example_out:
                with open(example_out, "w", encoding="utf-8") as f:
                    f.write(example)
            else:
                print(example, flush=True)
        return 0

    if "--copy" in argv:
        idx = argv.index("--copy")
        if idx + 1 >= len(argv):
            print("Укажи команду: findcmd --copy ls", file=sys.stderr)
            return 1
        if copy_first_example(argv[idx + 1]):
            card = resolve(argv[idx + 1])
            ex = card["examples"][0]["cmd"] if card and card.get("examples") else ""
            print(f"Скопировано: {ex}")
        else:
            print("Нет примера для копирования.")
            return 1
        return 0

    if not argv:
        return cmd_lookup(None, show_all=show_all) or 0

    if argv[0] == "index":
        cmd_index()
        return 0

    if argv[0] == "edit":
        if len(argv) < 2:
            print("Укажи команду: findcmd edit docker")
            return 1
        cmd_edit(argv[1])
        return 0

    if argv[0] == "related":
        if len(argv) < 2:
            print("Укажи команду: findcmd related ls")
            return 1
        browse_related(argv[1])
        return 0

    query = " ".join(argv)
    return cmd_lookup(query, show_all=show_all) or 0


if __name__ == "__main__":
    sys.exit(main())