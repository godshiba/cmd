# Changelog

All notable changes to **cmd** are documented here.

## [0.1.0] — 2026-06-23

### Added
- Smoke test suite: `tests/test_smoke.py` (locale parity, lookup, CLI)
- Local verify gate: `scripts/verify.sh`
- Evidence gate: `scripts/capture_evidence.py`, `tests/test_evidence.py`
- Localized `cmd --help` usage lines (`help.usage_lines` in en/ru/zh `ui.json`)
- `data/legacy/` isolated fallbacks + `data/LEGACY.md`; `scripts/migrate_legacy.py`
- Release notes: `.github/release-notes/v0.0.3.md`, `v0.1.0.md`
- Production audit runbook: `.claude/plans/production-audit-runbook.md`

### Fixed
- Docs: command table uses `cmd <query>` (not bogus `cmd copy` subcommand); README VERSION = 0.1.0; CHANGELOG 1.0.0 → 0.0.1
- `lib/lookup.py` useful-system fallback path → `data/legacy/`
- `lib/paths.py`: no import-time migration; `ESSENTIAL_PATH` → `locales/ru/essential.json`
- fzf browser from zsh widget (Ctrl+O / F2): items now reach fzf via stdin pipe
- `cmd ls` and essential lookup work without `cmd index`
- Search matches example text (e.g. `cmd docker` finds `brew`)
- `cmd related` fallback list when fzf is not installed
- Locale cache refreshes when `CMD_LANG` env is cleared or config changes
- zsh index builder: correct `commands` / `builtins` array listing

## [0.0.3] — 2026-06-23

### Fixed
- Browser hang after `cmd lang` — removed 76× `whatis` subprocess calls on Useful tier load
- Cache useful commands per locale; clear cache on language change

## [0.0.2] — 2026-06-23

### Fixed
- Mixed languages in browser: Useful tier now loads locale-specific titles (en/ru/zh)
- `cmd` not found after install — added `install.sh` and `~/bin/cmd` symlink

### Added
- Interactive language menu: `cmd lang` (fzf picker)
- Locale files for Useful commands: `data/locales/*/useful_system.json`
- Language hint in browser header

## [0.0.1] — 2026-06-23

### Added
- Initial release: terminal command navigator for macOS (project formerly `findcmd`)
- fzf browser with Essential / Recent / Useful / System tiers
- 32 curated Essential cards with examples
- zsh hotkeys: Ctrl+O, F2
- `cmd index` — macOS command index via apropos
- Personal cards via `cmd edit`

[0.1.0]: https://github.com/godshiba/cmd/releases/tag/v0.1.0
[0.0.3]: https://github.com/godshiba/cmd/releases/tag/v0.0.3
[0.0.2]: https://github.com/godshiba/cmd/releases/tag/v0.0.2
[0.0.1]: https://github.com/godshiba/cmd/releases/tag/v0.0.1