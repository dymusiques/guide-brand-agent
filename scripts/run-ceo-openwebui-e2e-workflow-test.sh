#!/usr/bin/env bash
# E2E: CEO goal → Open WebUI Router → outbox + job → handoff record → lightweight sub-agent verifies.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SOURCE="$ROOT/content/personal-ip/intake/2026-10-29-e2e-kpi-longform-source.md"
REPORT="$ROOT/content/evolution/00-manager/ceo-inbox/CEO-OPENWEBUI-E2E-TEST-$(date +%Y-%m-%d).md"
HANDOFF="$ROOT/integration/handoff/e2e-openwebui-workflow-test-latest.json"
MIN_OUTBOX_CHARS="${MIN_OUTBOX_CHARS:-400}"

GOAL='E2E workflow test：基于 personal-ip intake（KPI Publish×法派长笛跨界），产出 LinkedIn 系列深度口播分节大纲；须结合 brand-ip-knowledge 事实，长文结构化输出'

FAIL=0
note() { echo ">>> $*"; }
pass() { echo "PASS: $*"; }
fail() { echo "FAIL: $*"; FAIL=$((FAIL + 1)); }

note "0 · prerequisites"
[[ -f "$SOURCE" ]] && pass "intake source" || fail "missing intake source"

if bash scripts/verify-openwebui-ceo-router.sh >/tmp/owui-verify.log 2>&1; then
  pass "verify-openwebui-ceo-router"
else
  cat /tmp/owui-verify.log
  fail "verify-openwebui-ceo-router"
fi

note "−1 · Open WebUI Router (CEO AUTO-WORKFLOW step −1)"
if bash scripts/run-openwebui-router-pipeline.sh --goal "$GOAL" --platform personal_ip --intake "$SOURCE" 2>&1 | tee /tmp/owui-pipeline.log; then
  pass "run-openwebui-router-pipeline"
else
  fail "run-openwebui-router-pipeline"
fi

ROUTE="$(python3 -c "
import re
t=open('/tmp/owui-pipeline.log').read()
m=re.search(r'\"route\":\s*\"(\w+)\"', t)
print(m.group(1) if m else 'UNKNOWN')
")"
[[ "$ROUTE" != "SKIP" ]] && pass "route=$ROUTE (Open WebUI invoked)" || fail "unexpected SKIP"

JOB="$(python3 - <<PY
import json, re
from pathlib import Path
root = Path("$ROOT")
t = Path("/tmp/owui-pipeline.log").read_text()
job_path = None
for line in reversed(t.splitlines()):
    if "openwebui-jobs/" in line and line.strip().endswith(".json"):
        raw = line.split()[-1]
        p = Path(raw)
        job_path = p if p.is_absolute() else (root / p)
        break
if job_path is None:
    d = root / "integration/handoff/openwebui-jobs"
    jobs = sorted(d.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    job_path = jobs[0] if jobs else None
print(job_path.resolve() if job_path else "")
PY
)"

OUTBOX=""
JOB_STATUS=""
if [[ -n "$JOB" && -f "$JOB" ]]; then
  read -r OUTBOX JOB_STATUS < <(python3 -c "import json; j=json.load(open('$JOB')); print(j.get('outbox_md',''), j.get('status',''))")
  pass "job json: $JOB"
  if [[ "$JOB_STATUS" == "done" ]]; then
    pass "job status=done"
  else
    fail "job status=$JOB_STATUS (not done; stale outbox must not count as PASS)"
  fi
else
  fail "job json missing"
fi

if [[ -n "$OUTBOX" && -f "$OUTBOX" ]]; then
  CHARS=$(wc -c < "$OUTBOX" | tr -d ' ')
  if [[ "$CHARS" -ge "$MIN_OUTBOX_CHARS" ]]; then
    pass "outbox content ($CHARS chars): $OUTBOX"
  else
    fail "outbox too short ($CHARS < $MIN_OUTBOX_CHARS): $OUTBOX"
  fi
  if grep -qE '法派|长笛|LinkedIn|口播|跨界' "$OUTBOX"; then
    pass "outbox topical anchors (IP/flute/LinkedIn)"
  else
    fail "outbox missing IP/flute/LinkedIn anchors (intake/prompt drift)"
  fi
else
  fail "outbox path missing"
fi

