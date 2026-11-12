#!/usr/bin/env python3
"""C2：品牌 AUTO 阶段门控（读 monorepo TIMELINE JSON，脚本仍在品牌仓）。"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = ROOT / "content/evolution/00-manager/ceo-inbox/CEO-RUN-MANIFEST-latest.json"


def find_monorepo() -> Path | None:
    for key in ("DANYING_AGENT_WORKSPACE", "DANYING_AGENT_MONOREPO"):
        raw = os.environ.get(key, "").strip()
        if raw:
            p = Path(raw).expanduser().resolve()
            if (p / "docs/agent/AGENT-BRAND-CEO-AUTO-TIMELINE.json").is_file():
                return p
    for p in (
        Path.home() / "Desktop/未命名",
        Path.home() / "Desktop/danying-agent-workspace",
    ):
        if (p / "docs/agent/AGENT-BRAND-CEO-AUTO-TIMELINE.json").is_file():
            return p.resolve()
    return None


def phase_from_timeline(monorepo: Path, phase_id: str) -> dict | None:
    path = monorepo / "docs/agent/AGENT-BRAND-CEO-AUTO-TIMELINE.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    phases = data.get("phases") or []
    legacy = data.get("legacy_id_index") or {"3d": "6-9", "3c": "6-10", "3b": "6-8"}
    resolved = legacy.get(phase_id, phase_id)
    return next((p for p in phases if p.get("id") == resolved), None)


def qc_report_pass(report: Path) -> bool:
    if not report.is_file():
        return False
    lines = [ln.strip() for ln in report.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return bool(lines) and lines[-1] == "QC_VERDICT: PASS"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True, help="6-1…6-11 or legacy 3d/3c")
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--qc-report", type=Path, help="13-QC report.md（可相对 monorepo）")
    args = ap.parse_args()

    monorepo = find_monorepo()
    if not monorepo:
        print("FAIL monorepo not found (set DANYING_AGENT_WORKSPACE)", file=sys.stderr)
        return 1

    phase = phase_from_timeline(monorepo, args.phase.strip())
    if not phase:
        print(f"FAIL unknown phase {args.phase!r}", file=sys.stderr)
        return 1

    mpath = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    manifest: dict = {}
    if mpath.is_file():
        manifest = json.loads(mpath.read_text(encoding="utf-8"))

    fails: list[str] = []
    pid = phase.get("id")

    if pid == "6-10" or args.phase.strip() in ("3c", "6-10"):
        prereq = phase.get("prerequisite_phase") or phase.get("prerequisite") or ""
        if "6-9" in str(prereq) or "6-9" in str(phase):
            qc_ok = (manifest.get("qc_verdict") or "").upper() == "PASS"
            report = args.qc_report
            if report:
                if not report.is_absolute():
                    report = monorepo / report
                qc_ok = qc_ok or qc_report_pass(report)
            if not qc_ok:
                fails.append(
                    "phase 6-10/3c blocked: need qc_verdict PASS or --qc-report with QC_VERDICT: PASS"
                )
        owner_uri = (manifest.get("owner_html_uri") or "").strip()
        if not owner_uri and args.phase.strip() in ("3c", "6-10"):
            fails.append("owner_html_uri empty — run owner-delivery script before 3c gate")

    if fails:
        for f in fails:
            print(f"FAIL {f}", file=sys.stderr)
        return 1

    print(f"PASS verify-ceo-brand-phase phase={pid} · {phase.get('label')}")
    print(f"  timeline: {monorepo / 'docs/agent/AGENT-BRAND-CEO-AUTO-TIMELINE.json'}")
    for label in ("verify_in_brand_repo", "monorepo_run"):
        val = phase.get(label)
        if val:
            for line in val:
                print(f"  {label}: {line}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
