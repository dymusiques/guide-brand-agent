#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
fail=0
ok() { echo "PASS $1"; }
bad() { echo "FAIL $1"; fail=1; }

PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="python3"

[[ -f "$ROOT/docs/OWNER-PENDING-VIDEOS-EVAL-SOP.md" ]] && ok SOP || bad SOP
[[ -f "$ROOT/integration/handoff/owner-pending-videos-pipeline.json" ]] && ok pipeline.json || bad pipeline.json
[[ -f "$ROOT/scripts/pending_video_md_lib.py" ]] && ok md_lib || bad md_lib
[[ -f "$ROOT/scripts/build-owner-pending-videos-facts-manifest.py" ]] && ok facts_manifest_py || bad facts_manifest_py
[[ -f "$ROOT/scripts/agent-gate-pending-videos-advice.py" ]] && ok advice_gate || bad advice_gate
[[ -f "$ROOT/scripts/pending_videos_gate_policy.py" ]] && ok gate_policy || bad gate_policy
[[ -f "$ROOT/scripts/assert-pending-videos-advice-gate.py" ]] && ok assert_gate || bad assert_gate
[[ -f "$ROOT/scripts/agent-brainstorm-preflight.py" ]] && ok brainstorm_preflight || bad brainstorm_preflight
[[ -f "$ROOT/scripts/verify-xhs-analytics-freshness.py" ]] && ok xhs_freshness || bad xhs_freshness
[[ -x "$ROOT/scripts/run-owner-pending-videos-eval.sh" ]] && ok run.sh || bad run.sh
[[ -f "$ROOT/scripts/evaluate-owner-pending-videos.py" ]] && ok evaluate.py || bad evaluate.py
[[ -f "$ROOT/scripts/build-owner-pending-videos-eval-html.py" ]] && ok build-html.py || bad build-html.py
[[ -f "$ROOT/content/xiaohongshu/inbox/pending-videos/TEMPLATE.md" ]] && ok TEMPLATE || bad TEMPLATE

rg -q 'L2d_PENDING_VIDEOS_EVAL' "$ROOT/integration/handoff/workflow-automation-manifest.json" \
  && ok manifest-L2d || bad manifest-L2d
rg -q 'run-owner-pending-videos-eval' "$ROOT/scripts/run_ceo_full_execution.py" \
  && ok ceo-hook || bad ceo-hook
rg -q 'agent-gate-pending-videos-advice' "$ROOT/integration/handoff/owner-pending-videos-pipeline.json" \
  && ok pipeline-gate || bad pipeline-gate
rg -q 'build-owner-pending-videos-facts-manifest' "$ROOT/scripts/run-owner-pending-videos-eval.sh" \
  && ok run-facts-gate || bad run-facts-gate

if [[ -f "$ROOT/integration/handoff/owner-pending-videos-eval-latest.json" ]]; then
  "$PY" - <<'PY' || bad eval-json-schema
import json
import sys
from pathlib import Path
ROOT = Path(".")
data = json.loads((ROOT / "integration/handoff/owner-pending-videos-eval-latest.json").read_text())
sm = data.get("scoring_model", "")
if not str(sm).startswith("rule-v2-full-body"):
    sys.exit("scoring_model")
for it in data.get("items") or []:
    if "narrative_facts" not in it:
        sys.exit(f"no narrative_facts {it.get('id')}")
    if "decision_summary" not in it:
        sys.exit(f"no decision_summary {it.get('id')}")
    if it.get("body_preview"):
        sys.exit("body_preview must be removed")
    hg = it.get("human_glance_only") or {}
    if not hg.get("not_for_decisions"):
        sys.exit("human_glance_only.not_for_decisions")
PY
  [[ $? -eq 0 ]] && ok eval-json-schema || true
else
  bad eval-json-missing
fi

if [[ -f "$ROOT/integration/handoff/owner-pending-videos-facts-latest.json" ]]; then
  "$PY" - <<'PY' || bad facts-json-schema
import json
import sys
from pathlib import Path
ROOT = Path(".")
data = json.loads((ROOT / "integration/handoff/owner-pending-videos-facts-latest.json").read_text())
if data.get("facts_source") != "content/xiaohongshu/inbox/pending-videos/*.md":
    sys.exit("facts_source")
for it in data.get("items") or []:
    if "decision_summary" not in it or "sha256" not in it:
        sys.exit("item fields")
PY
  [[ $? -eq 0 ]] && ok facts-json-schema || true
else
  bad facts-json-missing
fi

"$PY" scripts/agent-gate-pending-videos-advice.py --no-refresh >/dev/null 2>&1 && ok advice-gate-pass || bad advice-gate-pass

exit "$fail"
