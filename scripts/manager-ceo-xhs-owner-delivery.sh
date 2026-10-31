#!/usr/bin/env bash
# CEO XHS Owner delivery: evolution (optional briefs) + HTML rebuild + verify (+ optional round2).
# See docs/CEO-XHS-OWNER-DELIVERY-AUTOPILOT.md
# Rule: if ANY Discovery brief changed (or --brief is Discovery) → evolve ALL Discovery 01–04.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
bash scripts/ensure-venv-deps.sh

BRIEFS=()
# unset | 0 = off · 1 = always add Discovery queue · auto (default) = detect mtime / --brief
DISCOVERY_MODE="${CEO_DELIVERY_INCLUDE_DISCOVERY:-auto}"
NO_DISCOVERY_AUTO=0
ROUND2="${CEO_WORKFLOW_TEST_ROUND2:-0}"

discovery_queue() {
  local b
  for b in content/xiaohongshu/2026-10-17-discovery-0{1,2,3,4}-*-brief.md; do
    [[ -f "$b" ]] && echo "$b"
  done
}

filter_html_path() {
  local day
  day="$(date +%Y-%m-%d)"
  echo "content/evolution/00-manager/ceo-inbox/OWNER-XHS-FILTER-DELIVERABLE-${day}.html"
}

discovery_stale_vs_html() {
  local html="$1"
  [[ -f "$html" ]] || return 0
  local html_mtime b
  html_mtime="$(stat -f %m "$html" 2>/dev/null || stat -c %Y "$html")"
  while IFS= read -r b; do
    [[ -z "$b" ]] && continue
    b_mtime="$(stat -f %m "$b" 2>/dev/null || stat -c %Y "$b")"
    if [[ "$b_mtime" -gt "$html_mtime" ]]; then
      return 0
    fi
  done < <(discovery_queue)
  return 1
}

brief_list_contains_discovery() {
  [[ ${#BRIEFS[@]} -eq 0 ]] && return 1
  local b
  for b in "${BRIEFS[@]}"; do
    [[ "$b" == *"discovery-"* ]] && return 0
  done
  return 1
}

expand_discovery_queue() {
  local -a kept=()
  local b d
  for b in "${BRIEFS[@]}"; do
    [[ "$b" != *"discovery-"* ]] && kept+=("$b")
  done
  while IFS= read -r d; do
    [[ -z "$d" ]] && continue
    kept+=("$d")
  done < <(discovery_queue)
  BRIEFS=()
  local x y dup
  for x in "${kept[@]}"; do
    dup=0
    if [[ ${#BRIEFS[@]} -gt 0 ]]; then
      for y in "${BRIEFS[@]}"; do
        [[ "$x" == "$y" ]] && dup=1 && break
      done
    fi
    [[ "$dup" -eq 0 ]] && BRIEFS+=("$x")
  done
}

should_expand_discovery() {
  [[ "$NO_DISCOVERY_AUTO" -eq 1 ]] && return 1
  [[ "$DISCOVERY_MODE" == "1" ]] && return 0
  [[ "$DISCOVERY_MODE" == "0" ]] && return 1
  brief_list_contains_discovery && return 0
  discovery_stale_vs_html "$(filter_html_path)" && return 0
  return 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --brief) BRIEFS+=("${2:-}"); shift 2 ;;
    --include-discovery) DISCOVERY_MODE=1; shift ;;
    --no-discovery-auto) NO_DISCOVERY_AUTO=1; shift ;;
    --round2) ROUND2=1; shift ;;
    -h|--help)
      cat <<'EOF'
Usage: bash scripts/manager-ceo-xhs-owner-delivery.sh [options]

Options:
  --brief <path>       One or more briefs (if any is Discovery → all Discovery 01–04 evolve)
  --include-discovery  Always add Discovery 01–04 (CEO_DELIVERY_INCLUDE_DISCOVERY=1)
  --no-discovery-auto  Disable auto expand when Discovery mtime > HTML
  --round2             After delivery, run workflow test round2 campaign

Env:
  CEO_DELIVERY_INCLUDE_DISCOVERY=auto|0|1  (default: auto)
EOF
      exit 0
      ;;
    *) echo "Unknown: $1" >&2; exit 2 ;;
  esac
done

if [[ ${#BRIEFS[@]} -eq 0 ]]; then
  TEST="$(ls -t content/xiaohongshu/*-test-brief.md 2>/dev/null | head -1 || true)"
  [[ -n "$TEST" ]] && BRIEFS+=("$TEST")
  if [[ "$DISCOVERY_MODE" == "1" ]]; then
    while IFS= read -r b; do [[ -n "$b" ]] && BRIEFS+=("$b"); done < <(discovery_queue)
  fi
fi

if should_expand_discovery; then
  echo ">>> Auto: Discovery queue (any Discovery change → evolve 01–04)"
  expand_discovery_queue
fi

echo "=== manager-ceo-xhs-owner-delivery · briefs=${#BRIEFS[@]} round2=$ROUND2 discovery_mode=$DISCOVERY_MODE ==="
FAIL=0
for b in "${BRIEFS[@]}"; do
  [[ -f "$b" ]] || { echo "FAIL: missing $b"; exit 1; }
  echo "--- evolution: $b ---"
  if ! bash scripts/manager-brief-evolution-until-gap.sh --brief "$b"; then
    EC=$?
    if [[ "$EC" -eq 42 ]]; then
      echo "NEEDS_WORK: $b — read EVOLUTION-GAP + CEO-REROUTE"
      exit 42
    fi
    FAIL=$((FAIL + 1))
  fi
done

echo "--- HTML rebuild + verify ---"
bash scripts/refresh-owner-notify-html.sh || FAIL=$((FAIL + 1))

if [[ "$ROUND2" == "1" ]] && ls content/xiaohongshu/*-test-brief.md >/dev/null 2>&1; then
  echo "--- workflow test round2 campaign ---"
  bash scripts/ceo-workflow-test-round2-finish.sh || FAIL=$((FAIL + 1))
fi

if [[ "$FAIL" -eq 0 ]]; then
  echo "RESULT: PASS manager-ceo-xhs-owner-delivery"
  exit 0
fi
echo "RESULT: FAIL manager-ceo-xhs-owner-delivery ($FAIL)"
exit 1
