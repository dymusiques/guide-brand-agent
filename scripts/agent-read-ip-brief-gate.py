#!/usr/bin/env python3
"""Must read IP positioning brief in full (L2 body), not L1 header only."""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BRIEF = ROOT / "content/personal-ip/ip-positioning-brief-2026-10-05.md"
OUT = ROOT / "integration/handoff/owner-ip-brief-read-latest.json"
MIN_CHARS = 1500


def main() -> int:
    if not BRIEF.is_file():
        print("FAIL missing IP brief", file=sys.stderr)
        return 2
    text = BRIEF.read_text(encoding="utf-8")
    # L2 起算
    if "## L2 正文" in text:
        body = text.split("## L2 正文", 1)[1]
    else:
        body = text
    cjk = len([c for c in body if "\u4e00" <= c <= "\u9fff" or c.isascii()])
    sha = hashlib.sha256(text.encode()).hexdigest()[:16]
    ok = cjk >= MIN_CHARS
    payload = {
        "as_of": datetime.now(timezone.utc).isoformat(),
        "path": str(BRIEF.relative_to(ROOT)),
        "sha256_prefix": sha,
        "body_chars": cjk,
        "min_required": MIN_CHARS,
        "status": "PASS" if ok else "FAIL",
        "supervision": "禁止只读 L1 压缩顶栏当 IP 背书",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
