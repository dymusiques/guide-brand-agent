#!/usr/bin/env python3
"""Mechanical QC report from research-gate layers → verify-qc-report (13-QC 合同)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MONOREPO = Path.home() / "Desktop/未命名"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", required=True)
    ap.add_argument("--gate-json", type=Path, required=True)
    args = ap.parse_args()
    gate = json.loads(args.gate_json.read_text(encoding="utf-8")) if args.gate_json.is_file() else {}
    report_dir = MONOREPO / "tmp/double-check" / args.session
    report_dir.mkdir(parents=True, exist_ok=True)
    report = report_dir / "report.md"
    layers = gate.get("layers") or []
    lines = [
        "# QC Report · research-gate",
        "",
        "## Scope",
        f"- goal: {gate.get('goal', '')}",
        f"- gate status: {gate.get('status')}",
        "",
        "## C2 evidence",
        f"- c2 log: {ROOT / 'tmp/research-gate-c2.log'}",
        "",
        "## Layer audit",
    ]
    for L in layers:
        lines.append(f"- {L.get('name')}: {L.get('status')} (exit {L.get('exit_code', '')})")
    fail = gate.get("fail_count", 0)
    verdict = "PASS" if fail == 0 else "FAIL"
    lines.extend(
        [
            "",
            "## Delivery wording",
            "- 门禁层全部 PASS 时才允许声称全链路调研",
            "",
            "## Verdict",
            f"QC_VERDICT: {verdict}",
        ]
    )
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    r = subprocess.run(
        ["python3", "scripts/verify-qc-report.py", "--report", str(report)],
        cwd=MONOREPO,
        capture_output=True,
        text=True,
    )
    print((r.stdout or "") + (r.stderr or ""))
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
