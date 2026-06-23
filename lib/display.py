TIER_LABELS = {
    "essential": "Основные",
    "recent": "Недавние",
    "useful": "Полезные",
    "system": "Система",
}

TIER_ICONS = {
    "essential": "⭐",
    "recent": "🕐",
    "useful": "✦",
    "system": "💻",
}


def format_card(card, compact=False):
    lines = []
    tier = card.get("tier", "essential")
    icon = TIER_ICONS.get(tier, "")
    tier_label = TIER_LABELS.get(tier, tier)

    lines.append("=" * 50)
    lines.append(f"{icon} {card['name']} — {card.get('title', '')}")
    sub = card.get("subcategory_title")
    cat = card.get("category_title", "")
    if sub:
        lines.append(f"   {cat} → {sub}  [{tier_label}]")
    elif tier != "essential" or card.get("source"):
        lines.append(f"   [{tier_label}]")
    lines.append("=" * 50)

    if card.get("what"):
        lines.append(f"\nЧто делает:\n  {card['what']}")
    if card.get("when"):
        lines.append(f"\nЗачем нужна:\n  {card['when']}")
    if card.get("when_not"):
        lines.append(f"\nКогда НЕ нужна:\n  {card['when_not']}")

    examples = card.get("examples", [])
    if examples:
        lines.append("\nПримеры:")
        for i, ex in enumerate(examples, 1):
            lines.append(f"  [{i}] $ {ex['cmd']}")
            if ex.get("desc"):
                lines.append(f"      → {ex['desc']}")
        if not compact:
            lines.append("\n  findcmd --pick-example " + card["name"] + "  — выбрать пример")

    if card.get("danger"):
        note = card.get("danger_note", "Будь осторожен с этой командой!")
        lines.append(f"\n⚠️  ОПАСНО: {note}")

    related = card.get("related", [])
    if related and not compact:
        lines.append(f"\nСвязанные: {', '.join(related)}")
        lines.append(f"  findcmd related {card['name']}  — открыть связанные")

    if tier in ("system", "useful") and not compact:
        lines.append(f"\n💡 Добавь свою карточку: findcmd edit {card['name']}")

    lines.append("")
    return "\n".join(lines)


def format_search_results(results, query):
    if not results:
        return f"Ничего не найдено по запросу «{query}».\nПопробуй: findcmd --all {query}"
    lines = [f"Найдено: {len(results)} по запросу «{query}»\n"]
    for i, r in enumerate(results):
        tier = TIER_ICONS.get(r.get("tier", ""), " ")
        title = r.get("title") or r.get("what") or ""
        lines.append(f"  [{i}] {tier} {r['name']} — {title}")
    lines.append("\nfindcmd <имя>  или  findcmd --pick")
    return "\n".join(lines)


def format_browser_line(entry):
    tier = TIER_ICONS.get(entry.get("tier", ""), " ")
    cat = entry.get("category_title", "")
    sub = entry.get("subcategory_title", "")
    title = entry.get("title", "")
    group = f"{cat}/{sub}" if sub else cat
    display = f"{tier} {entry['name']} — {title}"
    return f"{display}\t{entry['name']}\t{group}\t{entry.get('tier', '')}"


def format_group_header(entry):
    tier = TIER_LABELS.get(entry.get("tier", ""), entry.get("tier", ""))
    cat = entry.get("category_title", "")
    sub = entry.get("subcategory_title", "")
    if sub:
        label = f"{tier} · {cat} → {sub}"
    else:
        label = f"{tier} · {cat}"
    return f"# ── {label} ──\t\t\t"