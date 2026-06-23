# cmd

**Навигатор по командам терминала для macOS** — карточки, примеры, браузер, горячие клавиши.

<p align="center">
  <strong>Документация</strong>:
  <a href="README.md">English</a> ·
  <a href="README.ru.md"><b>Русский</b></a> ·
  <a href="README.zh-CN.md">中文</a>
</p>

<p align="center">
  <a href="https://github.com/godshiba/cmd/releases"><img src="https://img.shields.io/github/v/release/godshiba/cmd?style=flat-square" alt="Release"></a>
  <img src="https://img.shields.io/badge/platform-macOS%2013+-000?style=flat-square" alt="macOS">
  <img src="https://img.shields.io/badge/python-3.9+-3776ab?style=flat-square" alt="Python">
  <img src="https://img.shields.io/badge/shell-zsh%205.8+-89b4fa?style=flat-square" alt="zsh">
  <img src="https://img.shields.io/badge/fzf-0.30+-fb4934?style=flat-square" alt="fzf">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT">
</p>

---

## Содержание

- [Что это](#что-это)
- [Требования](#требования)
- [Установка](#установка)
- [Языки документации](#языки-документации)
- [Язык приложения](#язык-приложения)
- [Горячие клавиши](#горячие-клавиши)
- [Команды](#команды)
- [Структура репозитория](#структура-репозитория)
- [Changelog и лицензия](#changelog-и-лицензия)

---

## Что это

`cmd` — **личный справочник команд** в терминале: карточки, примеры, браузер fzf, Ctrl+O.

## Требования

| Компонент | Версия | Примечание |
|-----------|--------|------------|
| **macOS** | 13+ | Индекс через `apropos` |
| **Python** | 3.9+ | Только stdlib |
| **zsh** | 5.8+ | Стандартная оболочка |
| **fzf** | 0.30+ | `brew install fzf` |

```bash
sw_vers && python3 --version && zsh --version && fzf --version && cmd --version
```

## Установка

```bash
brew install fzf
git clone https://github.com/godshiba/cmd.git ~/scripts/cmd
cd ~/scripts/cmd && ./cmd index
```

`~/.zshrc`:

```bash
unalias cmd 2>/dev/null
export PATH="$HOME/scripts/cmd:$PATH"
source "$HOME/scripts/cmd/shell/cmd.widget.zsh"
```

## Языки документации

| Язык | Файл |
|------|------|
| English | [README.md](README.md) |
| **Русский** | [README.ru.md](README.ru.md) |
| 中文 | [README.zh-CN.md](README.zh-CN.md) |

Ссылки:
- https://github.com/godshiba/cmd/blob/main/README.ru.md

## Язык приложения

```bash
cmd lang        # меню выбора (fzf)
cmd lang ru     # сразу русский
```

В браузере в шапке: `Язык: cmd lang`

## Горячие клавиши

| Клавиша | Действие |
|---------|----------|
| **Ctrl+O** | Браузер |
| **F2** | Браузер (запасной) |

## Команды

| Команда | Описание |
|---------|----------|
| `cmd` | Браузер |
| `cmd ls` | Карточка |
| `cmd копир` | Поиск |
| `cmd index` | Индекс macOS |
| `cmd lang` | Язык UI |
| `cmd --version` | Версия |

## Структура репозитория

```
cmd/                     → github.com/godshiba/cmd
├── README.md / .ru.md / .zh-CN.md
├── VERSION, CHANGELOG.md, LICENSE
├── cmd, main.py, data/, lib/, shell/
└── ~/.cmd/              → данные пользователя
```

## Changelog и лицензия

- [CHANGELOG.md](CHANGELOG.md)
- [Релизы](https://github.com/godshiba/cmd/releases)
- [MIT](LICENSE)