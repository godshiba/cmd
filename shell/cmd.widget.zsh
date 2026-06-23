# cmd — zsh widget (Ctrl+O / F2)
# source "$HOME/scripts/cmd/shell/cmd.widget.zsh"

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

_cmd_cleanup_legacy() {
  zle -D findcmd-open-widget 2>/dev/null
  zle -D findcmd-insert-widget 2>/dev/null
  local key
  for key in '^G' '^O' '^A' '^@' $'\x60' '^[[99~' ${terminfo[kf2]-}; do
    bindkey -r "$key" 2>/dev/null
  done
}
_cmd_cleanup_legacy

bindkey '^O' cmd-open-widget
if [[ -n ${terminfo[kf2]-} ]]; then
  bindkey "$terminfo[kf2]" cmd-open-widget
fi

_cmd_widget_msg() {
  local key=$1
  local lang=en
  if [[ -f "$HOME/.cmd/config.json" ]]; then
    lang=$(command python3 -c "import json;print(json.load(open('$HOME/.cmd/config.json')).get('lang','en'))" 2>/dev/null) || lang=en
  fi
  case $lang in
    ru)
      case $key in
        keys_title) echo "cmd — шорткаты zsh:" ;;
        ctrl_o) echo "  Ctrl+O  → браузер (основной)" ;;
        f2) echo "  F2      → браузер (запасной)" ;;
      esac ;;
    zh)
      case $key in
        keys_title) echo "cmd — zsh 快捷键:" ;;
        ctrl_o) echo "  Ctrl+O  → 浏览器 (主)" ;;
        f2) echo "  F2      → 浏览器 (备用)" ;;
      esac ;;
    *)
      case $key in
        keys_title) echo "cmd — zsh shortcuts:" ;;
        ctrl_o) echo "  Ctrl+O  → browser (primary)" ;;
        f2) echo "  F2      → browser (fallback)" ;;
      esac ;;
  esac
}

cmd-keys() {
  echo ""
  $(_cmd_widget_msg keys_title)
  bindkey | command grep cmd-open-widget
  echo ""
  $(_cmd_widget_msg ctrl_o)
  $(_cmd_widget_msg f2)
}