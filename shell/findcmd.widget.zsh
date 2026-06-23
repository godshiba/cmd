# findcmd zsh widgets
# source "$HOME/scripts/findcmd/shell/findcmd.widget.zsh"

# Запуск findcmd на реальном терминале (обязательно из zle-виджета)
_findcmd_tty() {
  FINDCMD_FROM_ZLE=1 command "$@" < /dev/tty > /dev/tty 2>&1
}

findcmd-open-widget() {
  emulate -L zsh
  zle -I
  _findcmd_tty findcmd
  zle reset-prompt
}

findcmd-insert-widget() {
  emulate -L zsh
  setopt localoptions noshwords
  zle -I

  local tmp name tmp2 example
  tmp=$(mktemp "${TMPDIR:-/tmp}/findcmd.pick.XXXXXX")
  tmp2=$(mktemp "${TMPDIR:-/tmp}/findcmd.example.XXXXXX")

  FINDCMD_PICK_OUT=$tmp _findcmd_tty findcmd --pick
  name=$(<"$tmp")
  rm -f "$tmp"
  [[ -z "$name" ]] && { zle reset-prompt; return 0 }

  FINDCMD_EXAMPLE_OUT=$tmp2 _findcmd_tty findcmd --pick-example "$name"
  example=$(<"$tmp2")
  rm -f "$tmp2"
  [[ -z "$example" ]] && { zle reset-prompt; return 0 }

  BUFFER="$example"
  CURSOR=${#BUFFER}
  zle -M "findcmd: $example"
  zle reset-prompt
}

zle -N findcmd-open-widget
zle -N findcmd-insert-widget

# Основные шорткаты (работают только на строке ввода zsh, не вне prompt)
bindkey '^O' findcmd-open-widget    # Ctrl+O — браузер
bindkey '^G' findcmd-open-widget    # Ctrl+G — браузер
bindkey '\C-`' findcmd-insert-widget  # Ctrl+` — вставить пример

# F2 — запасной вариант, если Ctrl+G/O перехватывает терминал
if [[ -n ${terminfo[kf2]-} ]]; then
  bindkey "$terminfo[kf2]" findcmd-open-widget
fi

# Показать привязки: findcmd-keys
findcmd-keys() {
  echo "findcmd шорткаты (на строке ввода zsh):"
  echo "  Ctrl+O / Ctrl+G / F2  → браузер findcmd"
  echo "  Ctrl+\`               → команда → пример → вставка"
  bindkey | command grep findcmd
}