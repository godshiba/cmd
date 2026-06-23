# cmd — zsh-виджет (Ctrl+O / F2)
# source "$HOME/scripts/findcmd/shell/cmd.widget.zsh"

_cmd_tty() {
  CMD_FROM_ZLE=1 command "$@" < /dev/tty > /dev/tty 2>&1
  return $?
}

cmd-open-widget() {
  emulate -L zsh
  zle -I
  _cmd_tty cmd
  zle reset-prompt
}

zle -N cmd-open-widget

# Снять старые привязки findcmd из предыдущих версий
_cmd_cleanup_legacy() {
  zle -D findcmd-open-widget 2>/dev/null
  zle -D findcmd-insert-widget 2>/dev/null
  local key
  for key in '^G' '^O' '^A' '^@' $'\x60' '^[[99~' ${terminfo[kf2]-}; do
    bindkey -r "$key" 2>/dev/null
  done
}
_cmd_cleanup_legacy

# Два шортката: основной и запасной
bindkey '^O' cmd-open-widget
if [[ -n ${terminfo[kf2]-} ]]; then
  bindkey "$terminfo[kf2]" cmd-open-widget
fi

cmd-keys() {
  echo ""
  echo "cmd — шорткаты zsh:"
  bindkey | command grep cmd-open-widget
  echo ""
  echo "  Ctrl+O  → браузер (основной)"
  echo "  F2      → браузер (запасной)"
}