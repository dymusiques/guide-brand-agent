#!/usr/bin/env bash
# Ensure .venv has gdocs + Gemini deps for integration verify.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ ! -x .venv/bin/python ]]; then
  python3 -m venv .venv
fi
need=0
.venv/bin/python -c "import gdocs" 2>/dev/null || need=1
.venv/bin/python -c "from google import genai" 2>/dev/null || need=1
if [[ "$need" == "1" ]]; then
  echo "Installing venv deps (gdocs-skill + requirements-gemini.txt)..."
  .venv/bin/pip install -e vendor/gdocs-skill -r requirements-gemini.txt -q
fi