note "0 · CEO dispatch record + sub-agent smoke verifies"
mkdir -p "$(dirname "$REPORT")"
export E2E_GOAL="$GOAL" E2E_ROUTE="$ROUTE" E2E_JOB="$JOB" E2E_OUTBOX="$OUTBOX" E2E_REPORT="$REPORT" E2E_HANDOFF="$HANDOFF" E2E_ROOT="$ROOT"
python3 <<'PY'
import json
import os
from datetime import datetime, timezone
from pathlib import Path

root = Path(os.environ["E2E_ROOT"])
goal = os.environ["E2E_GOAL"]
route = os.environ["E2E_ROUTE"]
job_path = Path(os.environ["E2E_JOB"]).resolve()
outbox = os.environ["E2E_OUTBOX"]
report = Path(os.environ["E2E_REPORT"])
handoff_path = Path(os.environ["E2E_HANDOFF"])

job = json.loads(job_path.read_text(encoding="utf-8")) if job_path.is_file() else {}
outbox_path = Path(outbox).expanduser().resolve()
outbox_chars = len(outbox_path.read_text(encoding="utf-8")) if outbox_path.is_file() else 0

report.write_text(
    f"""# CEO Open WebUI E2E Test · {datetime.now().strftime("%Y-%m-%d")}

## Owner 目标（原话）

{goal}

## 步 −1 · Router

| 项 | 值 |
|----|-----|
| route | **{route}** |
| job | `{job.get("slug", "")}` |
| outbox | `{job.get("outbox_md", outbox)}` |
| intake 源 | `content/personal-ip/intake/2026-10-29-e2e-kpi-longform-source.md` |

## 步 0 · Manager 计划（模拟派活）

| Agent | 动作 |
|-------|------|
| **01 personal-ip** | 核对 outbox 提纲 vs CAPSTONE / ip-positioning-brief |
| **04 xhs-topic-manager** | 若转小红书：三镜头 Brief v0（**不**直接发 outbox 终稿） |

## API Key 边界

- Open WebUI 段：**OpenRouter**
- CEO 后续改稿：**GEMINI_API_KEY**（`.env`）

## 下一步迭代

1. Manager 读 outbox → Brief / LinkedIn v0  
2. `manager-ceo-gate-one-round.sh --brief …`  
3. 可选：`bash scripts/ceo-workflow-test-round2-finish.sh`
""",
    encoding="utf-8",
)

handoff = {
    "version": 1,
    "test": "ceo-openwebui-e2e",
    "finished_at": datetime.now(timezone.utc).isoformat(),
    "goal": goal,
    "route": route,
    "source_md": "content/personal-ip/intake/2026-10-29-e2e-kpi-longform-source.md",
    "job_json": str(job_path.relative_to(root)) if job_path.is_file() else None,
    "job_status": job.get("status"),
    "outbox_md": str(outbox_path) if outbox_path.is_file() else (job.get("outbox_md") or outbox),
    "outbox_chars": outbox_chars,
    "ceo_report": str(report.relative_to(root)),
    "subagent_verifies": [],
}
handoff_path.write_text(json.dumps(handoff, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
PY
pass "CEO report: $REPORT"

for cmd in \
  "bash scripts/verify-workflow-automation.sh" \
  "SKIP_GEMINI=1 bash scripts/verify-agent-fused.sh --agent 01" \
  "SKIP_GEMINI=1 bash scripts/verify-agent-fused.sh --agent 04"; do
  note "$cmd"
  if eval "$cmd" >/tmp/e2e-sub.log 2>&1; then
    pass "$cmd"
    E2E_VERIFY_CMD="$cmd" E2E_HANDOFF="$HANDOFF" python3 -c "
import json, os
from pathlib import Path
p=Path(os.environ['E2E_HANDOFF'])
d=json.loads(p.read_text())
d.setdefault('subagent_verifies', []).append({'cmd': os.environ['E2E_VERIFY_CMD'], 'result': 'PASS'})
p.write_text(json.dumps(d, indent=2, ensure_ascii=False)+'\n')
"
  else
    tail -20 /tmp/e2e-sub.log
    fail "$cmd"
  fi
done

if [[ "$FAIL" -gt 0 ]]; then
  echo "RESULT: FAIL ceo-openwebui-e2e-workflow-test ($FAIL)"
  exit 1
fi
echo "RESULT: PASS ceo-openwebui-e2e-workflow-test"
echo "Read: $REPORT"
echo "Outbox: $OUTBOX"
echo "Handoff: $HANDOFF"
