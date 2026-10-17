from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INTEGRATION = ROOT / "integration"
IMPORTANT = INTEGRATION / "IMPORTANT.md"
GOALS_JSON = INTEGRATION / "goals/registry.json"
AGENTS_DIR = ROOT / "agents"
SCRIPTS = ROOT / "scripts"
SHELLS = SCRIPTS / "agent-shells"
