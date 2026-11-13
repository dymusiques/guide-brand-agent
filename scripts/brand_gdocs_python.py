#!/usr/bin/env python3
"""Resolve Python that can import googleapiclient + gdocs CLI (vendor/gdocs-skill venv)."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CANDIDATES = (
    ROOT / "vendor/gdocs-skill/.venv/bin/python3",
    ROOT / "vendor/gdocs-skill/.venv/bin/python",
    ROOT / ".venv/bin/python3",
    Path(shutil.which("python3") or sys.executable),
)


def resolve_gdocs_python() -> Path:
    import os

    for p in CANDIDATES:
        if p.is_file() and os.access(p, os.X_OK):
            return p
    return Path(sys.executable)
