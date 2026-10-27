#!/usr/bin/env bash
# Refresh content/personal-ip/cv-source-*.md from Drive Doc (Agent or Owner).
# Requires: gdocs MCP authorized OR manual paste after read_file on fileId below.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TARGET="$ROOT/content/personal-ip/cv-source-2026-09-15.md"
DRIVE_DOC_ID="13vh69eCf_OaVY0DT9gj7AYifeq_wjmCt482cExcjf0k"
echo "CV Git truth: $TARGET"
echo "Drive Doc ID: $DRIVE_DOC_ID"
echo "Agent: use plugin-google-drive read_file on fileId, then update §可引用经历 bullet if facts changed."
if [[ -f "$TARGET" ]]; then
  echo "RESULT: PASS cv-source present (manual/MCP sync)"
  exit 0
fi
echo "RESULT: FAIL missing $TARGET"
exit 1
