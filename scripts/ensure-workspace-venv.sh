#!/usr/bin/env bash
# Source from Agent shell before IP skill CLIs (voice-lora, bili-upload, …).
# Usage: source scripts/ensure-workspace-venv.sh
set -euo pipefail
_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
_ACTIVATE="$_ROOT/.venv/bin/activate"
if [[ ! -f "$_ACTIVATE" ]]; then
  echo "ensure-workspace-venv: missing $_ROOT/.venv — run SETUP.md §2 first" >&2
  return 1 2>/dev/null || exit 1
fi
# shellcheck disable=SC1090
source "$_ACTIVATE"
export PATH="$_ROOT/.venv/bin:$PATH"
export VIRTUAL_ENV="$_ROOT/.venv"
