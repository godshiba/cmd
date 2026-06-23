#!/usr/bin/env bash
set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"

chmod +x "$DIR/cmd"
mkdir -p "$HOME/bin"
ln -sf "$DIR/cmd" "$HOME/bin/cmd"

echo "✓ cmd установлен:"
echo "  $DIR/cmd"
echo "  $HOME/bin/cmd → $DIR/cmd"
echo ""
echo "Проверка:"
"$DIR/cmd" --version
echo ""
echo "Добавь в ~/.zshrc (если ещё нет):"
echo '  export PATH="$HOME/scripts/cmd:$PATH"'
echo '  source "$HOME/scripts/cmd/shell/cmd.widget.zsh"'
echo ""
echo "Затем: source ~/.zshrc"