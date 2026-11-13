#!/usr/bin/env python3
"""Agent 维护 classify 触发词 overlay（补词）；不改动交付原则，仅扩 CEO/匹配口语。"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "integration/handoff/pending-videos-goal-phrases.json"
BUCKETS = ("eval", "advice", "owner_decision", "brainstorm")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--phrase", required=True)
    ap.add_argument(
        "--bucket",
        required=True,
        choices=BUCKETS,
        help="eval=全量评估 | owner_decision=拍板口令 | advice=语境词 | brainstorm=讨论",
    )
    ap.add_argument("--note", default="")
    ap.add_argument(
        "--apply",
        action="store_true",
        help="写入 overlay（默认只打印 proposal）",
    )
    args = ap.parse_args()
    phrase = args.phrase.strip()
    if not phrase:
        print("FAIL empty phrase", file=__import__("sys").stderr)
        return 1

    data: dict = {"version": 1, "phrases": {}}
    if OUT.is_file():
        data = json.loads(OUT.read_text(encoding="utf-8"))
    phrases = data.setdefault("phrases", {b: [] for b in BUCKETS})
    for b in BUCKETS:
        phrases.setdefault(b, [])
    if phrase in phrases[args.bucket]:
        print(f"OK already in {args.bucket}: {phrase}")
        return 0

    entry = {
        "phrase": phrase,
        "added_at": datetime.now(timezone.utc).isoformat(),
        "note": args.note,
    }
    proposal = {**data, "last_proposal": entry}

    if not args.apply:
        print(json.dumps(proposal, ensure_ascii=False, indent=2))
        print("Proposal only — rerun with --apply to write overlay")
        return 0

    phrases[args.bucket].append(phrase if not args.note else {"phrase": phrase, "note": args.note})
    data["phrases"] = phrases
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK added to {args.bucket}: {phrase} → {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
