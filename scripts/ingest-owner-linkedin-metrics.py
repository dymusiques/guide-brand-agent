#!/usr/bin/env python3
"""Ingest LinkedIn post metrics MD/JSON → posts.jsonl + handoff latest."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.multichannel_intake_md import parse_metrics_md  # noqa: E402

INBOX = ROOT / "content/analytics/linkedin/inbox"
LEDGER = ROOT / "content/analytics/linkedin/posts.jsonl"
OUT = ROOT / "integration/handoff/owner-linkedin-metrics-latest.json"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="", help="path under inbox or absolute")
    ap.add_argument("--scan-inbox", action="store_true", help="ingest all new md except TEMPLATE")
    args = ap.parse_args()
    if not args.scan_inbox and not args.file:
        ap.error("need --file or --scan-inbox")

    paths: list[Path] = []
    if args.scan_inbox:
        paths = [p for p in sorted(INBOX.glob("*.md")) if not p.name.upper().startswith("TEMPLATE")]
    else:
        p = Path(args.file)
        if not p.is_absolute():
            p = ROOT / p
        paths = [p]

    if not paths:
        print("WARN no files", file=sys.stderr)
        return 0

    records: list[dict] = []
    for p in paths:
        if not p.is_file():
            print(f"FAIL missing {p}", file=sys.stderr)
            return 2
        if p.suffix.lower() == ".json":
            rec = json.loads(p.read_text(encoding="utf-8"))
            rec.setdefault("platform", "linkedin")
            rec["source_file"] = p.name
        else:
            rec = parse_metrics_md(p, platform="linkedin")
        rec["ingested_at"] = datetime.now(timezone.utc).isoformat()
        records.append(rec)
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        with LEDGER.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    payload = {
        "schema": "owner_linkedin_metrics_v1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "count_ingested": len(records),
        "items": records,
        "ledger": str(LEDGER.relative_to(ROOT)),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "ingested": len(records), "handoff": str(OUT.relative_to(ROOT))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())