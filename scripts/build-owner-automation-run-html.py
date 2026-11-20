#!/usr/bin/env python3
"""Render integration/handoff/owner-automation-html/<slug>-latest.json to HTML."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "integration/handoff/owner-automation-html"

STATUS_CLASS = {
    "PASS": "pass",
    "INFO": "info",
    "NEEDS_WORK": "warn",
}


def render(payload: dict) -> str:
    title = html.escape(str(payload.get("automation_title_zh") or payload.get("automation_slug") or "Automation"))
    slug = html.escape(str(payload.get("automation_slug") or ""))
    run_date = html.escape(str(payload.get("run_date") or ""))
    status = str(payload.get("status") or "")
    badge = STATUS_CLASS.get(status, "info")
    summary = html.escape(str(payload.get("summary_zh") or ""))
    md_path = html.escape(str(payload.get("md_path") or ""))
    version = html.escape(str(payload.get("version") or ""))

    rows = []
    for item in payload.get("items") or []:
        excerpt = html.escape(str(item.get("excerpt_zh") or ""))
        item_title = html.escape(str(item.get("title_zh") or ""))
        zone = html.escape(str(item.get("zone") or ""))
        source = html.escape(str(item.get("source_name") or ""))
        info_date = html.escape(str(item.get("info_date") or ""))
        url = str(item.get("url") or "")
        url_e = html.escape(url, quote=True)
        link = f'<a href="{url_e}">{url_e}</a>' if url else "—"
        rows.append(
            f"""<article class="panel">
<h2>{item_title}</h2>
<p><span class="badge">{zone}</span> <span class="badge">{info_date}</span></p>
<p>{excerpt}</p>
<p class="meta">来源：<code>{source}</code><br/>{link}</p>
</article>"""
        )
    body = "\n".join(rows) if rows else '<p class="hint">无 items</p>'

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{title} · {run_date}</title>
<style>
  :root {{ font-family: -apple-system, "PingFang SC", sans-serif; line-height: 1.65; }}
  body {{ max-width: 920px; margin: 0 auto; padding: 28px 20px 80px; background: #f4f2ef; color: #1a1a1a; }}
  h1 {{ font-size: 1.55rem; }}
  .badge {{ display: inline-block; background: #111; color: #fff; font-size: 0.72rem; padding: 4px 10px; border-radius: 999px; margin: 2px 4px 2px 0; }}
  .badge.pass {{ background: #0a7; }}
  .badge.info {{ background: #246; }}
  .badge.warn {{ background: #c60; }}
  .panel {{ background: #fff; border-radius: 12px; padding: 18px 20px; margin: 14px 0; box-shadow: 0 2px 10px rgba(0,0,0,.06); }}
  .hint {{ background: #fff8e6; border: 1px solid #e6c200; border-radius: 8px; padding: 12px 14px; font-size: 0.92rem; }}
  a {{ color: #0645ad; word-break: break-all; }}
  .meta {{ font-size: 0.88rem; color: #333; }}
  footer {{ margin-top: 2rem; font-size: 0.82rem; color: #555; }}
</style>
</head>
<body>
<h1>{title}</h1>
<p>
  <span class="badge {badge}">{html.escape(status or "—")}</span>
  <span class="badge">{run_date}</span>
  <span class="badge">{slug}</span>
</p>
<p class="hint">{summary}</p>
{body}
<footer>
<p>真源：<code>{md_path}</code> · version {version}</p>
</footer>
</body>
</html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    args = ap.parse_args()
    slug = args.slug.strip()
    if not slug or "/" in slug or slug.startswith("."):
        print("FAIL: bad --slug", file=sys.stderr)
        return 2
    src = OUT_DIR / f"{slug}-latest.json"
    if not src.is_file():
        print(f"FAIL: missing {src}", file=sys.stderr)
        return 2
    payload = json.loads(src.read_text(encoding="utf-8"))
    out = OUT_DIR / f"{slug}-latest.html"
    out.write_text(render(payload), encoding="utf-8")
    print(out.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
