#!/usr/bin/env python3
"""
Append/update high-engagement post snapshots for V-Tier copy benchmarks.
Agent Must run before each dual-track write cycle when corpus is stale or brief is new.

  .venv/bin/python scripts/refresh-owner-copy-v-tier-live-corpus.py --from-json patch.json
  .venv/bin/python scripts/refresh-owner-copy-v-tier-live-corpus.py --verify-only
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from owner_copy_v_tier_corpus_lib import (  # noqa: E402
    CORPUS_PATH,
    append_log,
    load_corpus,
    save_corpus,
    upsert_entries,
    validate_entry,
    engagement_floors,
)

STALE_DAYS = 14


def corpus_is_stale(corpus: dict) -> bool:
    updated = corpus.get("updated_at") or corpus.get("checked_at") or "1970-01-01"
    try:
        dt = datetime.strptime(updated[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return True
    return datetime.now(timezone.utc) - dt > timedelta(days=STALE_DAYS)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--from-json", help="File with {entries:[...]} to merge")
    p.add_argument("--verify-only", action="store_true")
    p.add_argument("--export-csv", action="store_true")
    args = p.parse_args()

    if not CORPUS_PATH.is_file():
        print(f"FAIL: missing {CORPUS_PATH.relative_to(ROOT)}")
        return 1

    corpus = load_corpus()
    floors = engagement_floors(corpus)

    if args.from_json:
        patch = json.loads(Path(args.from_json).read_text(encoding="utf-8"))
        entries = patch.get("entries") or patch
        if isinstance(entries, dict):
            entries = [entries]
        corpus, errs = upsert_entries(corpus, entries)
        if errs:
            for e in errs:
                print(f"WARN: skip entry: {e}")
        save_corpus(corpus)
        append_log("upsert", {"count": len(entries), "errors": len(errs)})
        print(f"OK corpus updated · entries={len(corpus.get('entries') or [])}")

    if args.verify_only or not args.from_json:
        fails = 0
        creators = set()
        plats = set()
        for e in corpus.get("entries") or []:
            for msg in validate_entry(e, floors):
                print(f"FAIL entry {e.get('id')}: {msg}")
                fails += 1
            creators.add(e.get("creator_handle"))
            plats.add(e.get("platform"))
        if len(corpus.get("entries") or []) < 6:
            print(f"FAIL: corpus needs >=6 post entries, got {len(corpus.get('entries') or [])}")
            fails += 1
        if len(creators) < 4:
            print(f"FAIL: need >=4 distinct creators, got {len(creators)}")
            fails += 1
        for need in ("xiaohongshu", "linkedin", "medium"):
            if need not in plats:
                print(f"FAIL: missing platform in corpus: {need}")
                fails += 1
        if corpus_is_stale(corpus):
            print(f"WARN: corpus updated_at older than {STALE_DAYS}d — refresh high-engagement posts before write")
        if fails:
            return 1
        print("PASS refresh-owner-copy-v-tier-live-corpus --verify-only")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
