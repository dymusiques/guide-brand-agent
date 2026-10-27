#!/usr/bin/env python3
"""Fetch note description text from Xiaohongshu explore URLs (requires logged-in browser).

Usage:
  python scripts/analytics/xhs_fetch_note_captions.py
  python scripts/analytics/xhs_fetch_note_captions.py --profile ~/.xhs-playwright-profile

First run: headful login in opened Chrome window, then re-run.
Updates content/xiaohongshu/voice-anchor-sources.json caption fields.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = ROOT / "content/xiaohongshu/voice-anchor-sources.json"
NOTE_ID_RE = re.compile(r"/explore/([a-f0-9]+)")


def extract_note_id(url: str) -> str:
    m = NOTE_ID_RE.search(url or "")
    return m.group(1) if m else ""


def first_80(text: str) -> str:
    t = re.sub(r"\s+", " ", (text or "").strip())
    return t[:80]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        default=str(Path.home() / ".xhs-playwright-profile"),
        help="Persistent Chrome profile (login once)",
    )
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()

    if not SOURCES.is_file():
        print(f"missing {SOURCES}; run xhs_build_voice_anchor.py first", file=sys.stderr)
        return 1

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("pip install playwright && playwright install chromium", file=sys.stderr)
        return 2

    data = json.loads(SOURCES.read_text(encoding="utf-8"))
    anchors = data.get("anchors") or []

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            args.profile,
            headless=args.headless,
            locale="zh-CN",
        )
        page = context.pages[0] if context.pages else context.new_page()
        for item in anchors:
            url = item.get("note_url") or ""
            nid = extract_note_id(url)
            if not nid:
                item["caption_status"] = "no_url"
                continue
            target = f"https://www.xiaohongshu.com/explore/{nid}"
            try:
                page.goto(target, wait_until="domcontentloaded", timeout=60000)
                page.wait_for_timeout(3000)
                body = page.inner_text("body")
                if "页面不见了" in body or "无法浏览" in body:
                    item["caption_status"] = "blocked_or_login"
                    continue
                # Heuristic: longest paragraph block in body text
                chunks = [c.strip() for c in body.split("\n") if len(c.strip()) > 20]
                desc = max(chunks, key=len) if chunks else body[:500]
                item["first_80_chars"] = first_80(desc)
                item["caption_status"] = "fetched"
                item["caption_source"] = "playwright_dom"
            except Exception as e:
                item["caption_status"] = f"error:{type(e).__name__}"
        context.close()

    data["anchors"] = anchors
    SOURCES.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"updated {SOURCES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
