#!/usr/bin/env python3
"""Shared schema + validation for V-Tier live high-engagement post corpus."""

from __future__ import annotations

import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CORPUS_PATH = ROOT / "integration/handoff/owner-copy-v-tier-live-corpus.json"
LOG_PATH = ROOT / "content/evolution/00-manager/ceo-inbox/owner-copy-v-tier-corpus-log.jsonl"

PLATFORM_ALIASES = {
    "xhs": "xiaohongshu",
    "小红书": "xiaohongshu",
    "linkedin": "linkedin",
    "medium": "medium",
}

PROFILE_URL_MARKERS = (
    "/user/profile/",
    "/search_result?",
    "/in/",
    "medium.com/@",
)
# post URL heuristics — must look like a single post
POST_URL_HINTS = (
    "/posts/",
    "/activity-",
    "xiaohongshu.com/explore/",
    "xhslink.com",
    "medium.com/@",
    "/p/",
)


def norm_platform(p: str) -> str:
    k = (p or "").strip().casefold()
    return PLATFORM_ALIASES.get(k, k)


def is_profile_or_search_url(url: str) -> bool:
    u = url.casefold()
    if "/activity-" in u or "/explore/" in u:
        return False
    if u.rstrip("/").endswith("medium.com") or re.search(r"medium\.com/@[^/]+$", u):
        return True
    if "linkedin.com/in/" in u and "/posts/" not in u and "activity-" not in u:
        return True
    for m in PROFILE_URL_MARKERS:
        if m in u and "activity-" not in u and "/explore/" not in u:
            if m == "medium.com/@" and re.search(r"medium\.com/@[^/]+/[^/]+", u):
                return False
            if m in ("/user/profile/", "/search_result?"):
                return True
    return False


def load_corpus(path: Path | None = None) -> dict:
    p = path or CORPUS_PATH
    return json.loads(p.read_text(encoding="utf-8"))


def save_corpus(data: dict, path: Path | None = None) -> None:
    p = path or CORPUS_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def engagement_floors(corpus: dict) -> dict:
    return corpus.get("engagement_floors") or {}


def entry_meets_floor(entry: dict, floors: dict) -> list[str]:
    fails: list[str] = []
    plat = norm_platform(str(entry.get("platform", "")))
    eng = entry.get("engagement") or {}
    fl = floors.get(plat) or floors.get("default") or {}
    likes = eng.get("likes") or eng.get("reactions") or 0
    comments = eng.get("comments") or 0
    claps = eng.get("claps") or 0
    min_likes = fl.get("min_likes_or_reactions") or 0
    min_claps = fl.get("min_claps") or 0
    min_comments = fl.get("min_comments") or 0
    high_interaction = comments >= 500 and (likes >= 1000 or claps >= 1000)
    if plat == "medium":
        if claps < min_claps and min_claps and not high_interaction:
            fails.append(f"claps {claps} < {min_claps}")
    else:
        if likes < min_likes and min_likes and not high_interaction:
            fails.append(f"likes/reactions {likes} < {min_likes}")
    if comments < min_comments and min_comments and not high_interaction:
        fails.append(f"comments {comments} < {min_comments}")
    followers = entry.get("creator_followers_approx") or 0
    min_f = corpus_min_followers(entry, floors)
    if isinstance(followers, int) and min_f and followers < min_f:
        if not (entry.get("high_engagement_exception") or entry.get("engagement_verified_via")):
            fails.append(f"creator_followers_approx {followers} < {min_f}")
    return fails


def corpus_min_followers(entry: dict, floors: dict) -> int:
    plat = norm_platform(str(entry.get("platform", "")))
    fl = floors.get(plat) or {}
    return int(fl.get("min_creator_followers") or 0)


def validate_entry(entry: dict, floors: dict | None = None) -> list[str]:
    fails: list[str] = []
    plat = norm_platform(str(entry.get("platform", "")))
    if plat not in ("xiaohongshu", "linkedin", "medium"):
        fails.append(f"invalid platform: {entry.get('platform')}")
    url = (entry.get("post_url") or entry.get("url") or "").strip()
    if not url.startswith("http"):
        fails.append("post_url must be http(s)")
    elif is_profile_or_search_url(url) and not entry.get("engagement_verified_via"):
        fails.append("post_url must be a single post/article, not profile/search/home")
    plat_native = (entry.get("platform_native_url") or "").strip()
    if norm_platform(str(entry.get("platform", ""))) == "xiaohongshu":
        if "xiaohongshu.com/explore/" not in url and "xhslink.com" not in url:
            if not entry.get("engagement_verified_via") and not plat_native:
                fails.append("xiaohongshu: need explore/xhslink URL or engagement_verified_via + session refresh")
    title = (entry.get("title") or "").strip()
    if len(title) < 8:
        fails.append("title too short")
    handle = (entry.get("creator_handle") or entry.get("handle") or "").strip()
    if not handle:
        fails.append("creator_handle required")
    eng = entry.get("engagement") or {}
    if not any(eng.get(k) for k in ("likes", "reactions", "claps", "comments", "reads")):
        fails.append("engagement must include at least one metric")
    if floors:
        fails.extend(entry_meets_floor(entry, floors))
    captured = (entry.get("captured_at") or "").strip()
    if not captured:
        fails.append("captured_at required")
    source = (entry.get("source") or "").strip()
    if len(source) < 5:
        fails.append("source required (how metrics were verified)")
    return fails


def append_log(action: str, payload: dict) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": action,
        **payload,
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def upsert_entries(corpus: dict, new_entries: list[dict]) -> tuple[dict, list[str]]:
    """Merge by post_url; assign id if missing."""
    errors: list[str] = []
    floors = engagement_floors(corpus)
    by_url: dict[str, dict] = {}
    for e in corpus.get("entries") or []:
        u = (e.get("post_url") or "").strip()
        if u:
            by_url[u] = e
    for raw in new_entries:
        e = dict(raw)
        e["platform"] = norm_platform(str(e.get("platform", "")))
        fails = validate_entry(e, floors)
        if fails:
            errors.append(f"{e.get('post_url', '?')}: " + "; ".join(fails))
            continue
        url = e["post_url"].strip()
        if not e.get("id"):
            e["id"] = str(uuid.uuid4())[:8]
        e.setdefault("captured_at", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
        by_url[url] = e
    corpus["entries"] = sorted(by_url.values(), key=lambda x: x.get("captured_at", ""), reverse=True)
    corpus["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return corpus, errors


def index_by_id(corpus: dict) -> dict[str, dict]:
    return {e["id"]: e for e in (corpus.get("entries") or []) if e.get("id")}
