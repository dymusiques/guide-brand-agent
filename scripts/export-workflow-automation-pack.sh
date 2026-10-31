#!/usr/bin/env bash
# Export workflow manifest + L1 index → RAG mirror for Open WebUI (# workflow-automation-pack).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/scripts/build-workflow-automation-catalog.py"
echo "EXPORT_OK workflow-automation-pack"
