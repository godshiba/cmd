# findcmd zsh widgets
# source "$HOME/scripts/findcmd/shell/findcmd.widget.zsh"

findcmd-widget() {
  emulate -L zsh
  setopt localoptions noshwords

  # Обязательно: отпустить терминал перед интерактивным fzf
  zle -I

  local name example
  name=$(command findcmd --pick) || return 0
  [[ -z "$name" ]] && return 0

  example=$(command findcmd --pick-example "$name") || return 0
  [[ -z "$example" ]] && return 0

  BUFFER="$example"
  CURSOR=${#BUFFER}
  zle -M "findcmd: $example"
  zle redisplay
}

findcmd-open-widget() {
  emulate -L zsh
  zle -I
  command findcmd
  zle redisplay
}

zle -N findcmd-widget
zle -N findcmd-open-widget

# Ctrl+` — выбрать команду → пример → вставить в строку
# \C-` и ^` — два варианта для разных терминалов
bindkey '\C-`' findcmd-widget
bindkey '^`' findcmd-widget

# Ctrl+G — открыть браузер (без вставки)
bindkey '^G' findcmd-open-widget

# Запасной вариант, если Ctrl+` перехватывает Terminal/iTerm:
# bindkey '^ ' findcmd-widget   # Ctrl+Space