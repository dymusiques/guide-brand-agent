#!/usr/bin/env python3
"""
Verify pre-draft V-Tier benchmark review against live high-engagement corpus.
Does NOT score Owner prose style.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CULTURAL_POOL = ROOT / "integration/handoff/owner-copy-v-tier-cultural-art-creators.json"
sys.path.insert(0, str(ROOT / "scripts"))

from owner_copy_v_tier_corpus_lib import (  # noqa: E402
    CORPUS_PATH,
    append_log,
    index_by_id,
    load_corpus,
    norm_platform,
    save_corpus,
    upsert_entries,
    validate_entry,
    engagement_floors,
)

ATTEST_DIR = ROOT / "content/xiaohongshu/v-tier-attestations"
MAX_AGE_DAYS = 30


def brief_requires_attestation(brief_path: Path) -> bool:
    name = brief_path.name.casefold()
    if "discovery-" in name or name.endswith("-test-brief.md"):
        return False
    if "flutebuddy" in name or "owner-ip" in name or "personal-ip" in name:
        return True
    if brief_path.is_file():
        head = brief_path.read_text(encoding="utf-8", errors="replace")[:4000]
        if "owner-copy-v-tier" in head or "V-Tier" in head or "v-tier-attestation" in head:
            return True
        if re.search(r"FluteBuddy|个人IP|生态链|张丹瀛", head):
            return True
    return False


def attestation_path_for(brief_path: Path) -> Path:
    rel = brief_path if brief_path.is_absolute() else ROOT / brief_path
    return ATTEST_DIR / f"{rel.name}.json"


def parse_date(s: str) -> datetime | None:
    s = (s or "").strip()
    if not s:
        return None
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        pass
    try:
        return datetime.strptime(s[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def cultural_handle_set() -> set[str]:
    if not CULTURAL_POOL.is_file():
        return set()
    pool = json.loads(CULTURAL_POOL.read_text(encoding="utf-8"))
    names: set[str] = set()
    for c in pool.get("creators") or []:
        h = (c.get("handle") or "").strip()
        if h:
            names.add(h.casefold())
        for a in c.get("aliases") or []:
            names.add(str(a).casefold())
    for alias in (pool.get("owner_aliases") or {}).keys():
        names.add(alias.casefold())
    return names


def entry_is_cultural_art(e: dict) -> bool:
    tags = {str(t).casefold() for t in (e.get("owner_tags") or e.get("tags") or [])}
    if "cultural_art_aesthetic" in tags:
        return True
    handle = (e.get("creator_handle") or e.get("handle") or "").casefold()
    return handle in cultural_handle_set()


def collect_referenced_entries(data: dict, corpus: dict) -> tuple[list[dict], list[str]]:
    """Resolve corpus ids + session_fresh_posts + legacy benchmarks_reviewed."""
    fails: list[str] = []
    by_id = index_by_id(corpus)
    out: list[dict] = []

    for cid in data.get("corpus_entry_ids") or []:
        e = by_id.get(cid)
        if not e:
            fails.append(f"unknown corpus_entry_id: {cid}")
        else:
            out.append(e)

    for raw in data.get("session_fresh_posts") or []:
        out.append(dict(raw))

    # legacy
    for raw in data.get("benchmarks_reviewed") or []:
        e = dict(raw)
        e.setdefault("post_url", e.get("url"))
        e.setdefault("creator_handle", e.get("handle"))
        e.setdefault("platform", e.get("platform"))
        eng = e.get("engagement") or {}
        if e.get("likes") and not eng:
            eng = {"likes": e.get("likes")}
        if not eng and e.get("followers_approx"):
            eng = {"likes": 0}
        e["engagement"] = eng
        e.setdefault("title", e.get("title") or "untitled")
        e.setdefault("captured_at", data.get("checked_at"))
        e.setdefault("source", "legacy benchmarks_reviewed")
        out.append(e)

    return out, fails


def validate_session(entries: list[dict], floors: dict) -> list[str]:
    fails: list[str] = []
    if len(entries) < 3:
        fails.append(f"need >=3 referenced posts total, got {len(entries)}")
    creators = {e.get("creator_handle") or e.get("handle") for e in entries}
    creators.discard(None)
    creators.discard("")
    if len(creators) < 3:
        fails.append(f"need >=3 distinct creators, got {len(creators)}")
    plats = {norm_platform(str(e.get("platform", ""))) for e in entries}
    if "xiaohongshu" not in plats:
        fails.append("need xiaohongshu in set")
    if not plats.intersection({"linkedin", "medium"}):
        fails.append("need linkedin or medium in set")
    for i, e in enumerate(entries):
        fails.extend([f"ref[{i}] {msg}" for msg in validate_entry(e, floors)])
    return fails


def attestation_stale(data: dict, brief_path: Path) -> bool:
    checked = parse_date(str(data.get("checked_at", "")))
    if not checked:
        return True
    age = datetime.now(timezone.utc) - checked
    if age <= timedelta(days=MAX_AGE_DAYS):
        return False
    brief_mtime = datetime.fromtimestamp(brief_path.stat().st_mtime, tz=timezone.utc)
    return brief_mtime > checked


def main() -> int:
    p = argparse.ArgumentParser(description="V-Tier attestation + live corpus trace")
    p.add_argument("--brief", required=True)
    p.add_argument("--strict-discovery", action="store_true")
    p.add_argument("--merge-corpus", action="store_true", default=True)
    p.add_argument("--no-merge-corpus", action="store_false", dest="merge_corpus")
    args = p.parse_args()

    brief_rel = args.brief.strip().lstrip("/")
    brief_path = ROOT / brief_rel
    if not brief_path.is_file():
        print(f"FAIL: brief missing: {brief_rel}")
        return 1

    if not args.strict_discovery and not brief_requires_attestation(brief_path):
        print(f"SKIP verify-owner-copy-v-tier-attestation: {brief_rel}")
        return 0

    if not CORPUS_PATH.is_file():
        print("FAIL: missing owner-copy-v-tier-live-corpus.json")
        return 1

    ap = attestation_path_for(brief_path)
    if not ap.is_file():
        print(f"FAIL: missing attestation: {ap.relative_to(ROOT)}")
        print("HINT: docs/OWNER-COPY-V-TIER-LIVE-CORPUS-SOP.md")
        return 1

    data = json.loads(ap.read_text(encoding="utf-8"))
    if data.get("brief") and data["brief"] != brief_rel:
        print(f"FAIL: attestation brief mismatch")
        return 1

    fresh = data.get("session_fresh_posts") or []
    if len(fresh) < 1:
        print("FAIL: session_fresh_posts must have >=1 newly scraped high-engagement post")
        return 1

    intent = (data.get("style_transfer_intent") or "").strip()
    if len(intent) < 30:
        print("FAIL: style_transfer_intent too short")
        return 1
    if data.get("owner_review_still_required") is not True:
        print("FAIL: owner_review_still_required must be true")
        return 1

    checked = parse_date(str(data.get("checked_at", "")))
    if not checked:
        print("FAIL: checked_at invalid")
        return 1

    corpus = load_corpus()
    floors = engagement_floors(corpus)
    entries, id_fails = collect_referenced_entries(data, corpus)
    fails = id_fails + validate_session(entries, floors)
    if not any(entry_is_cultural_art(e) for e in entries):
        fails.append(
            "need >=1 cultural_art_aesthetic post (谢胜子/天才女友GG/艺术审美向) — "
            "see owner-copy-v-tier-cultural-art-creators.json"
        )
    if attestation_stale(data, brief_path):
        fails.append(f"attestation stale (> {MAX_AGE_DAYS}d) vs brief mtime")

    if fails:
        for f in fails:
            print(f"FAIL: {f}")
        return 1

    if args.merge_corpus and fresh:
        corpus, errs = upsert_entries(corpus, fresh)
        save_corpus(corpus)
        append_log(
            "attestation_merge",
            {"brief": brief_rel, "fresh_count": len(fresh), "merge_errors": errs},
        )
        for e in errs:
            print(f"WARN merge: {e}")

    append_log(
        "attestation_pass",
        {
            "brief": brief_rel,
            "corpus_entry_ids": data.get("corpus_entry_ids"),
            "session_fresh_ids": [x.get("id") for x in fresh],
            "creators": list({x.get("creator_handle") for x in entries}),
        },
    )

    print(f"PASS verify-owner-copy-v-tier-attestation · {ap.relative_to(ROOT)}")
    print("NOTE: PASS = traceable high-engagement comparables logged; NOT = draft matches V-Tier prose.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
