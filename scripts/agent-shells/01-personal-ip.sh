#!/usr/bin/env bash
# Agent 01 — validate IP brief scope markers (no Gemini).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
IP="$ROOT/content/personal-ip/ip-positioning-brief-2026-10-05.md"
if [[ "${1:-}" == "--check" ]]; then
  PY="$ROOT/.venv/bin/python"
  [[ -x "$PY" ]] || PY="python3"
  exec "$PY" "$ROOT/scripts/evaluate_personal_ip.py" --check
fi
echo "=== Agent 01 personal-ip shell ==="
grep -E "品牌合作范围|不单品类绑定|三支柱" "$IP" | head -5
echo "RESULT: PASS — IP brief markers present"
