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

# Рабочие привязки (zsh, не видны в настройках Terminal)
bindkey '^G' findcmd-open-widget
bindkey '^O' findcmd-insert-widget
bindkey '^@' findcmd-open-widget
bindkey '\C-`' findcmd-open-widget
bindkey '^`' findcmd-open-widget

# Если настроишь Terminal отправлять эту последовательность (см. findcmd-setup-grave)
bindkey '^[[99~' findcmd-open-widget

if [[ -n ${terminfo[kf2]-} ]]; then
  bindkey "$terminfo[kf2]" findcmd-open-widget
fi

# Пользовательская привязка из ~/.findcmd/bindkey (создаётся findcmd-detect-key)
[[ -f "$HOME/.findcmd/bindkey" ]] && source "$HOME/.findcmd/bindkey"

# Узнать, что реально приходит при нажатии клавиши
findcmd-detect-key() {
  emulate -L zsh 2>/dev/null
  echo ""
  echo "=== findcmd: детектор клавиш ==="
  echo "Нажми Ctrl+\` (или Ctrl+G для сравнения)."
  echo "Ctrl+C — выход."
  echo ""
  cat -v
  echo ""
  echo "Если при Ctrl+\` ничего не появилось — Terminal не передаёт клавишу в shell."
  echo "Запусти: findcmd-setup-grave"
}

# Настройка Ctrl+` через Terminal (когда клавиша не доходит до zsh)
findcmd-setup-grave() {
  cat <<'EOF'

=== Как привязать Ctrl+` ===

Почему Ctrl+G работает, а в настройках Terminal его нет?
  Ctrl+G ловит zsh (bindkey), а не Terminal.
  Настройки Terminal → Клавиатура показывают только действия Terminal,
  не шорткаты zsh.

Если Ctrl+` издаёт «квак» и findcmd-detect-key ничего не показывает:

1. Terminal → Настройки → Профили → Клавиатура
2. Нажми «+» (добавить)
3. В поле «Клавиша» нажми Ctrl+`
4. Действие: «Отправить текст» / «Send Text»
5. Вставь ровно это (без Enter в конце):

   ^[[99~

6. source ~/.zshrc
7. Ctrl+` должен открыть findcmd

Уже привязано в виджете: bindkey '^[[99~' findcmd-open-widget

Запасные без настройки: Ctrl+G, F2

EOF
}

findcmd-keys() {
  echo ""
  echo "findcmd — шорткаты zsh (не в настройках Terminal):"
  bindkey | command grep findcmd
  echo ""
  echo "  Ctrl+G / F2     → браузер"
  echo "  Ctrl+O          → вставить пример"
  echo "  Ctrl+\`         → браузер (если Terminal передаёт клавишу)"
  echo ""
  echo "Диагностика:  findcmd-detect-key"
  echo "Настройка \`:  findcmd-setup-grave"
}