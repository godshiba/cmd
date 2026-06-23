# findcmd zsh widgets
# source "$HOME/scripts/findcmd/shell/findcmd.widget.zsh"

_findcmd_tty() {
  FINDCMD_FROM_ZLE=1 command "$@" < /dev/tty > /dev/tty 2>&1
  return $?
}

findcmd-open-widget() {
  emulate -L zsh
  zle -I
  _findcmd_tty findcmd
  zle reset-prompt
}

findcmd-insert-widget() {
  emulate -L zsh
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

# Ctrl+` на Mac часто приходит как ^@ (не \C-`)
bindkey '^@' findcmd-open-widget
bindkey '\C-`' findcmd-open-widget
bindkey '^`' findcmd-open-widget

# Ctrl+O — вставить пример (сначала выбор команды, потом примера)
bindkey '^O' findcmd-insert-widget

# Запасные
bindkey '^G' findcmd-open-widget
if [[ -n ${terminfo[kf2]-} ]]; then
  bindkey "$terminfo[kf2]" findcmd-open-widget
fi

findcmd-keys() {
  echo "findcmd шорткаты (на строке ввода zsh):"
  echo "  Ctrl+\`  → браузер (на Mac часто = Ctrl+@)"
  echo "  Ctrl+O   → команда → пример → вставка"
  echo "  Ctrl+G / F2 → браузер (запасные)"
  echo ""
  echo "Если Ctrl+\` не работает (звук «квак»):"
  echo "  Terminal → Настройки → Клавиатура → отключи шорткат на Ctrl+\`"
  echo "  или используй Ctrl+G"
  bindkey | command grep findcmd
}