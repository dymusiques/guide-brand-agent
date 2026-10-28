#!/usr/bin/env bash
# Detect stale locks / duplicate deep-delivery / broken logs → fix → optional retry.
# See docs/CEO-AUTO-RECOVER-AND-RETRY.md
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# shellcheck source=scripts/lib/ceo-deep-delivery-lock.sh
source "$ROOT/scripts/lib/ceo-deep-delivery-lock.sh"
INBOX="$ROOT/content/evolution/00-manager/ceo-inbox"
REPORT="$INBOX/ceo-auto-recover-latest.md"
mkdir -p "$INBOX"

DRY="${CEO_AUTO_RECOVER_DRY_RUN:-0}"
KILL_DUP="${CEO_AUTO_RECOVER_KILL_DUP_DEEP:-1}"
DEEP_ROUNDS="${CEO_DEEP_ROUNDS:-2}"
SKIP_PLATFORM="${VERIFY_GOALS_SKIP_PLATFORM:-1}"
CAMPAIGN_LOCK="/tmp/ceo-ip-all-agents-campaign.lock"

actions=()
note() { actions+=("$1"); echo ">>> $1"; }

latest_log() {
  local pat="$1"
  ls -t "$INBOX"/$pat 2>/dev/null | head -1 || true
}

log_closed_pass() {
  local f="$1"
  local marker="$2"
  [[ -n "$f" && -f "$f" ]] || return 1
  grep -q "$marker" "$f" 2>/dev/null || return 1
}

log_has_fatal_tail() {
  local f="$1"
  [[ -n "$f" && -f "$f" ]] || return 1
  tail -n 120 "$f" 2>/dev/null | grep -E 'syntax error|RESULT: FAIL ceo-deep-delivery' 2>/dev/null | tail -1 || return 1
}

# —— Detect / Fix: stale deep lock ——
if ceo_deep_lock_stale_remove; then
  note "removed stale ceo-deep-delivery lock"
fi

# —— Duplicate top-level deep processes (exclude child bash from same tree) ——
deep_roots=()
while IFS= read -r p; do
  [[ -n "$p" ]] || continue
  ppid="$(ps -o ppid= -p "$p" 2>/dev/null | tr -d ' ')"
  if ps -o command= -p "$ppid" 2>/dev/null | grep -q run-ceo-deep-delivery-cycle; then
    continue
  fi
  deep_roots+=("$p")
done < <(pgrep -f 'run-ceo-deep-delivery-cycle\.sh' 2>/dev/null | sort -u)

if [[ "${#deep_roots[@]}" -gt 1 && "$KILL_DUP" == "1" ]]; then
  keep="${deep_roots[0]}"
  note "multiple deep-delivery roots: ${deep_roots[*]} · keep $keep"
  idx=1
  while [[ "$idx" -lt "${#deep_roots[@]}" ]]; do
    pid="${deep_roots[$idx]}"
    if [[ "$DRY" == "1" ]]; then
      note "DRY_RUN would SIGTERM pid $pid"
    else
      kill -TERM "$pid" 2>/dev/null || true
      note "SIGTERM duplicate deep pid $pid"
    fi
    idx=$((idx + 1))
  done
fi

DEEP_LOG="$(latest_log 'ceo-deep-delivery-*.log')"
CAMP_LOG="$(latest_log 'ceo-ip-all-agents-campaign-*.log')"

need_deep_retry=0
if err="$(log_has_fatal_tail "$DEEP_LOG")"; then
  if log_closed_pass "$DEEP_LOG" 'RESULT: PASS ceo-deep-delivery'; then
    note "ignored stale error in deep log (final PASS present)"
  else
    note "deep log tail error: $err"
    need_deep_retry=1
  fi
