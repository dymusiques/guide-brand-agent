#!/usr/bin/env python3
"""Goal Registry — 6 integration cases."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REG_JSON = ROOT / "integration/goals/registry.json"
REG_MD = ROOT / "integration/GOALS-REGISTRY.md"

AGENT_SLUGS = [
    "00-manager",
    "01-personal-ip",
    "02-business-brand",
    "03-marketing-strategy",
    "04-xhs-topic-manager",
    "05-xhs-kernel",
    "06-xhs-content-pipeline",
    "07-brand-visual",
    "08-platform-integration",
    "09-data-analytics",
]


def case_1_json_valid() -> tuple[bool, str]:
    if not REG_JSON.is_file():
        return False, "missing registry.json"
    data = json.loads(REG_JSON.read_text(encoding="utf-8"))
    if "owner_goals" not in data:
        return False, "missing owner_goals"
    return True, f"{len(data['owner_goals'])} goals"


def case_2_version() -> tuple[bool, str]:
    data = json.loads(REG_JSON.read_text(encoding="utf-8"))
    v = data.get("version")
    return (True, f"v{v}") if v else (False, "no version")


def case_3_unique_ids() -> tuple[bool, str]:
    data = json.loads(REG_JSON.read_text(encoding="utf-8"))
    ids = [g["id"] for g in data["owner_goals"]]
    if len(ids) != len(set(ids)):
        return False, "duplicate goal ids"
    return True, "unique ids"


def case_4_all_agents_covered() -> tuple[bool, str]:
    data = json.loads(REG_JSON.read_text(encoding="utf-8"))
    covered: set[str] = set()
    for g in data["owner_goals"]:
        covered.update(g.get("agents", []))
    missing = [a for a in AGENT_SLUGS if a not in covered]
    if missing:
        return False, f"agents not in any goal: {missing}"
    return True, "all 10 agents linked"


def case_5_quality_growth_milestones() -> tuple[bool, str]:
    data = json.loads(REG_JSON.read_text(encoding="utf-8"))
    g = next((x for x in data["owner_goals"] if x["id"] == "G-QUALITY-GROWTH"), None)
    if not g:
        return False, "missing G-QUALITY-GROWTH"
    if g.get("kpi_automated") is not False:
        return False, "kpi must not be automated in classifier"
    ms = g.get("milestones")
    if ms != [1700, 5000, 10000]:
        return False, f"unexpected milestones {ms}"
    return True, "milestones documented"


def case_6_md_points_to_json() -> tuple[bool, str]:
    if not REG_MD.is_file():
        return False, "missing GOALS-REGISTRY.md"
    t = REG_MD.read_text(encoding="utf-8")
    if "registry.json" not in t or "G-QUALITY-GROWTH" not in t:
        return False, "md out of sync"
    return True, "GOALS-REGISTRY.md ok"


CASES = [
    ("Goals · registry.json 可读", case_1_json_valid),
    ("Goals · version 字段", case_2_version),
    ("Goals · goal id 唯一", case_3_unique_ids),
    ("Goals · 10 个 Agent 均有目标", case_4_all_agents_covered),
    ("Goals · 涨粉 KPI 文档化非 kernel 断言", case_5_quality_growth_milestones),
    ("Goals · GOALS-REGISTRY.md", case_6_md_points_to_json),
]


def main() -> int:
    passed = failed = 0
    print("=== Goal Registry verify (6 cases) ===\n")
    for desc, fn in CASES:
        try:
            ok, detail = fn()
        except Exception as exc:
            ok, detail = False, str(exc)
        if ok:
            print(f"  PASS · {desc} ({detail})")
            passed += 1
        else:
            print(f"  FAIL · {desc} — {detail}")
            failed += 1
    print(f"\n=== Summary ===\ncases: {passed} passed, {failed} failed")
    if failed:
        print("RESULT: FAIL — goals registry")
        return 1
    print("RESULT: PASS — goals registry 6 cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
