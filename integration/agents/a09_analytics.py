from __future__ import annotations

import json
import os
import subprocess

from integration.agents._paths import AGENTS_DIR, GOALS_JSON, ROOT, SHELLS

AGENT_ID = "09"
AGENT_LABEL = "Data Analytics"
GOAL_IDS = ["G-ANALYTICS-EVIDENCE", "G-QUALITY-GROWTH"]
SHELL = SHELLS / "09-analytics.sh"


def case_1_prompt_and_data_needs() -> tuple[bool, str]:
    for name in ("INTEGRATION-PROMPT.md", "DATA-NEEDS.md"):
        if not (AGENTS_DIR / "09-data-analytics" / name).is_file():
            return False, f"missing {name}"
    return True, "prompt + DATA-NEEDS"


def case_2_analytics_readme() -> tuple[bool, str]:
    p = ROOT / "content/analytics/README.md"
    return (True, "ok") if p.is_file() else (False, "missing analytics README")


def case_3_pipeline_script() -> tuple[bool, str]:
    p = ROOT / "scripts/analytics-pipeline.sh"
    return (True, "ok") if p.is_file() and os.access(p, os.X_OK) else (False, "missing pipeline")


def case_4_example_csv() -> tuple[bool, str]:
    ig = ROOT / "content/analytics/instagram/posts.example.csv"
    if not ig.is_file():
        return False, "missing IG example"
    if "听见Daily" not in ig.read_text(encoding="utf-8"):
        return False, "IG pillar should be 听见Daily not numeric"
    return True, "example CSV ok"


def case_5_shell() -> tuple[bool, str]:
    if not SHELL.is_file() or not os.access(SHELL, os.X_OK):
        return False, "shell"
    proc = subprocess.run([str(SHELL), "--check"], capture_output=True, text=True, cwd=ROOT)
    return (True, "ok") if proc.returncode == 0 else (False, proc.stdout[:200])


def case_6_goals() -> tuple[bool, str]:
    data = json.loads(GOALS_JSON.read_text(encoding="utf-8"))
    growth = next((g for g in data["owner_goals"] if g["id"] == "G-QUALITY-GROWTH"), None)
    if not growth or "milestones" not in growth:
        return False, "milestones missing"
    return True, f"milestones {growth['milestones']}"


CASES = [
    ("09 · Prompt + DATA-NEEDS", case_1_prompt_and_data_needs),
    ("09 · content/analytics README", case_2_analytics_readme),
    ("09 · analytics-pipeline.sh", case_3_pipeline_script),
    ("09 · example CSV", case_4_example_csv),
    ("09 · 函数壳", case_5_shell),
    ("09 · Goal milestones", case_6_goals),
]
