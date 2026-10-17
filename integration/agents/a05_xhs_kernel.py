from __future__ import annotations

import json
import os
import subprocess
import sys

from integration.agents._paths import AGENTS_DIR, GOALS_JSON, ROOT, SHELLS

AGENT_ID = "05"
AGENT_LABEL = "XHS Kernel"
GOAL_IDS = ["G-STRONG-LINK", "G-NOT-SINGLE-VERTICAL-LOCK"]
SHELL = SHELLS / "05-xhs-kernel.sh"
KERNEL = ROOT / "kernels/xiaohongshu/line2/is_xhs_growth_aligned.py"
KERNEL_TEST = ROOT / "kernels/xiaohongshu/line2/tests/test_is_xhs_growth_aligned.py"


def case_1_kernel_module() -> tuple[bool, str]:
    return (True, "kernel file") if KERNEL.is_file() else (False, "missing kernel")


def case_2_empty_false() -> tuple[bool, str]:
    sys.path.insert(0, str(KERNEL.parent))
    from is_xhs_growth_aligned import is_xhs_growth_aligned

    if is_xhs_growth_aligned({"subject": "", "body": ""}) is not False:
        return False, "empty should be False"
    return True, "empty input False"


def case_3_gemini_test_module() -> tuple[bool, str]:
    return (True, "6-test module") if KERNEL_TEST.is_file() else (False, "missing test module")


def case_4_verify_script() -> tuple[bool, str]:
    p = ROOT / "scripts/verify-xhs-topic.sh"
    return (True, "verify-xhs-topic.sh") if p.is_file() and os.access(p, os.X_OK) else (False, "script")


def case_5_prompt() -> tuple[bool, str]:
    p = AGENTS_DIR / "05-xhs-kernel/INTEGRATION-PROMPT.md"
    return (True, "ok") if p.is_file() else (False, "missing prompt")


def case_6_goals_kpi_not_automated() -> tuple[bool, str]:
    data = json.loads(GOALS_JSON.read_text(encoding="utf-8"))
    growth = next((g for g in data["owner_goals"] if g["id"] == "G-QUALITY-GROWTH"), None)
    if not growth or growth.get("kpi_automated") is not False:
        return False, "G-QUALITY-GROWTH must not be kpi_automated in kernel"
    return True, "KPI not in kernel asserts"


CASES = [
    ("05 · kernel 模块", case_1_kernel_module),
    ("05 · 空输入 False", case_2_empty_false),
    ("05 · Gemini 6-test 路径", case_3_gemini_test_module),
    ("05 · verify-xhs-topic 壳", case_4_verify_script),
    ("05 · INTEGRATION-PROMPT", case_5_prompt),
    ("05 · 粉丝 KPI 不进 kernel", case_6_goals_kpi_not_automated),
]
