# Changelog

All notable changes to **cmd** are documented here.

## [0.1.0] — 2026-06-23

### Added
- Smoke test suite: `tests/test_smoke.py` (locale parity, lookup, CLI)
- Production audit runbook: `.claude/plans/production-audit-runbook.md`

### Fixed
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

## [1.0.0] — 2026-06-23

### Added
- CLI `cmd` — terminal command navigator for macOS
- fzf browser with Essential / Recent / Useful / System tiers
- 32 curated Essential cards with examples
- i18n: English, Russian, Chinese (`cmd lang`)
- zsh hotkeys: Ctrl+O, F2
- `cmd index` — macOS command index via apropos
- Personal cards via `cmd edit`
- Multilingual README: [EN](README.md) · [RU](README.ru.md) · [ZH](README.zh-CN.md)

[0.1.0]: https://github.com/godshiba/cmd/releases/tag/v0.1.0
[0.0.3]: https://github.com/godshiba/cmd/releases/tag/v0.0.3
[0.0.2]: https://github.com/godshiba/cmd/releases/tag/v0.0.2
[1.0.0]: https://github.com/godshiba/cmd/releases/tag/v1.0.0