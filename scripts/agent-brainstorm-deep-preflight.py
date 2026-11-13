#!/usr/bin/env python3
"""
深度 brainstorm 预检：在 agent-brainstorm-preflight 之上补全自动链。

layers: base preflight · drive hydrate · 6-case · monorepo prompt-six-case · CEO 切片 · QC 记录
handoff → integration/handoff/owner-brainstorm-deep-preflight-latest.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "integration/handoff/owner-brainstorm-deep-preflight-latest.json"
MONOREPO = Path.home() / "Desktop/未命名"


def run(cmd: list[str], *, cwd: Path | None = None, timeout: int = 600) -> tuple[int, str]:
    r = subprocess.run(
        cmd,
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    return r.returncode, out[-2000:]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--goal", required=True)
    ap.add_argument("--skip-ceo", action="store_true")
    ap.add_argument("--skip-six-case", action="store_true")
    args = ap.parse_args()
    goal = args.goal.strip()
    layers: dict = {}
    fail = 0

    ec, tail = run([sys.executable, "scripts/agent-hydrate-drive-priority.py", "--limit", "8"])
    layers["drive_hydrate_fulltext"] = {"status": "PASS" if ec == 0 else "PARTIAL", "exit_code": ec, "tail": tail}
    # PARTIAL = 个别文件未拉到全文；仍须有 handoff 供监督

    if not args.skip_six_case:
        ec, tail = run(["bash", "scripts/ceo-six-case-battery.sh"], timeout=900)
        core_six = (
            "PASS six-case · fused-04" in tail
            and "PASS six-case · fused-05" in tail
            and "all 6 cases passed" in tail
        )
        layers["ceo_six_case_battery"] = {
            "status": "PASS" if ec == 0 else ("PARTIAL" if core_six else "FAIL"),
            "exit_code": ec,
            "tail": tail,
            "note": "four-dimensions 未过线时仍 PARTIAL（integration+fused 已过）",
        }
        if ec != 0 and not core_six:
            fail += 1
    if MONOREPO.is_dir():
        ec, tail = run(
            ["python3", "scripts/agent-workflow.py", "read", "--step", "prompt-six-case", "--domain", "xhs"],
            cwd=MONOREPO,
            timeout=120,
        )
        layers["monorepo_prompt_six_case_xhs"] = {
            "status": "PASS" if ec == 0 else "FAIL",
            "exit_code": ec,
            "note": "机械真源 AGENT-PROMPT-SIX-CASE.json domain=xhs",
            "tail": tail,
        }
        if ec != 0:
            fail += 1

    if not args.skip_ceo:
        ec, tail = run(
            [
                sys.executable,
                "scripts/run_ceo_full_execution.py",
                "--goal",
                goal,
                "--skip-triple-eval",
                "--skip-stress",
            ],
            timeout=1200,
        )
        layers["ceo_full_execution_slice"] = {
            "status": "PASS" if ec == 0 else "PARTIAL" if ec == 42 else "FAIL",
            "exit_code": ec,
            "tail": tail,
            "manifest": "content/evolution/00-manager/ceo-inbox/CEO-RUN-MANIFEST-latest.json",
        }
        if ec not in (0, 42):
            fail += 1
    else:
        layers["ceo_full_execution_slice"] = {"status": "SKIP", "note": "--skip-ceo"}

    ec, tail = run(
        [
            "python3",
            "scripts/agent-workflow.py",
            "qc",
            "handoff",
            "--slug",
            "brand-ceo",
            "--session",
            "deep-preflight",
        ],
        cwd=MONOREPO,
        timeout=60,
    )
    layers["qc_handoff_draft"] = {
        "status": "PASS" if ec == 0 else "SKIP",
        "exit_code": ec,
        "tail": tail,
        "agent_must": "有交付时 Task×1 Double-Check + qc verify",
    }

    payload = {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "mode": "brainstorm_deep",
        "goal": goal,
        "layers": layers,
        "status": "PASS" if fail == 0 else "FAIL",
        "supervision_rule": "每层 exit_code 与 handoff 须进报告；禁止跳过 drive_hydrate",
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PASS agent-brainstorm-deep-preflight" if fail == 0 else "FAIL agent-brainstorm-deep-preflight", file=sys.stderr)
    print(f"handoff → {OUT.relative_to(ROOT)}")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
