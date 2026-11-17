"""Brand repo Python + Gemini key — use for any script that may call google-genai."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
VENV_PY = ROOT / ".venv/bin/python3"


def brand_python() -> str:
    if VENV_PY.is_file():
        return str(VENV_PY)
    return sys.executable


def gemini_key_available() -> bool:
    if os.environ.get("GEMINI_API_KEY", "").strip():
        return True
    env_path = ROOT / ".env"
    if not env_path.is_file():
        return False
    try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            if s.startswith("GEMINI_API_KEY="):
                val = s.split("=", 1)[1].strip().strip("'\"")
                return len(val) > 8
    except OSError:
        return False
    return False