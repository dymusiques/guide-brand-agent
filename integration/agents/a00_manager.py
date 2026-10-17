from __future__ import annotations

import json
import os
import sys

from integration.agents._paths import AGENTS_DIR, GOALS_JSON, IMPORTANT, ROOT, SHELLS

AGENT_ID = "00"
AGENT_LABEL = "Manager"
GOAL_IDS = ["G-STRONG-LINK", "G-BRIEF-ALIGNED-GATE", "G-ANALYTICS-EVIDENCE"]
SHELL = SHELLS / "00-manager.sh"


def _py() -> str:
    venv = ROOT / ".venv/bin/python"
    return str(venv) if venv.is_file() else sys.executable


def case_1_auto_workflow() -> tuple[bool, str]:
    p = AGENTS_DIR / "00-manager/AUTO-WORKFLOW.md"
    if not p.is_file():
        return False, "missing AUTO-WORKFLOW.md"
    t = p.read_text(encoding="utf-8")
    if "Manager's Loop" not in t or "manager-workflow-verify" not in t:
        return False, "AUTO-WORKFLOW missing loop or verify"
    return True, "AUTO-WORKFLOW ok"


def case_2_integration_prompt() -> tuple[bool, str]:
    p = AGENTS_DIR / "00-manager/INTEGRATION-PROMPT.md"
    return (True, "present") if p.is_file() else (False, "missing INTEGRATION-PROMPT")


def case_3_important_readable() -> tuple[bool, str]:
    if not IMPORTANT.is_file():
        return False, "missing IMPORTANT.md"
    text = IMPORTANT.read_text(encoding="utf-8")
    for needle in ("跨行业", "强链接", "verify-xhs-topic"):
        if needle not in text:
            return False, f"missing {needle!r}"
    return True, "IMPORTANT markers"


def case_4_shell_executable() -> tuple[bool, str]:
    if not SHELL.is_file():
        return False, "missing agent shell"
    if not os.access(SHELL, os.X_OK):
        return False, "shell not executable"
    return True, str(SHELL.relative_to(ROOT))


def case_5_goals_linked() -> tuple[bool, str]:
    data = json.loads(GOALS_JSON.read_text(encoding="utf-8"))
    ids = {g["id"] for g in data["owner_goals"]}
    for gid in GOAL_IDS:
        if gid not in ids:
            return False, f"goal {gid} missing in registry"
    return True, "goal ids in registry"


def case_6_ceo_dashboard_runs() -> tuple[bool, str]:
    import subprocess

    p = ROOT / "scripts/manager-dashboard.sh"
    if not p.is_file():
        return False, "missing manager-dashboard.sh"
    proc = subprocess.run(
        ["bash", str(p)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "")[-300:]
        return False, f"dashboard exit {proc.returncode}: {tail}"
    derived = ROOT / "content/analytics/derived"
    today = __import__("datetime").date.today().isoformat()
    md = derived / f"manager-dashboard-{today}.md"
    if not md.is_file():
        return False, "dashboard md not written"
    return True, "manager-dashboard.sh exit 0"


CASES = [
    ("00 · AUTO-WORKFLOW 指挥链", case_1_auto_workflow),
    ("00 · INTEGRATION-PROMPT", case_2_integration_prompt),
    ("00 · IMPORTANT 可读", case_3_important_readable),
    ("00 · 函数壳 00-manager.sh", case_4_shell_executable),
    ("00 · 成功目标注册", case_5_goals_linked),
    ("00 · CEO 仪表盘可跑", case_6_ceo_dashboard_runs),
]
