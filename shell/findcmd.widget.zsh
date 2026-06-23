# findcmd zsh widget — Ctrl+` opens browser and inserts example
# Add to ~/.zshrc:
#   source "$HOME/scripts/findcmd/shell/findcmd.widget.zsh"

findcmd-widget() {
  emulate -L zsh
  setopt localoptions noshwords

  local name example
  name=$(command findcmd --pick 2>/dev/null) || return 0
  [[ -z "$name" ]] && return 0

  example=$(command findcmd --pick-example "$name" 2>/dev/null) || return 0
  [[ -z "$example" ]] && return 0

  BUFFER="$example"
  CURSOR=${#BUFFER}
  zle redisplay
}

findcmd-open-widget() {
  emulate -L zsh
  command findcmd 2>/dev/null
  zle redisplay
}

zle -N findcmd-widget
zle -N findcmd-open-widget

# Ctrl+` — выбрать команду и вставить пример в строку
bindkey '^`' findcmd-widget

# Ctrl+G — только открыть браузер (без вставки)
bindkey '^G' findcmd-open-widget