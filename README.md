# findcmd

**Личный навигатор по командам терминала для macOS.**  
Помогает не теряться среди команд: что делает, зачем нужна, примеры — на русском.

> Personal terminal command navigator for macOS beginners. Russian cards + auto-indexed system commands.

## Зачем

- Забыл команду → `findcmd ls` → карточка с примерами
- Не знаешь имя → `findcmd копир` → поиск по смыслу
- Много команд → браузер с **группировкой** и **подкатегориями**
- Быстро вставить пример → **Ctrl+`** в терминале

## Быстрый старт

### 1. Зависимости

```bash
brew install fzf
```

### 2. Установка

```bash
git clone https://github.com/YOUR_USERNAME/findcmd.git ~/scripts/findcmd
cd ~/scripts/findcmd
./findcmd index
```

### 3. PATH

Добавь в `~/.zshrc`:

```bash
export PATH="$HOME/scripts/findcmd:$PATH"
```

### 4. Горячая клавиша (zsh)

```bash
source "$HOME/scripts/findcmd/shell/findcmd.widget.zsh"
```

| Клавиша | Действие |
|---------|----------|
| **Ctrl+O** или **Ctrl+G** | Открыть браузер findcmd |
| **F2** | Браузер (запасной вариант) |
| **Ctrl+`** | Команда → пример → вставить в строку |

Проверить привязки: `findcmd-keys`

**Важно:** шорткаты работают только на **строке ввода** zsh (когда видишь `%` и курсор).

Перезагрузи shell:

```bash
source ~/.zshrc
```

**Ctrl+` не срабатывает?** Некоторые терминалы перехватывают эту клавишу (новое окно).
Отключи шорткат в настройках Terminal/iTerm или раскомментируй в `shell/findcmd.widget.zsh`:

```zsh
bindkey '^ ' findcmd-widget   # Ctrl+Space
```

## Использование

| Команда | Описание |
|---------|----------|
| `findcmd` | Браузер: Essential → Recent → Useful |
| `findcmd ls` | Карточка команды |
| `findcmd копир` | Поиск по русским тегам и описанию |
| `findcmd related ls` | Связанные команды (cd, pwd…) |
| `findcmd --copy ls` | Скопировать первый пример в буфер |
| `findcmd --pick-example ls` | Выбрать пример (Enter / Ctrl-Y) |
| `findcmd --all` | + все 1200+ системных команд |
| `findcmd index` | Обновить индекс macOS |
| `findcmd edit docker` | Своя карточка |

### В браузере (fzf)

- **Enter** — открыть карточку
- **Ctrl+E** — выбрать пример (вставить / скопировать)
- Группы: `Основные · Навигация → Перемещение`

## Уровни команд

| Уровень | Иконка | Откуда |
|---------|--------|--------|
| Essential | ⭐ | 32 русские карточки (`data/essential.json`) |
| Recent | 🕐 | История просмотров (`~/.findcmd/history.json`) |
| Useful | ✦ | ~70 полезных системных (`data/useful_system.json`) |
| System | 💻 | Полный индекс macOS (`findcmd index`) |

## Структура

```
findcmd/
├── findcmd                 # точка входа
├── main.py
├── data/
│   ├── essential.json      # русские карточки
│   ├── useful_system.json  # полезные системные
│   └── categories.json     # категории и подкатегории
├── lib/
├── shell/
│   └── findcmd.widget.zsh  # горячие клавиши zsh
└── ~/.findcmd/
    ├── index.json
    ├── custom.json
    └── history.json
```

## Добавить свою карточку

```bash
findcmd edit mytool
```

Откроется `~/.findcmd/custom.json`. Пример поля:

```json
{
  "name": "mytool",
  "category": "dev",
  "subcategory": "tools",
  "title": "Мой инструмент",
  "what": "Что делает",
  "when": "Когда использовать",
  "examples": [{"cmd": "mytool run", "desc": "Запуск"}],
  "related": ["git", "brew"],
  "tags": ["мой", "проект"]
}
```

## Contributing

1. Fork → branch → PR
2. Новые Essential-команды → `data/essential.json`
3. Полезные системные → `data/useful_system.json`

## License

MIT — see [LICENSE](LICENSE)