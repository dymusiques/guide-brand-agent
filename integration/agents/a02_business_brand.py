from __future__ import annotations

import json
import os
import subprocess

from integration.agents._paths import AGENTS_DIR, GOALS_JSON, ROOT, SHELLS

AGENT_ID = "02"
AGENT_LABEL = "Business Brand"
GOAL_IDS = ["G-CROSS-INDUSTRY", "G-BUSINESS-BRAND"]
SHELL = SHELLS / "02-business-brand.sh"
README = ROOT / "content/business-brand/README.md"


def case_1_prompt() -> tuple[bool, str]:
    p = AGENTS_DIR / "02-business-brand/INTEGRATION-PROMPT.md"
    return (True, "ok") if p.is_file() else (False, "missing INTEGRATION-PROMPT")


def case_2_role() -> tuple[bool, str]:
    p = AGENTS_DIR / "02-business-brand/ROLE.md"
    return (True, "ok") if p.is_file() else (False, "missing ROLE")


def case_3_skill() -> tuple[bool, str]:
    p = ROOT / ".cursor/skills/business-brand/SKILL.md"
    return (True, "ok") if p.is_file() else (False, "missing skill")


def case_4_readme_template() -> tuple[bool, str]:
    if not README.is_file():
        return False, "missing content/business-brand/README.md"
    t = README.read_text(encoding="utf-8")
    for needle in ("定位", "SWOT"):
        if needle not in t:
            return False, f"README missing {needle}"
    return True, "template sections"


def case_5_shell() -> tuple[bool, str]:
    if not SHELL.is_file() or not os.access(SHELL, os.X_OK):
        return False, "shell"
    proc = subprocess.run([str(SHELL), "--check"], capture_output=True, text=True, cwd=ROOT)
    if proc.returncode != 0:
        return False, proc.stderr[:120]
    for name in ("evaluate-business-brand.py", "verify-business-brand.sh", "lint-strategic-doc.py"):
        if not (ROOT / "scripts" / name).is_file():
            return False, f"missing scripts/{name}"
    kernel = ROOT / "kernels/strategic_docs/line2/is_strategic_doc_aligned.py"
    return (True, "shell+evaluate") if kernel.is_file() else (False, "missing strategic kernel")


def case_6_goals() -> tuple[bool, str]:
    data = json.loads(GOALS_JSON.read_text(encoding="utf-8"))
    found = any(g["id"] == "G-BUSINESS-BRAND" for g in data["owner_goals"])
    return (True, "G-BUSINESS-BRAND") if found else (False, "goal missing")


CASES = [
    ("02 · INTEGRATION-PROMPT", case_1_prompt),
    ("02 · ROLE", case_2_role),
    ("02 · Skill", case_3_skill),
    ("02 · 产出模板 README", case_4_readme_template),
    ("02 · 函数壳", case_5_shell),
    ("02 · Goal G-BUSINESS-BRAND", case_6_goals),
]
