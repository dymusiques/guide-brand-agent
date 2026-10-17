from __future__ import annotations

import json
import os
import subprocess

from integration.agents._paths import AGENTS_DIR, GOALS_JSON, ROOT, SHELLS

AGENT_ID = "08"
AGENT_LABEL = "Platform Integration"
GOAL_IDS = ["G-PLATFORM-SYNC"]
SHELL = SHELLS / "08-platform.sh"


def case_1_prompt() -> tuple[bool, str]:
    p = AGENTS_DIR / "08-platform-integration/INTEGRATION-PROMPT.md"
    return (True, "ok") if p.is_file() else (False, "missing")


def case_2_verify_integration_py() -> tuple[bool, str]:
    p = ROOT / "scripts/verify_integration.py"
    return (True, "ok") if p.is_file() else (False, "missing verify_integration.py")


def case_3_gdocs_submodule() -> tuple[bool, str]:
    p = ROOT / "vendor/gdocs-skill/pyproject.toml"
    return (True, "gdocs vendor") if p.is_file() else (False, "submodule")


def case_4_shell_wrapper() -> tuple[bool, str]:
    p = ROOT / "scripts/verify-integration.sh"
    if not p.is_file() or not os.access(p, os.X_OK):
        return False, "verify-integration.sh"
    return True, "platform verify shell"


def case_5_agent_shell() -> tuple[bool, str]:
    if not SHELL.is_file() or not os.access(SHELL, os.X_OK):
        return False, "08 shell"
    proc = subprocess.run([str(SHELL), "--check"], capture_output=True, text=True, cwd=ROOT)
    return (True, "ok") if proc.returncode == 0 else (False, proc.stdout[:120])


def case_6_goals() -> tuple[bool, str]:
    data = json.loads(GOALS_JSON.read_text(encoding="utf-8"))
    g = next((x for x in data["owner_goals"] if x["id"] == "G-PLATFORM-SYNC"), None)
    if not g or g.get("kpi_automated") is not True:
        return False, "G-PLATFORM-SYNC config"
    return True, "platform goal automated verify"


CASES = [
    ("08 · INTEGRATION-PROMPT", case_1_prompt),
    ("08 · verify_integration.py", case_2_verify_integration_py),
    ("08 · gdocs-skill vendor", case_3_gdocs_submodule),
    ("08 · verify-integration.sh", case_4_shell_wrapper),
    ("08 · agent shell", case_5_agent_shell),
    ("08 · Goal G-PLATFORM-SYNC", case_6_goals),
]
