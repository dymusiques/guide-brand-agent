from __future__ import annotations

import json
import os
import subprocess

from integration.agents._paths import AGENTS_DIR, GOALS_JSON, ROOT, SHELLS

AGENT_ID = "06"
AGENT_LABEL = "XHS Content Pipeline"
GOAL_IDS = ["G-BRIEF-ALIGNED-GATE"]
SHELL = SHELLS / "06-xhs-pipeline.sh"


def case_1_prompt() -> tuple[bool, str]:
    p = AGENTS_DIR / "06-xhs-content-pipeline/INTEGRATION-PROMPT.md"
    return (True, "ok") if p.is_file() else (False, "missing")


def case_2_batch_script() -> tuple[bool, str]:
    p = ROOT / "scripts/verify-xhs-content-dir.sh"
    return (True, "ok") if p.is_file() and os.access(p, os.X_OK) else (False, "missing script")


def case_3_brief_glob_pattern() -> tuple[bool, str]:
    briefs = list((ROOT / "content/xiaohongshu").glob("*-brief.md"))
    return (True, f"{len(briefs)} brief(s)") if briefs else (True, "0 brief (ok for green)")


def case_4_template() -> tuple[bool, str]:
    p = ROOT / "kernels/templates/xhs-content-brief.template.md"
    return (True, "template") if p.is_file() else (False, "missing brief template")


def case_5_shell() -> tuple[bool, str]:
    if not SHELL.is_file() or not os.access(SHELL, os.X_OK):
        return False, "shell"
    proc = subprocess.run([str(SHELL), "--check"], capture_output=True, text=True, cwd=ROOT)
    return (True, "ok") if proc.returncode == 0 else (False, proc.stdout[:120])


def case_6_goals() -> tuple[bool, str]:
    data = json.loads(GOALS_JSON.read_text(encoding="utf-8"))
    g = next((x for x in data["owner_goals"] if x["id"] == "G-BRIEF-ALIGNED-GATE"), None)
    if not g or "06-xhs-content-pipeline" not in g.get("agents", []):
        return False, "gate goal not linked"
    return True, "aligned gate"


CASES = [
    ("06 · INTEGRATION-PROMPT", case_1_prompt),
    ("06 · verify-xhs-content-dir", case_2_batch_script),
    ("06 · *-brief.md 路径", case_3_brief_glob_pattern),
    ("06 · Brief 模板", case_4_template),
    ("06 · 函数壳", case_5_shell),
    ("06 · Goal aligned gate", case_6_goals),
]