elif ! log_closed_pass "$DEEP_LOG" 'RESULT: PASS ceo-deep-delivery'; then
  if [[ "${#deep_roots[@]}" -eq 0 ]]; then
    note "no PASS deep log and no running deep → schedule retry"
    need_deep_retry=1
  else
    note "deep in progress (pid ${deep_roots[*]:-?}) · skip restart"
  fi
fi

need_campaign_retry=0
if [[ -n "$CAMP_LOG" ]] && ! log_closed_pass "$CAMP_LOG" 'RESULT: PASS ceo-ip-all-agents-campaign'; then
  if grep -q 'Agent 02' "$CAMP_LOG" && ! grep -q 'Agent 03' "$CAMP_LOG"; then
    note "campaign stuck after Agent 02 in $(basename "$CAMP_LOG")"
    need_campaign_retry=1
  fi
fi

if [[ "$need_deep_retry" == "1" && "${#deep_roots[@]}" -gt 0 ]]; then
  if [[ "$DRY" == "1" ]]; then
    note "DRY_RUN would stop deep ${deep_roots[*]} before retry"
  else
    for pid in "${deep_roots[@]}"; do
      kill -TERM "$pid" 2>/dev/null || true
    done
    rm -f "$DEEP_LOCK"
    note "stopped failed deep pids for clean retry"
    deep_roots=()
  fi
fi

started_deep=0
started_campaign=0

if [[ "$need_deep_retry" == "1" && "${#deep_roots[@]}" -eq 0 ]]; then
  if [[ "$DRY" == "1" ]]; then
    note "DRY_RUN would nohup run-ceo-deep-delivery-cycle.sh"
  else
    nohup env VERIFY_GOALS_SKIP_PLATFORM="$SKIP_PLATFORM" CEO_DEEP_ROUNDS="$DEEP_ROUNDS" \
      bash "$ROOT/scripts/run-ceo-deep-delivery-cycle.sh" \
      >>"$INBOX/ceo-deep-delivery-live.log" 2>&1 &
    note "started deep-delivery nohup pid $! · CEO_DEEP_ROUNDS=$DEEP_ROUNDS"
    started_deep=1
  fi
fi

if [[ "$need_campaign_retry" == "1" ]]; then
  if ceo_deep_delivery_active && [[ "$started_deep" -eq 0 ]]; then
    note "campaign retry deferred (deep active · will SKIP_GEMINI)"
  fi
  if [[ "$DRY" == "1" ]]; then
    note "DRY_RUN would nohup run-ceo-ip-all-agents-campaign.sh"
  else
    nohup env VERIFY_GOALS_SKIP_PLATFORM="$SKIP_PLATFORM" \
      bash "$ROOT/scripts/run-ceo-ip-all-agents-campaign.sh" \
      >>"$INBOX/ceo-ip-all-agents-campaign-live.log" 2>&1 &
    note "started campaign nohup pid $! "
    started_campaign=1
  fi
fi

if [[ -f "$CAMPAIGN_LOCK" ]]; then
  cpid="$(tr -d '[:space:]' <"$CAMPAIGN_LOCK" 2>/dev/null || true)"
  if [[ -n "$cpid" ]] && ! kill -0 "$cpid" 2>/dev/null; then
    rm -f "$CAMPAIGN_LOCK"
    note "removed stale campaign lock (pid $cpid)"
  fi
fi

{
  echo "# CEO auto-recover · $(date -Iseconds)"
  echo ""
  echo "- dry_run: $DRY"
  echo "- deep_log: ${DEEP_LOG:-none}"
  echo "- campaign_log: ${CAMP_LOG:-none}"
  echo "- deep_roots: ${deep_roots[*]:-none}"
  echo "- started_deep: $started_deep"
  echo "- started_campaign: $started_campaign"
  echo ""
  echo "## Actions"
  for a in "${actions[@]}"; do
    echo "- $a"
  done
  if [[ "${#actions[@]}" -eq 0 ]]; then
    echo "- no action required"
  fi
} >"$REPORT"

echo "Report: $REPORT"
exit 0
