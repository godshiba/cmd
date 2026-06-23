# cmd

**Terminal command navigator for macOS** — curated cards, examples, fuzzy browser, and hotkeys.

<p align="center">
  <strong>Readme</strong>:
  <a href="README.md"><b>English</b></a> ·
  <a href="README.ru.md">Русский</a> ·
  <a href="README.zh-CN.md">中文</a>
</p>

<p align="center">
  <a href="https://github.com/godshiba/cmd/releases"><img src="https://img.shields.io/github/v/release/godshiba/cmd?style=flat-square" alt="Release"></a>
  <img src="https://img.shields.io/badge/platform-macOS%2013+-000?style=flat-square" alt="macOS 13+">
  <img src="https://img.shields.io/badge/python-3.9+-3776ab?style=flat-square" alt="Python 3.9+">
  <img src="https://img.shields.io/badge/shell-zsh%205.8+-89b4fa?style=flat-square" alt="zsh">
  <img src="https://img.shields.io/badge/fzf-0.30+-fb4934?style=flat-square" alt="fzf">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT">
</p>

---

## Table of contents

- [What is cmd?](#what-is-cmd)
- [Requirements](#requirements)
- [Quick start](#quick-start)
- [App languages](#app-languages)
- [Hotkeys](#hotkeys)
- [Commands](#commands)
- [Repository structure](#repository-structure)
- [Changelog & license](#changelog--license)

---

## What is cmd?

`cmd` is a **personal command reference** in your terminal:

- **Cards** — what a command does, when to use it, when *not* to
- **Examples** — copy-ready commands (`ls -la`, `cd ..`, …)
- **Browser** — Essential → Recent → Useful, searchable with fzf
- **Hotkeys** — Ctrl+O / F2 from the zsh prompt

Does not replace `man`. Helps you **find and remember** commands faster.

## Requirements

| Component | Version | Notes |
|-----------|---------|-------|
| **macOS** | 13+ (Ventura) | Uses `apropos` / `whatis` for indexing |
| **Python** | 3.9+ | Stdlib only, no pip install |
| **zsh** | 5.8+ | Default shell on modern macOS |
| **fzf** | 0.30+ | `brew install fzf` — required for browser |
| **Terminal** | any | Hotkeys work on zsh input line |

Optional: [Homebrew](https://brew.sh) for installing fzf.

Check versions:

```bash
sw_vers                    # macOS
python3 --version          # Python 3.9+
zsh --version              # zsh 5.8+
fzf --version              # fzf 0.30+
cmd --version              # cmd 0.1.0
```

## Quick start

```bash
brew install fzf
git clone https://github.com/godshiba/cmd.git ~/scripts/cmd
cd ~/scripts/cmd
./cmd index
```

Add to `~/.zshrc`:

```bash
unalias cmd 2>/dev/null
export PATH="$HOME/scripts/cmd:$PATH"
source "$HOME/scripts/cmd/shell/cmd.widget.zsh"
```

```bash
source ~/.zshrc
cmd ls
cmd lang en    # optional: set UI language
```

## App languages

**Interactive menu** (recommended):

```bash
cmd lang        # fzf picker: English / Русский / 中文
```

Or set directly:

```bash
cmd lang en     # English
cmd lang ru     # Русский
cmd lang zh     # 中文
```

Or `export CMD_LANG=en` — saved in `~/.cmd/config.json`.

The browser header also shows: `Lang: cmd lang`

## Hotkeys

On the **zsh input line** only:

| Key | Action |
|-----|--------|
| **Ctrl+O** | Open browser |
| **F2** | Open browser (fallback) |

`cmd-keys` — list bindings

## Commands

| Command | Description |
|---------|-------------|
| `cmd` | fzf browser |
| `cmd ls` | Command card |
| `cmd copy` | Search by keyword |
| `cmd related ls` | Related commands |
| `cmd --copy ls` | Copy first example |
| `cmd --all` | Include all system commands |
| `cmd index` | Rebuild macOS index |
| `cmd edit name` | Personal card |
| `cmd lang` | Language menu (fzf) |
| `cmd lang en\|ru\|zh` | Set language directly |
| `cmd --version` | Show version |

**Browser:** Enter = card · Ctrl+E = example · Esc = close

## Repository structure

```
cmd/                              # https://github.com/godshiba/cmd
├── .github/
│   └── ISSUE_TEMPLATE/           # bug & feature templates
├── CHANGELOG.md                  # release history
├── LICENSE                       # MIT
├── README.md                     # English (default)
├── README.ru.md                  # Russian
├── README.zh-CN.md               # Chinese
├── VERSION                       # 1.0.0
├── cmd                           # CLI entry (bash → python)
├── main.py                       # argument routing
├── data/
│   ├── locales/
│   │   ├── en/                   # UI + cards (English)
│   │   ├── ru/                   # UI + cards (Russian)
│   │   └── zh/                   # UI + cards (Chinese)
│   ├── essential.json            # legacy fallback
│   ├── categories.json
│   └── useful_system.json
├── lib/
│   ├── i18n.py                   # language system
│   ├── browser.py                # fzf browser
│   ├── lookup.py                 # search & resolve
│   ├── display.py                # card formatting
│   ├── index.py                  # apropos indexer
│   └── version.py
└── shell/
    └── cmd.widget.zsh            # Ctrl+O, F2

~/.cmd/                           # user data (created on first run)
├── config.json                   # language
├── index.json                    # system index
├── custom.json                   # your cards
└── history.json                  # recent commands
```

## Changelog & license

- [CHANGELOG.md](CHANGELOG.md) — version history
- [Releases](https://github.com/godshiba/cmd/releases) — tagged builds
- [MIT License](LICENSE)