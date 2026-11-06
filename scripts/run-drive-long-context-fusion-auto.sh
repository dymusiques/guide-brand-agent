#!/usr/bin/env bash
# Fully automatic Drive fusion: no Owner goal retype.
# ceo_dispatch after screen · pre_delivery before evolution gap / 定稿.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"

PHASE="${DRIVE_FUSION_PHASE:-full}"
BRIEF="${CEO_SIX_CASE_BRIEF:-${CEO_OWNER_EXTRA_BRIEF:-}}"
EXTRA=()
[[ -n "${1:-}" ]] && EXTRA=("$@")

if [[ " ${EXTRA[*]:-} " == *" --brief "* ]]; then
  :
elif [[ -n "$BRIEF" ]]; then
  EXTRA+=(--brief "$BRIEF")
fi

exec "$PY" scripts/build-drive-long-context-fusion.py --auto --phase "$PHASE" "${EXTRA[@]}"
