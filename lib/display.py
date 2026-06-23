from .i18n import t, tier_icons, tier_labels


def format_card(card, compact=False):
    lines = []
    tier = card.get("tier", "essential")
    icon = tier_icons().get(tier, "")
    tiers = tier_labels()
    tier_label = tiers.get(tier, tier)

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
        lines.append(f"\n{t('card.what')}:\n  {card['what']}")
    if card.get("when"):
        lines.append(f"\n{t('card.when')}:\n  {card['when']}")
    if card.get("when_not"):
        lines.append(f"\n{t('card.when_not')}:\n  {card['when_not']}")

    examples = card.get("examples", [])
    if examples:
        lines.append(f"\n{t('card.examples')}:")
        for i, ex in enumerate(examples, 1):
            lines.append(f"  [{i}] $ {ex['cmd']}")
            if ex.get("desc"):
                lines.append(f"      → {ex['desc']}")
        if not compact:
            lines.append(t("card.pick_example", name=card["name"]))

    if card.get("danger"):
        note = card.get("danger_note", t("card.danger_default"))
        lines.append(f"\n⚠️  {t('card.danger')}: {note}")

    related = card.get("related", [])
    if related and not compact:
        lines.append(f"\n{t('card.related')}: {', '.join(related)}")
        lines.append(t("card.related_cmd", name=card["name"]))

    if tier in ("system", "useful") and not compact:
        lines.append(f"\n💡 {t('card.edit_hint', name=card['name']).strip()}")

    lines.append("")
    return "\n".join(lines)


def format_search_results(results, query):
    if not results:
        return t("search.none", query=query)
    lines = [t("search.header", count=len(results), query=query) + "\n"]
    icons = tier_icons()
    for i, r in enumerate(results):
        tier = icons.get(r.get("tier", ""), " ")
        title = r.get("title") or r.get("what") or ""
        lines.append(f"  [{i}] {tier} {r['name']} — {title}")
    lines.append(t("search.footer"))
    return "\n".join(lines)


def format_browser_line(entry):
    tier = tier_icons().get(entry.get("tier", ""), " ")
    cat = entry.get("category_title", "")
    sub = entry.get("subcategory_title", "")
    title = entry.get("title", "")
    group = f"{cat} → {sub}" if sub else cat
    display = f"{tier} {entry['name']} — {title}  [{group}]"
    return f"{display}\t{entry['name']}\t{group}\t{entry.get('tier', '')}"


def format_group_header(entry):
    tiers = tier_labels()
    tier = tiers.get(entry.get("tier", ""), entry.get("tier", ""))
    cat = entry.get("category_title", "")
    sub = entry.get("subcategory_title", "")
    if sub:
        label = f"{tier} · {cat} → {sub}"
    else:
        label = f"{tier} · {cat}"
    return f"# ── {label} ──\t\t\t"