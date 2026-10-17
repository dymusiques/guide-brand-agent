from __future__ import annotations

import json
import os
import subprocess

from integration.agents._paths import AGENTS_DIR, GOALS_JSON, ROOT, SHELLS

AGENT_ID = "03"
AGENT_LABEL = "Marketing Strategy"
GOAL_IDS = ["G-MARKETING-CAMPAIGN", "G-STRONG-LINK"]
SHELL = SHELLS / "03-marketing.sh"
README = ROOT / "content/marketing/README.md"


def case_1_prompt() -> tuple[bool, str]:
    p = AGENTS_DIR / "03-marketing-strategy/INTEGRATION-PROMPT.md"
    return (True, "ok") if p.is_file() else (False, "missing prompt")


def case_2_skill() -> tuple[bool, str]:
    p = ROOT / ".cursor/skills/marketing-strategy/SKILL.md"
    return (True, "ok") if p.is_file() else (False, "missing skill")


def case_3_readme() -> tuple[bool, str]:
    if not README.is_file():
        return False, "missing README"
    t = README.read_text(encoding="utf-8")
    if "campaign" not in t.lower() and "Campaign" not in t:
        return False, "README missing campaign block"
    return True, "campaign template"


def case_4_content_dir() -> tuple[bool, str]:
    return (True, "dir ok") if (ROOT / "content/marketing").is_dir() else (False, "no dir")


def case_5_shell() -> tuple[bool, str]:
    if not SHELL.is_file() or not os.access(SHELL, os.X_OK):
        return False, "shell"
    proc = subprocess.run([str(SHELL), "--check"], capture_output=True, text=True, cwd=ROOT)
    if proc.returncode != 0:
        return False, proc.stderr[:120]
    for name in ("evaluate-marketing-campaign.py", "verify-marketing-campaign.sh"):
        if not (ROOT / "scripts" / name).is_file():
            return False, f"missing {name}"
    test = ROOT / "kernels/strategic_docs/line2/tests/test_marketing_aligned.py"
    return (True, "ok") if test.is_file() else (False, "missing gemini 6 tests")


def case_6_goals() -> tuple[bool, str]:
    data = json.loads(GOALS_JSON.read_text(encoding="utf-8"))
    return (
        (True, "ok")
        if any(g["id"] == "G-MARKETING-CAMPAIGN" for g in data["owner_goals"])
        else (False, "G-MARKETING-CAMPAIGN missing")
    )


CASES = [
    ("03 · INTEGRATION-PROMPT", case_1_prompt),
    ("03 · Skill", case_2_skill),
    ("03 · README campaign", case_3_readme),
    ("03 · content/marketing", case_4_content_dir),
    ("03 · 函数壳", case_5_shell),
    ("03 · Goal registry", case_6_goals),
]
