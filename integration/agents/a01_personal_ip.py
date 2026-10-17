from __future__ import annotations

import json
import os
import subprocess
import sys

from integration.agents._paths import AGENTS_DIR, GOALS_JSON, ROOT, SHELLS

AGENT_ID = "01"
AGENT_LABEL = "Personal IP"
GOAL_IDS = ["G-NOT-HOME-DECOR", "G-CROSS-INDUSTRY", "G-STRONG-LINK"]
SHELL = SHELLS / "01-personal-ip.sh"
IP_BRIEF = ROOT / "content/personal-ip/ip-positioning-brief-2026-10-05.md"


def case_1_prompt() -> tuple[bool, str]:
    p = AGENTS_DIR / "01-personal-ip/INTEGRATION-PROMPT.md"
    return (True, "ok") if p.is_file() else (False, "missing prompt")


def case_2_ip_brief() -> tuple[bool, str]:
    if not IP_BRIEF.is_file():
        return False, "missing IP brief"
    t = IP_BRIEF.read_text(encoding="utf-8")
    if "品牌合作范围" not in t or "不单品类绑定" not in t:
        return False, "missing scope markers"
    return True, "IP brief scope"


def case_3_skill() -> tuple[bool, str]:
    p = ROOT / ".cursor/skills/personal-ip/SKILL.md"
    return (True, "skill") if p.is_file() else (False, "missing personal-ip skill")


def case_4_content_dir() -> tuple[bool, str]:
    d = ROOT / "content/personal-ip"
    if not d.is_dir():
        return False, "no content/personal-ip"
    mds = list(d.glob("*.md"))
    return (True, f"{len(mds)} md") if mds else (False, "no brief md")


def case_5_shell() -> tuple[bool, str]:
    if not SHELL.is_file() or not os.access(SHELL, os.X_OK):
        return False, "shell missing or not executable"
    proc = subprocess.run([str(SHELL), "--check"], capture_output=True, text=True, cwd=ROOT)
    if proc.returncode != 0:
        return False, (proc.stderr or proc.stdout or "shell failed")[:200]
    return True, "shell --check ok"


def case_6_goals() -> tuple[bool, str]:
    data = json.loads(GOALS_JSON.read_text(encoding="utf-8"))
    for g in data["owner_goals"]:
        if g["id"] in GOAL_IDS and "01-personal-ip" not in g.get("agents", []):
            return False, f"{g['id']} missing agent 01"
    return True, "registry links 01"


CASES = [
    ("01 · INTEGRATION-PROMPT", case_1_prompt),
    ("01 · IP Brief 边界", case_2_ip_brief),
    ("01 · Skill 路由", case_3_skill),
    ("01 · content/personal-ip", case_4_content_dir),
    ("01 · 函数壳", case_5_shell),
    ("01 · Goal Registry", case_6_goals),
]
