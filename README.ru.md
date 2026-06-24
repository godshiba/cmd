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
- [Язык приложения](#язык-приложения)
- [Горячие клавиши](#горячие-клавиши)
- [Команды](#команды)
- [Структура репозитория](#структура-репозитория)
- [Журнал изменений и лицензия](#журнал-изменений-и-лицензия)

---

## Что это

`cmd` — **личный справочник команд** в терминале:

- **Карточки** — что делает команда, когда нужна, когда нет
- **Примеры** — готовые команды (`ls -la`, `cd ..`, …)
- **Браузер** — Essential → Recent → Useful, поиск через fzf
- **Горячие клавиши** — Ctrl+O / F2 из строки zsh

Не заменяет `man`. Помогает **быстрее находить и запоминать** команды.

## Требования

| Компонент | Версия | Примечание |
|-----------|--------|------------|
| **macOS** | 13+ | Индекс через `apropos` |
| **Python** | 3.9+ | Только stdlib |
| **zsh** | 5.8+ | Стандартная оболочка |
| **fzf** | 0.30+ | `brew install fzf` — нужен для браузера |
| **Terminal** | любой | Горячие клавиши работают в строке ввода zsh |

```bash
sw_vers                    # macOS
python3 --version          # Python 3.9+
zsh --version              # zsh 5.8+
fzf --version              # fzf 0.30+
cmd --version              # cmd 0.1.0
```

## Установка

```bash
brew install fzf
git clone https://github.com/godshiba/cmd.git ~/scripts/cmd
cd ~/scripts/cmd
bash install.sh
./cmd index
```

`~/.zshrc`:

```bash
unalias cmd 2>/dev/null
export PATH="$HOME/scripts/cmd:$PATH"
source "$HOME/scripts/cmd/shell/cmd.widget.zsh"
```

```bash
source ~/.zshrc
cmd ls
cmd lang ru    # язык интерфейса
```

## Язык приложения

```bash
cmd lang        # меню выбора (fzf)
cmd lang ru     # сразу русский
cmd lang en     # English
cmd lang zh     # 中文
```

Или `export CMD_LANG=ru` — сохраняется в `~/.cmd/config.json`.

В браузере в шапке: `Язык: cmd lang`

## Горячие клавиши

| Клавиша | Действие |
|---------|----------|
| **Ctrl+O** | Браузер |
| **F2** | Браузер (запасной) |

`cmd-keys` — список привязок

## Команды

| Команда | Описание |
|---------|----------|
| `cmd` | Браузер fzf |
| `cmd ls` | Карточка команды |
| `cmd <запрос>` | Поиск по ключевому слову (напр. `cmd grep`) |
| `cmd related ls` | Связанные команды |
| `cmd --pick` | Выбор команды (виджет zsh) |
| `cmd --pick-example ls` | Выбор примера |
| `cmd --copy ls` | Скопировать первый пример |
| `cmd --all` | Все системные команды |
| `cmd index` | Пересобрать индекс macOS |
| `cmd edit имя` | Личная карточка |
| `cmd lang` | Меню языка (fzf) |
| `cmd lang en\|ru\|zh` | Язык напрямую |
| `cmd --version` | Версия |

**В браузере:** Enter — карточка · Ctrl+E — пример · Esc — закрыть

Полная документация на английском: [README.md](README.md)

## Структура репозитория

```
cmd/                              # https://github.com/godshiba/cmd
├── README.md / README.ru.md / README.zh-CN.md
├── VERSION                       # 0.1.0
├── install.sh                    # PATH и права
├── scripts/verify.sh             # локальные тесты
├── scripts/migrate_legacy.py     # перенос data/*.json → data/legacy/
├── scripts/capture_evidence.py   # артефакты проверки (CMD_SCRATCH)
├── tests/                        # smoke + evidence тесты
├── CHANGELOG.md, LICENSE
├── cmd, main.py
├── data/
│   ├── locales/{en,ru,zh}/       # основные данные
│   ├── legacy/                   # categories + useful fallback (см. LEGACY.md)
│   └── LEGACY.md
├── lib/, shell/cmd.widget.zsh
└── ~/.cmd/                       # config, index, custom, history
```

## Журнал изменений и лицензия

- [CHANGELOG.md](CHANGELOG.md)
- [Релизы](https://github.com/godshiba/cmd/releases)
- [MIT](LICENSE)