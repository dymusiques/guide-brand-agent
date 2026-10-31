#!/usr/bin/env bash
# All XHS briefs: ensure redteam-pre + complete gate (kernel once). Unattended · no Owner.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"

if [[ ! -f .env ]] && [[ -z "${GEMINI_API_KEY:-}" ]]; then
  echo "SKIP manager-xhs-briefs-auto-pipeline — no GEMINI_API_KEY"
  exit 0
fi

echo "=== manager-xhs-briefs-auto-pipeline ==="
FAIL=0
"$PY" scripts/ensure-redteam-pre.py --all
"$PY" scripts/run-xhs-brief-adversarial-challenge.py --all || FAIL=$((FAIL + 1))
shopt -s nullglob
briefs=("$ROOT/content/xiaohongshu"/*-brief.md)
shopt -u nullglob
n=${#briefs[@]}
i=0
for b in "${briefs[@]}"; do
  i=$((i + 1))
  rel="${b#"$ROOT/"}"
  if [[ "$i" -lt "$n" ]]; then
    set +e
    "$PY" scripts/evaluate-xhs-brief-complete.py --brief "$rel" --skip-kernel-six
    ec=$?
    set -e
  else
    set +e
    "$PY" scripts/evaluate-xhs-brief-complete.py --brief "$rel"
    ec=$?
    set -e
  fi
  if [[ "$ec" -ne 0 ]]; then
    echo ">>> FAIL $rel — auto reroute"
    # Batch = first mechanical reroute per brief (not multi-round gate loop); round tracked in gate-loop only
    "$PY" scripts/ceo-auto-fix-brief.py --brief "$rel" --round "${CEO_FIX_ROUND:-1}" || true
    FAIL=$((FAIL + 1))
  fi
done

# kernel 6 once if any briefs
if [[ "$n" -gt 0 ]]; then
  bash scripts/verify-xhs-topic.sh || FAIL=$((FAIL + 1))
fi

"$PY" scripts/seo-lint-xhs-briefs.py || true

if [[ "$FAIL" -gt 0 ]]; then
  "$PY" scripts/ceo-action-needed-refresh.py || true
  echo "RESULT: FAIL ($FAIL brief(s)) — Cursor CEO should GM-loop; Owner not asked"
  echo "Read: content/evolution/00-manager/ceo-inbox/ceo-action-needed.md"
  exit 1
fi
echo "RESULT: PASS — all briefs complete gate"
exit 0
