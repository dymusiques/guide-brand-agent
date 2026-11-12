#!/usr/bin/env python3
"""C2：CEO-RUN-MANIFEST 诚实性 · 对照 monorepo AGENT-BRAND-CEO-ROSTER.json（不复制战役逻辑）。"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFEST = ROOT / "content/evolution/00-manager/ceo-inbox/CEO-RUN-MANIFEST-latest.json"

sys.path.insert(0, str(ROOT / "scripts"))
from ceo_agent_roster import AGENT_CATALOG  # noqa: E402

CATALOG_IDS = {aid for aid, _, _ in AGENT_CATALOG}


def resolve_monorepo(contract: Path | None) -> Path | None:
    if contract and contract.is_file():
        return contract.resolve().parents[2] if "docs" in contract.parts else contract.parent
    for key in ("DANYING_AGENT_WORKSPACE", "DANYING_AGENT_MONOREPO"):
        raw = os.environ.get(key, "").strip()
        if raw:
            p = Path(raw).expanduser().resolve()
            if (p / "docs/agent/AGENT-BRAND-CEO-ROSTER.json").is_file():
                return p
    candidates = [
        Path.home() / "Desktop/未命名",
        Path.home() / "Desktop/danying-agent-workspace",
    ]
    for p in candidates:
        if (p / "docs/agent/AGENT-BRAND-CEO-ROSTER.json").is_file():
            return p.resolve()
    return None


def load_contract(contract: Path | None) -> dict:
    monorepo = resolve_monorepo(contract)
    path = contract
    if path is None and monorepo:
        path = monorepo / "docs/agent/AGENT-BRAND-CEO-ROSTER.json"
    if not path or not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def check_qc_report(report: Path) -> tuple[bool, str]:
    if not report.is_file():
        return False, f"qc report missing: {report}"
    text = report.read_text(encoding="utf-8")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    if not lines:
        return False, "qc report empty"
    last = lines[-1]
    if not re.match(r"^QC_VERDICT: (PASS|FAIL)$", last):
        return False, f"qc report last line must be QC_VERDICT: … got {last!r}"
    if last.endswith("FAIL"):
        return False, "qc report QC_VERDICT: FAIL"
    return True, "qc PASS"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument(
        "--contract",
        type=Path,
        help="monorepo AGENT-BRAND-CEO-ROSTER.json（默认自动发现）",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="skipped 行必须有 skip_reason 非空",
    )
    ap.add_argument(
        "--require-qc",
        action="store_true",
        help="有 owner_html_uri 时必须 qc_verdict=PASS 或 --qc-report PASS",
    )
    ap.add_argument("--qc-report", type=Path, help="monorepo tmp/double-check/.../report.md")
    args = ap.parse_args()

    mpath = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    if not mpath.is_file():
        print(f"FAIL manifest missing {mpath}", file=sys.stderr)
        return 1

    data = json.loads(mpath.read_text(encoding="utf-8"))
    fails: list[str] = []
    warns: list[str] = []

    roster = data.get("roster") or []
    by_id = {str(r.get("id")): r for r in roster if r.get("id") is not None}

    if set(by_id.keys()) != CATALOG_IDS:
        missing = CATALOG_IDS - set(by_id.keys())
        extra = set(by_id.keys()) - CATALOG_IDS
        if missing:
            fails.append(f"roster missing ids: {sorted(missing)}")
        if extra:
            fails.append(f"roster unexpected ids: {sorted(extra)}")

    for rid, row in sorted(by_id.items()):
        st = row.get("status")
        if st not in ("invoked", "skipped"):
            fails.append(f"role {rid}: status must invoked|skipped, got {st!r}")
        if st == "skipped":
            reason = (row.get("skip_reason") or "").strip()
            if args.strict and not reason:
                fails.append(f"role {rid}: skipped without skip_reason (--strict)")
            elif not reason and not args.strict:
                warns.append(f"role {rid}: skipped without skip_reason (add for honesty)")

    par = data.get("parallelism") or {}
    if par.get("all_agents_invoked") is True:
        fails.append("parallelism.all_agents_invoked=true forbidden (全员 invoke)")

    owner_uri = (data.get("owner_html_uri") or "").strip()
    qc_verdict = (data.get("qc_verdict") or "").strip().upper()
    qc_session = (data.get("qc_session") or "").strip()

    contract = load_contract(args.contract)
    forbidden = (contract.get("manifest_contract") or {}).get("forbidden") or []
    if args.require_qc and owner_uri:
        if qc_verdict != "PASS":
            fails.append(
                "owner_html_uri set but qc_verdict != PASS "
                "(set manifest qc_verdict + qc_session after 13-QC)"
            )

    if args.require_qc or (owner_uri and args.qc_report):
        report = args.qc_report
        if report and not report.is_absolute():
            monorepo = resolve_monorepo(args.contract)
            if monorepo:
                report = monorepo / report
            else:
                report = Path(report).expanduser()
        if report:
            ok, msg = check_qc_report(report)
            if not ok:
                fails.append(msg)
        elif qc_verdict != "PASS":
            fails.append("--require-qc: need qc_verdict PASS or --qc-report")

    if qc_session and not re.match(r"^[\w\-]+$", qc_session):
        fails.append("qc_session should be session slug (e.g. brand-ceo-20260312)")

    for w in warns:
        print(f"WARN {w}")

    if fails:
        for f in fails:
            print(f"FAIL {f}", file=sys.stderr)
        print(f"FAIL verify-ceo-run-manifest ({len(fails)} issue(s))", file=sys.stderr)
        return 1

    print(f"PASS verify-ceo-run-manifest manifest={mpath.name} roles={len(by_id)}")
    if qc_session:
        print(f"  qc_session: {qc_session}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
