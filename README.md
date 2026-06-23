# cmd

Навигатор по командам терминала для macOS. Карточки на русском, примеры, группировка, поиск.

**cmd** — короткая команда в терминале. Репозиторий называется `findcmd` (исторически).

## Зачем

| Ситуация | Решение |
|----------|---------|
| Забыл команду | `cmd ls` → карточка с примерами |
| Не знаешь имя | `cmd копир` → поиск по смыслу |
| Много всего | `cmd` → браузер с группами |
| Быстро из shell | **Ctrl+O** или **F2** |

## Установка

**Зависимость:** [fzf](https://github.com/junegunn/fzf)

```bash
brew install fzf
git clone https://github.com/danilsmely/cmd.git ~/scripts/findcmd
cd ~/scripts/findcmd
./cmd index
```

Добавь в `~/.zshrc`:

```bash
unalias cmd 2>/dev/null
export PATH="$HOME/scripts/findcmd:$PATH"
source "$HOME/scripts/findcmd/shell/cmd.widget.zsh"
```

Перезагрузи shell:

```bash
source ~/.zshrc
```

## Горячие клавиши

Работают только на **строке ввода** zsh (промпт `%`).

| Клавиша | Действие |
|---------|----------|
| **Ctrl+O** | Открыть браузер |
| **F2** | То же (запасной) |

Проверка: `cmd-keys`

## Команды

| Команда | Описание |
|---------|----------|
| `cmd` | Браузер: Essential → Recent → Useful |
| `cmd ls` | Карточка команды |
| `cmd копир` | Поиск по тегам и описанию |
| `cmd related ls` | Связанные команды |
| `cmd --copy ls` | Скопировать первый пример |
| `cmd --all` | + все системные команды |
| `cmd index` | Обновить индекс macOS |
| `cmd edit docker` | Своя карточка |

### В браузере (fzf)

- **Enter** — карточка команды
- **Ctrl+E** — выбрать пример
- Группы: `Основные · Навигация → Перемещение`

## Уровни данных

| Уровень | Иконка | Источник |
|---------|--------|----------|
| Essential | ⭐ | `data/essential.json` — 32 русские карточки |
| Recent | 🕐 | `~/.cmd/history.json` |
| Useful | ✦ | `data/useful_system.json` |
| System | 💻 | Индекс macOS (`cmd index`) |

## Структура

```
findcmd/
├── cmd                 # CLI
├── main.py
├── data/
├── lib/
├── shell/
│   └── cmd.widget.zsh  # Ctrl+O, F2
└── ~/.cmd/             # индекс, история, свои карточки
```

> При первом запуске данные из старого `~/.findcmd/` переносятся в `~/.cmd/` автоматически.

## Своя карточка

```bash
cmd edit mytool
```

Редактируется `~/.cmd/custom.json`.

## License

MIT — [LICENSE](LICENSE)