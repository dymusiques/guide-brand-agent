#!/usr/bin/env bash
# IP 内容工具链 · 环境验收（防 Agent 误读「装好了」却命令找不到 / CDP 误报）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

FAIL=0
WARN=0
pass() { echo "  OK   $1"; }
fail() { echo "  FAIL $1"; FAIL=$((FAIL + 1)); }
warn() { echo "  WARN $1"; WARN=$((WARN + 1)); }

echo "=== IP skills env verify: $ROOT ==="
echo ""

VENV_BIN="$ROOT/.venv/bin"
if [[ ! -x "$VENV_BIN/python" ]]; then
  fail ".venv missing — SETUP.md §2 (python3 -m venv .venv && pip install …)"
  echo "RESULT: FAIL ($FAIL)"
  exit 1
fi
pass ".venv present"

# Prefer venv on PATH for this script
export PATH="$VENV_BIN:$PATH"

echo ""
echo "[CLI entry points — must exist in .venv/bin]"
for exe in semantic-search voice-lora bili-upload voice-memos intake-skill vlog typefully-twitter dataforseo-skill; do
  if [[ -x "$VENV_BIN/$exe" ]]; then
    pass "$exe"
  else
    fail "$exe not in .venv/bin (pip install -e vendor/… per SETUP.md)"
  fi
done

# pw-test: no --help flag upstream; empty argv prints USAGE to stderr
if [[ -x "$VENV_BIN/pw-test" ]]; then
  if { "$VENV_BIN/pw-test" 2>&1 || true; } | grep -q "Usage: pw-test"; then
    pass "pw-test (usage: no args — not pw-test --help)"
  else
    warn "pw-test installed but usage text unexpected"
  fi
else
  fail "pw-test not in .venv/bin"
fi

echo ""
echo "[Playwright browser]"
if [[ -d "$HOME/Library/Caches/ms-playwright" ]] || [[ -d "$HOME/.cache/ms-playwright" ]]; then
  pass "playwright browser cache dir present (run: playwright install chromium if bilibili fill fails)"
else
  warn "playwright cache not found — after SETUP: playwright install chromium"
fi

echo ""
echo "[Optional · not required for XHS Brief]"
if python -c "import mlx_qwen3_asr" 2>/dev/null; then
  pass "mlx-qwen3-asr (intake/asr transcribe weights)"
else
  warn "mlx-qwen3-asr not installed — intake/asr transcribe: pip install -e 'vendor/intake-skill[qwen-asr]' (+ asr vendor README)"
fi
if [[ -f "$VENV_BIN/opusvid" ]] || python -c "import opusvid" 2>/dev/null; then
  pass "opus-video-audio python deps"
else
  pass "opus-video-audio-skill: script repo only (no pip) — read vendor skill when triggered"
fi

echo ""
echo "[Dev pytest-asyncio — online-media may pin older]"
PA_VER="$("$VENV_BIN/python" -c "import pytest_asyncio; print(pytest_asyncio.__version__)" 2>/dev/null || echo none)"
if [[ "$PA_VER" == none ]]; then
  warn "pytest-asyncio not installed (OK unless running vendor pytest suites)"
else
  warn "pytest-asyncio $PA_VER (often from online-media-skill) — OK for manager verify; ignore unless running vendor pytest"
fi

echo ""
echo "[Agent discipline reminder]"
echo "  · XHS Brief default: NO IP skill CLI unless integration/ip-content-skills-adoption.md §1 triggers"
echo "  · Shell: source scripts/ensure-workspace-venv.sh before bare voice-lora / bili-upload"
echo "  · pw-test / bilibili: Chrome CDP first — see skill_bilibili_upload.md"

echo ""
echo "=== Summary ==="
if [[ "$FAIL" -gt 0 ]]; then
  echo "RESULT: FAIL ($FAIL fail, $WARN warn)"
  exit 1
fi
if [[ "$WARN" -gt 0 ]]; then
  echo "RESULT: PASS with warnings ($WARN)"
  exit 0
fi
echo "RESULT: PASS"
exit 0
