from __future__ import annotations

import json
import os
import subprocess

from integration.agents._paths import AGENTS_DIR, GOALS_JSON, ROOT, SHELLS

AGENT_ID = "07"
AGENT_LABEL = "Brand Visual"
GOAL_IDS = ["G-BRAND-VISUAL"]
SHELL = SHELLS / "07-brand-visual.sh"
README = ROOT / "content/visual/README.md"


def case_1_prompt() -> tuple[bool, str]:
    p = AGENTS_DIR / "07-brand-visual/INTEGRATION-PROMPT.md"
    return (True, "ok") if p.is_file() else (False, "missing")


def case_2_skill() -> tuple[bool, str]:
    p = ROOT / ".cursor/skills/brand-visual/SKILL.md"
    return (True, "ok") if p.is_file() else (False, "missing skill")


def case_3_readme() -> tuple[bool, str]:
    if not README.is_file():
        return False, "missing visual README"
    if "封面" not in README.read_text(encoding="utf-8"):
        return False, "README missing 封面 block"
    return True, "cover block"


def case_4_content_dir() -> tuple[bool, str]:
    return (True, "ok") if (ROOT / "content/visual").is_dir() else (False, "no dir")


def case_5_shell() -> tuple[bool, str]:
    if not SHELL.is_file() or not os.access(SHELL, os.X_OK):
        return False, "shell"
    proc = subprocess.run([str(SHELL), "--check"], capture_output=True, text=True, cwd=ROOT)
    return (True, "ok") if proc.returncode == 0 else (False, proc.stdout[:120])


def case_6_goals() -> tuple[bool, str]:
    data = json.loads(GOALS_JSON.read_text(encoding="utf-8"))
    return (
        (True, "ok")
        if any(g["id"] == "G-BRAND-VISUAL" for g in data["owner_goals"])
        else (False, "missing goal")
    )


CASES = [
    ("07 · INTEGRATION-PROMPT", case_1_prompt),
    ("07 · brand-visual skill", case_2_skill),
    ("07 · visual README", case_3_readme),
    ("07 · content/visual", case_4_content_dir),
    ("07 · 函数壳", case_5_shell),
    ("07 · Goal registry", case_6_goals),
]
