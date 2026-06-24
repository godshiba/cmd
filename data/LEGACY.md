# Legacy data (`data/legacy/`)

Russian originals kept as **fallback only** when a locale pack file is missing.

| File | Fallback for |
|------|----------------|
| `locales/ru/essential.json` | ultimate Russian fallback for essential (no duplicate in `legacy/`) |
| `legacy/categories.json` | `categories.json` when locale pack missing |
| `legacy/useful_system.json` | `useful_system.json` when locale pack missing |

**Authoritative data:** `data/locales/{en,ru,zh}/` via `lib/paths.locale_data_path()`.

To move stray root-level `data/*.json` into `data/legacy/`, run `python3 scripts/migrate_legacy.py` (also invoked by `scripts/verify.sh`).