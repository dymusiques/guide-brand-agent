#!/usr/bin/env bash
# Route goal → optional Open WebUI → outbox + job JSON. Used by Manager step -1.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

GOAL=""
BRIEF=""
INTAKE=""
PLATFORM="auto"
SLUG=""
DRY_RUN=0

usage() {
  echo "Usage: bash scripts/run-openwebui-router-pipeline.sh --goal \"...\" [--intake path.md] [--brief path] [--platform auto|personal_ip|website] [--slug name] [--dry-run]"
  exit 2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --goal|-g) GOAL="$2"; shift 2 ;;
    --brief) BRIEF="$2"; shift 2 ;;
    --intake) INTAKE="$2"; shift 2 ;;
    --platform) PLATFORM="$2"; shift 2 ;;
    --slug) SLUG="$2"; shift 2 ;;
    --dry-run) DRY_RUN=1; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown: $1"; usage ;;
  esac
done

[[ -n "$GOAL" ]] || usage

ROUTE_JSON="$(python3 scripts/route-openwebui-for-goal.py --goal "$GOAL" ${BRIEF:+--brief "$BRIEF"} --platform "$PLATFORM" ${SLUG:+--slug "$SLUG"} --json)"
echo "$ROUTE_JSON" | python3 -m json.tool

ROUTE="$(echo "$ROUTE_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['route'])")"
SLUG_FINAL="$(echo "$ROUTE_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['slug'])")"
PLATFORM_FINAL="$(echo "$ROUTE_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['platform'])")"

if [[ "$ROUTE" == "SKIP" ]]; then
  echo "RESULT: SKIP openwebui-router (CEO/Cursor only)"
  exit 0
fi

ARGS=(--route "$ROUTE" --goal "$GOAL" --slug "$SLUG_FINAL" --platform "$PLATFORM_FINAL")
[[ -n "$BRIEF" ]] && ARGS+=(--brief "$BRIEF")
[[ -n "$INTAKE" ]] && ARGS+=(--intake "$INTAKE")
[[ "$DRY_RUN" == 1 ]] && ARGS+=(--dry-run)

if [[ "$DRY_RUN" != 1 ]]; then
  python3 scripts/sync-openwebui-pipe-valves.py
fi

python3 scripts/openwebui-pipe-to-outbox.py "${ARGS[@]}"
echo "RESULT: PASS openwebui-router-pipeline route=$ROUTE slug=$SLUG_FINAL"
