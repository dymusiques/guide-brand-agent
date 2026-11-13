#!/usr/bin/env python3
"""
硬门禁：对 pending 口播给薯条/标题/选题/地点/视角类建议前必须 PASS。

- inbox 变更 → 自动跑 evaluate + facts manifest（禁止 Agent 手读旧 JSON）
- exit 0 →  stdout 打印须引用的 decision_summary；写入 advice-gate handoff
- exit 1 → 禁止交付建议
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "content/xiaohongshu/inbox/pending-videos"
FACTS = ROOT / "integration/handoff/owner-pending-videos-facts-latest.json"
EVAL = ROOT / "integration/handoff/owner-pending-videos-eval-latest.json"
GATE_OUT = ROOT / "integration/handoff/owner-pending-videos-advice-gate-latest.json"
PY = ROOT / ".venv/bin/python"
if not PY.is_file():
    PY = Path(sys.executable)


def inbox_latest_mtime() -> float:
    skip = {"readme.md", "template.md"}
    mt = 0.0
    for p in INBOX.glob("*.md"):
        if p.name.lower() in skip:
            continue
        mt = max(mt, p.stat().st_mtime)
    return mt


def needs_refresh() -> bool:
    if not FACTS.is_file() or not EVAL.is_file():
        return True
    try:
        data = json.loads(FACTS.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return True
    latest = inbox_latest_mtime()
    manifest_mtime = float(data.get("inbox_latest_mtime") or 0)
    if latest > manifest_mtime + 0.5:
        return True
    mtimes = data.get("inbox_file_mtimes") or {}
    for rel, m in mtimes.items():
        p = ROOT / rel
        if p.is_file() and abs(p.stat().st_mtime - float(m)) > 0.5:
            return True
    if FACTS.stat().st_mtime < latest:
        return True
    return False


def run_pipeline_refresh() -> None:
    subprocess.check_call(
        ["bash", "scripts/run-owner-pending-videos-eval.sh", "--no-open"],
        cwd=ROOT,
    )


def load_facts() -> dict:
    return json.loads(FACTS.read_text(encoding="utf-8"))


def validate_facts(data: dict) -> list[str]:
    errs: list[str] = []
    if not str(data.get("scoring_model", "")).startswith("rule-v2-full-body"):
        errs.append("facts scoring_model 非 rule-v2-full-body")
    for it in data.get("items") or []:
        nf = it.get("narrative_facts")
        if not isinstance(nf, dict):
            errs.append(f"{it.get('id')}: 缺 narrative_facts")
            continue
        if "decision_summary" not in it:
            errs.append(f"{it.get('id')}: 缺 decision_summary")
    eval_data = {}
    if EVAL.is_file():
        eval_data = json.loads(EVAL.read_text(encoding="utf-8"))
    if not str(eval_data.get("scoring_model", "")).startswith("rule-v2-full-body"):
        errs.append("eval scoring_model 非 rule-v2-full-body")
    for it in eval_data.get("items") or []:
        if "narrative_facts" not in it:
            errs.append(f"eval {it.get('id')}: 缺 narrative_facts")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--files",
        help="逗号分隔的 inbox 文件名或 stem；默认全 inbox",
    )
    ap.add_argument(
        "--no-refresh",
        action="store_true",
        help="禁止自动 refresh（仅 CI；Agent 勿用）",
    )
    ap.add_argument(
        "--intent",
        choices=("advice", "brainstorm"),
        default="advice",
        help="advice=给结论前必过；brainstorm=创意讨论豁免（不许据此下事实结论）",
    )
    ap.add_argument(
        "--quiet",
        action="store_true",
        help="CEO 自动化：stdout 一行，不打印全文 decision_summary",
    )
    args = ap.parse_args()

    if args.intent == "brainstorm":
        gate = {
            "as_of": datetime.now(timezone.utc).isoformat(),
            "status": "EXEMPT",
            "advice_allowed": False,
            "mode": "brainstorm",
            "agent_must": "brainstorm 结束若要给薯条/标题/地点/叙事结论 → 再跑 --intent advice",
            "forbidden_in_brainstorm": [
                "引用 decision_summary 作事实",
                "human_glance_only",
                "body_preview",
            ],
        }
        GATE_OUT.parent.mkdir(parents=True, exist_ok=True)
        GATE_OUT.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("EXEMPT pending-advice-gate (brainstorm)")
        return 0

    if needs_refresh():
        if args.no_refresh:
            print("FAIL pending-videos facts stale — run: bash scripts/run-owner-pending-videos-eval.sh", file=sys.stderr)
            return 1
        run_pipeline_refresh()

    if not FACTS.is_file():
        print("FAIL missing facts manifest", file=sys.stderr)
        return 1

    data = load_facts()
    errs = validate_facts(data)
    if errs:
        print("FAIL facts validation:\n- " + "\n- ".join(errs), file=sys.stderr)
        return 1

    selected = data.get("items") or []
    if args.files:
        want = {x.strip() for x in args.files.split(",") if x.strip()}
        selected = [
            it
            for it in selected
            if it.get("id") in want
            or it.get("file", "").split("/")[-1] in want
            or any(w in it.get("file", "") for w in want)
        ]
        if not selected:
            print("FAIL --files 未匹配任何 inbox 项", file=sys.stderr)
            return 1

    gate = {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "advice_allowed": True,
        "mode": "advice",
        "intent": args.intent,
        "agent_must_cite": "integration/handoff/owner-pending-videos-facts-latest.json → items[].decision_summary",
        "delivery_must_include_line": "GATE: PASS · pending-advice · <as_of>",
        "forbidden_for_decisions": data.get("forbidden_for_decisions"),
        "selected_ids": [it["id"] for it in selected],
        "decision_summaries": {it["id"]: it["decision_summary"] for it in selected},
    }
    GATE_OUT.parent.mkdir(parents=True, exist_ok=True)
    GATE_OUT.write_text(json.dumps(gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.quiet:
        print(f"PASS pending-advice-gate as_of={gate['as_of'][:19]} items={len(selected)}")
        return 0

    print("PASS agent-gate-pending-videos-advice")
    print("CITE facts manifest (full-md parse) — 禁止 body_preview:")
    for it in selected:
        print(f"  · {it['id']}: {it['decision_summary']}")
    print(f"handoff → {GATE_OUT.relative_to(ROOT)}")
    print(f"交付结论时回复须含: {gate['delivery_must_include_line']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
