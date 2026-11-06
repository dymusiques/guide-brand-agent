#!/usr/bin/env bash
# V-Tier 40–50万粉文笔标准 · 文件与 JSON 完整性（不替代 Owner 文笔 review）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FAIL=0
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAIL=$((FAIL + 1)); }

for f in \
  docs/OWNER-COPY-V-TIER-400K-MANDATE.md \
  docs/OWNER-COPY-V-TIER-MEASUREMENT-HONESTY.md \
  docs/OWNER-DUAL-TRACK-COPY-WORKFLOW.md \
  scripts/verify-owner-copy-v-tier-attestation.py \
  integration/handoff/owner-copy-v-tier-400k.json \
  integration/handoff/owner-copy-benchmarks-tier2.json \
  integration/handoff/owner-ip-benchmark-creators.json \
  integration/handoff/owner-copy-v-tier-live-corpus.json \
  docs/OWNER-COPY-V-TIER-LIVE-CORPUS-SOP.md \
  scripts/refresh-owner-copy-v-tier-live-corpus.py \
  docs/OWNER-COPY-V-TIER-CULTURAL-ART-STANDARD.md \
  integration/handoff/owner-copy-v-tier-cultural-art-creators.json; do
  [[ -f "$ROOT/$f" ]] && pass "$f" || fail "missing $f"
done

if command -v python3 >/dev/null 2>&1; then
  python3 - <<'PY' || fail "owner-copy-v-tier-400k.json schema"
import json
from pathlib import Path
p = Path("integration/handoff/owner-copy-v-tier-400k.json")
d = json.loads(p.read_text(encoding="utf-8"))
for k in ("standard_id", "mandate_doc", "workflow_doc", "applies_to_tracks", "style_checklist", "tracks"):
    assert k in d, k
assert d.get("owner_review_required") is True
assert "flutebuddy_product" in d["tracks"]
assert "personal_ip_ecosystem" in d["tracks"]
print("PASS: v-tier JSON keys")
PY
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "RESULT: PASS verify-owner-copy-v-tier-mandate"
  echo "HINT: Agent Must read mandate + deep-scrape; Owner Must review final copy."
  exit 0
fi
echo "RESULT: FAIL verify-owner-copy-v-tier-mandate ($FAIL)"
exit 1
