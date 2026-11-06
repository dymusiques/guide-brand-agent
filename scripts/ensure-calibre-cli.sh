#!/usr/bin/env bash
# Install Calibre (cask) if missing; symlink ebook-convert into ~/.local/bin for PATH.
set -euo pipefail

CAL_APP="/Applications/calibre.app/Contents/MacOS/ebook-convert"
LOCAL_BIN="${HOME}/.local/bin"

install_cask() {
  if command -v brew >/dev/null 2>&1; then
    HOMEBREW_NO_AUTO_UPDATE=1 brew install --cask calibre
  else
    echo "FAIL: Homebrew not found — install Calibre from https://calibre-ebook.com/download" >&2
    return 1
  fi
}

if [[ ! -x "$CAL_APP" ]]; then
  install_cask
fi

if [[ ! -x "$CAL_APP" ]]; then
  echo "FAIL: Calibre not at $CAL_APP" >&2
  exit 1
fi

mkdir -p "$LOCAL_BIN"
ln -sf "$CAL_APP" "$LOCAL_BIN/ebook-convert"
ln -sf "/Applications/calibre.app/Contents/MacOS/ebook-meta" "$LOCAL_BIN/ebook-meta" 2>/dev/null || true

echo "OK: ebook-convert -> $LOCAL_BIN/ebook-convert"
if [[ ":${PATH}:" != *":${LOCAL_BIN}:"* ]]; then
  echo "HINT: add to ~/.zshrc: export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

"$LOCAL_BIN/ebook-convert" --version | head -1
