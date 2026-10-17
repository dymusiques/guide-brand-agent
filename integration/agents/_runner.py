from __future__ import annotations

import importlib
import sys
from typing import Callable

AGENT_MODULES = [
    "integration.agents.a00_manager",
    "integration.agents.a01_personal_ip",
    "integration.agents.a02_business_brand",
    "integration.agents.a03_marketing",
    "integration.agents.a04_xhs_topic",
    "integration.agents.a05_xhs_kernel",
    "integration.agents.a06_xhs_pipeline",
    "integration.agents.a07_brand_visual",
    "integration.agents.a08_platform",
    "integration.agents.a09_analytics",
]


def run_agent_module(mod_name: str) -> tuple[int, int, str]:
    mod = importlib.import_module(mod_name)
    agent_id = getattr(mod, "AGENT_ID", "?")
    cases: list[tuple[str, Callable[[], tuple[bool, str]]]] = mod.CASES
    passed = failed = 0
    print(f"\n--- Agent {agent_id} · {getattr(mod, 'AGENT_LABEL', mod_name)} ({len(cases)} cases) ---")
    for desc, fn in cases:
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
    return passed, failed, agent_id


def run_all_agents() -> int:
    total_p = total_f = 0
    for mod_name in AGENT_MODULES:
        p, f, _ = run_agent_module(mod_name)
        total_p += p
        total_f += f
    print(f"\n=== Agent matrix summary ===")
    print(f"cases: {total_p} passed, {total_f} failed")
    if total_f:
        print("RESULT: FAIL — agent matrix")
        return 1
    print("RESULT: PASS — all agents 6-case matrix")
    return 0


if __name__ == "__main__":
    from integration.agents._paths import ROOT

    sys.path.insert(0, str(ROOT))
    raise SystemExit(run_all_agents())
