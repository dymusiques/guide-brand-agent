#!/usr/bin/env python3
"""Cross-dimension benchmark: refresh artist-watchlist-screened + full MD read audit."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "integration/handoff/owner-benchmark-cross-dim-latest.json"
MD = ROOT / "content/ip-research/artist-watchlist-screened.md"
JSON_PATH = ROOT / "content/ip-research/artist-watchlist-screened.json"
MIN_MD_CHARS = 500


def main() -> int:
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts/screen-artist-watchlist.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    md_text = MD.read_text(encoding="utf-8") if MD.is_file() else ""
    data = json.loads(JSON_PATH.read_text(encoding="utf-8")) if JSON_PATH.is_file() else {}
    urls = []
    for a in (data.get("artists") or [])[:5]:
        urls.extend(a.get("urls") or [])
    payload = {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "screen_exit_code": r.returncode,
        "md_chars": len(md_text),
        "md_path": str(MD.relative_to(ROOT)) if MD.is_file() else None,
        "top_urls_for_deep_read": urls[:8],
        "artist_count": len(data.get("artists") or []),
        "status": "PASS" if r.returncode == 0 and len(md_text) >= MIN_MD_CHARS else "FAIL",
        "supervision": "PLD/APO 须读 screened.md 全文；URL 深读由 Agent/MCP 或 GM 日更",
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
