#!/usr/bin/env python3
"""Backward-compatible wrapper — Manager integration = Goals 6 + Agent 00 matrix.

Prefer: bash scripts/verify-agent-matrix.sh
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    py = sys.executable
    venv = ROOT / ".venv/bin/python"
    if venv.is_file():
        py = str(venv)
    for script in (
        "integration/tests/test_goals_registry.py",
        "integration/tests/test_agents_matrix.py",
    ):
        proc = subprocess.run([py, str(ROOT / script), *sys.argv[1:]], cwd=ROOT)
        if proc.returncode != 0:
            return proc.returncode
    print("\nRESULT: PASS — manager integration (goals + full agent matrix)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
