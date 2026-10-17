#!/usr/bin/env bash
# Full integration build — 00 Manager capstone.
# Tiers: docs/VERIFY-TIERS.md
# Usage:
#   VERIFY_TIER=release bash scripts/verify-all.sh
#   VERIFY_TIER=ci bash scripts/verify-all.sh
#   bash scripts/verify-all.sh --brief content/xiaohongshu/foo-brief.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh
BRIEF=""
if [[ "${1:-}" == "--brief" ]]; then
  BRIEF="${2:-}"
fi

VERIFY_TIER="${VERIFY_TIER:-release}"
if [[ "$VERIFY_TIER" == "ci" ]]; then
  SKIP_GEMINI="${SKIP_GEMINI:-1}"
else
  SKIP_GEMINI="${SKIP_GEMINI:-0}"
fi
SKIP_PLATFORM="${SKIP_PLATFORM:-0}"
FAIL=0

step() {
  local title="$1"
  shift
  echo ""
  echo "######## $title ########"
  if "$@"; then
    echo ">>> $title: PASS"
  else
    echo ">>> $title: FAIL"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== verify-all tier: $VERIFY_TIER (SKIP_GEMINI=$SKIP_GEMINI) ==="

step "L0 handoff" bash scripts/verify-handoff.sh

step "Goal registry + Agent matrix (10×6)" bash scripts/verify-agent-matrix.sh

step "M4 · Goal verify hooks" bash scripts/verify-goals.sh

if [[ "$SKIP_PLATFORM" == "1" ]]; then
  echo ""
  echo "######## Platform 6 (SKIP_PLATFORM=1) ########"
  echo ">>> SKIP"
else
  step "Platform integration 6 (gdocs/Drive/Git)" bash scripts/verify-integration.sh
fi

if [[ "$SKIP_GEMINI" == "1" ]] || { [[ ! -f .env ]] && [[ -z "${GEMINI_API_KEY:-}" ]]; }; then
  echo ""
  echo "######## Gemini suites (skipped — CI tier or no key) ########"
  echo ">>> SKIP XHS 05 + strategic 02/03 (offline matrix still ran in agent step)"
else
  step "05 · XHS kernel Gemini 6" bash scripts/verify-xhs-topic.sh
  step "02 · Business brand static + Gemini 6" bash scripts/verify-business-brand.sh
  step "03 · Marketing campaign static + Gemini 6" bash scripts/verify-marketing-campaign.sh
fi

step "Analytics 09 demo pipeline" bash scripts/analytics-pipeline.sh --demo

export VERIFY_SKIP_INTEGRATION_MATRIX=1
if [[ -n "$BRIEF" ]]; then
  step "Manager workflow + Brief gate" bash scripts/manager-workflow-verify.sh "$BRIEF"
else
  step "Manager workflow (no Brief path)" bash scripts/manager-workflow-verify.sh
fi

if [[ "${VERIFY_STRICT_BRIEFS:-0}" == "1" ]] && [[ "$SKIP_GEMINI" != "1" ]]; then
  brief_count=$(find content/xiaohongshu -maxdepth 1 -name '*-brief.md' 2>/dev/null | wc -l | tr -d ' ')
  step "XHS content-dir batch ($brief_count briefs)" bash scripts/verify-xhs-content-dir.sh
fi

if [[ "${VERIFY_STRICT_STRATEGIC:-0}" == "1" ]] && [[ "$SKIP_GEMINI" != "1" ]]; then
  PY=".venv/bin/python"
  step "02/03 strict strategic deliverables" bash -c '
    set -euo pipefail
    shopt -s nullglob
    for f in content/business-brand/*.md; do
      [[ "$(basename "$f")" == "README.md" ]] && continue
      "$PY" scripts/lint-strategic-doc.py --kind business_brand --file "$f"
      "$PY" scripts/evaluate-business-brand.py --file "$f"
    done
    for f in content/marketing/*.md; do
      [[ "$(basename "$f")" == "README.md" ]] && continue
      "$PY" scripts/lint-strategic-doc.py --kind marketing --file "$f"
      "$PY" scripts/evaluate-marketing-campaign.py --file "$f"
    done
  '
fi

echo ""
echo "=== verify-all summary (tier=$VERIFY_TIER) ==="
if [[ "$FAIL" -gt 0 ]]; then
  echo "RESULT: FAIL — $FAIL step(s) failed"
  exit 1
fi
echo "RESULT: PASS — integration build (00 Manager capstone)"
echo "See docs/VERIFY-TIERS.md for CI vs Release semantics."

DERIVED="$ROOT/content/analytics/derived"
mkdir -p "$DERIVED"
PY=""
if [[ -x .venv/bin/python ]]; then PY=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then PY="python3"; fi
if [[ -n "$PY" ]]; then
  VERIFY_TIER="$VERIFY_TIER" DERIVED="$DERIVED" "$PY" - <<'PY' || true
import json, os
from datetime import datetime
from pathlib import Path
derived = Path(os.environ["DERIVED"])
p = derived / ".manager-dashboard-state.json"
p.write_text(json.dumps({
    "last_verify_all": {
        "at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "tier": os.environ.get("VERIFY_TIER", "?"),
        "result": "PASS",
    }
}, ensure_ascii=False, indent=2), encoding="utf-8")
PY
fi
bash scripts/manager-dashboard.sh >/dev/null 2>&1 || true
