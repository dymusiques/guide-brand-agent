# shellcheck shell=bash
# Shared /tmp/ceo-deep-delivery.lock helpers for deep-delivery + IP campaign.
# Source from repo root scripts; sets DEEP_LOCK if unset.
: "${DEEP_LOCK:=/tmp/ceo-deep-delivery.lock}"

_ceo_deep_lock_pid() {
  if [[ ! -f "$DEEP_LOCK" ]]; then
    return 1
  fi
  local pid
  pid="$(tr -d '[:space:]' <"$DEEP_LOCK" 2>/dev/null || true)"
  [[ -n "$pid" ]] || return 1
  printf '%s' "$pid"
}

ceo_deep_lock_stale_remove() {
  local pid
  pid="$(_ceo_deep_lock_pid)" || return 1
  if kill -0 "$pid" 2>/dev/null; then
    return 1
  fi
  echo ">>> stale ceo-deep-delivery lock removed (pid $pid not running)"
  rm -f "$DEEP_LOCK"
  return 0
}

ceo_deep_delivery_active() {
  if ceo_deep_lock_stale_remove; then
    :
  fi
  if [[ -f "$DEEP_LOCK" ]]; then
    local pid
    pid="$(_ceo_deep_lock_pid)" || true
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
      return 0
    fi
    rm -f "$DEEP_LOCK"
  fi
  pgrep -f 'run-ceo-deep-delivery-cycle\.sh' >/dev/null 2>&1
}

ceo_acquire_deep_lock_or_exit() {
  if ceo_deep_lock_stale_remove; then
    :
  fi
  if [[ -f "$DEEP_LOCK" ]]; then
    local old_pid
    old_pid="$(_ceo_deep_lock_pid)" || true
    if [[ -n "$old_pid" ]] && kill -0 "$old_pid" 2>/dev/null; then
      echo "Another ceo-deep-delivery is running (pid $old_pid · $DEEP_LOCK)"
      exit 2
    fi
    rm -f "$DEEP_LOCK"
  fi
  echo $$ >"$DEEP_LOCK"
  trap 'rm -f "$DEEP_LOCK"' EXIT
}

ceo_campaign_wait_for_deep() {
  local max="${CEO_CAMPAIGN_WAIT_DEEP_SEC:-0}"
  [[ "$max" -gt 0 ]] || return 0
  local waited=0
  while ceo_deep_delivery_active && [[ "$waited" -lt "$max" ]]; do
    if [[ "$waited" -eq 0 ]]; then
      echo ">>> deep-delivery active — waiting up to ${max}s (CEO_CAMPAIGN_WAIT_DEEP_SEC) before campaign Gemini phases"
    fi
    sleep 5
    waited=$((waited + 5))
  done
  if ceo_deep_delivery_active; then
    echo ">>> deep-delivery still active after ${max}s — campaign continues with SKIP_GEMINI=1 for shell Gemini"
  fi
}
