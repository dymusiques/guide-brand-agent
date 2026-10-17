from __future__ import annotations

import json
import os
import subprocess
import sys

from integration.agents._paths import AGENTS_DIR, GOALS_JSON, ROOT, SHELLS

AGENT_ID = "04"
AGENT_LABEL = "XHS Topic Manager"
GOAL_IDS = ["G-STRONG-LINK", "G-BRIEF-ALIGNED-GATE", "G-CROSS-INDUSTRY"]
SHELL = SHELLS / "04-xhs-topic.sh"
EVAL = ROOT / "scripts/evaluate-xhs-topic.py"


def _py() -> str:
    venv = ROOT / ".venv/bin/python"
    return str(venv) if venv.is_file() else sys.executable


def case_1_prompt() -> tuple[bool, str]:
    p = AGENTS_DIR / "04-xhs-topic-manager/INTEGRATION-PROMPT.md"
    return (True, "ok") if p.is_file() else (False, "missing")


def case_2_evaluate_script() -> tuple[bool, str]:
    return (True, "evaluate") if EVAL.is_file() else (False, "missing evaluate-xhs-topic.py")


def case_3_bad_brief_exit_2() -> tuple[bool, str]:
    tmp = ROOT / ".tmp-agent04-brief.md"
    tmp.write_text("# no classifier\n", encoding="utf-8")
    try:
        proc = subprocess.run(
            [_py(), str(EVAL), "--brief", str(tmp)],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        return (True, "exit 2") if proc.returncode == 2 else (False, f"exit {proc.returncode}")
    finally:
        tmp.unlink(missing_ok=True)


def case_4_pipeline_doc() -> tuple[bool, str]:
    p = ROOT / "content/xiaohongshu/PIPELINE.md"
    return (True, "PIPELINE") if p.is_file() else (False, "missing PIPELINE.md")


def case_5_shell() -> tuple[bool, str]:
    if not SHELL.is_file() or not os.access(SHELL, os.X_OK):
        return False, "shell"
    proc = subprocess.run([str(SHELL), "--check"], capture_output=True, text=True, cwd=ROOT)
    return (True, "ok") if proc.returncode == 0 else (False, proc.stdout[:120])


def case_6_goals() -> tuple[bool, str]:
    data = json.loads(GOALS_JSON.read_text(encoding="utf-8"))
    for gid in GOAL_IDS:
        row = next((g for g in data["owner_goals"] if g["id"] == gid), None)
        if not row or "04-xhs-topic-manager" not in row.get("agents", []):
            return False, f"{gid} not linked to 04"
    return True, "goals linked"


CASES = [
    ("04 · INTEGRATION-PROMPT", case_1_prompt),
    ("04 · evaluate 函数壳", case_2_evaluate_script),
    ("04 · 缺 marker exit 2", case_3_bad_brief_exit_2),
    ("04 · PIPELINE 文档", case_4_pipeline_doc),
    ("04 · agent shell", case_5_shell),
    ("04 · Goal registry", case_6_goals),
]
