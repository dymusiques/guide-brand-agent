#!/usr/bin/env python3
"""Collector: append Owner-fed material under content/evolution/ and update manifest."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVO = ROOT / "content" / "evolution"


def _slug(s: str) -> str:
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s.strip()).strip("-")[:80]


def main() -> int:
    p = argparse.ArgumentParser(description="Collector intake for evolution pipeline")
    p.add_argument("--agent", required=True, help="e.g. 04-xhs, 00-manager, 01-personal-ip")
    p.add_argument("--slug", required=True, help="artifact slug, e.g. pivot-E")
    p.add_argument("--file", type=Path, help="file to copy into intake/")
    p.add_argument("--text", help="inline text body")
    p.add_argument("--stdin", action="store_true", help="read body from stdin")
    p.add_argument("--note", default="", help="optional note in manifest")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    body: str | None = None
    if args.file:
        body = args.file.read_text(encoding="utf-8")
        source = str(args.file)
    elif args.text is not None:
        body = args.text
        source = "--text"
    elif args.stdin:
        body = sys.stdin.read()
        source = "stdin"
    else:
        p.error("one of --file, --text, or --stdin required")

    agent = _slug(args.agent)
    slug = _slug(args.slug)
    base = EVO / agent / slug
    intake_dir = base / "intake"
    manifest_path = base / "manifest.json"

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    intake_id = f"{ts}-{_slug(source)[-20:] or 'inline'}"
    dest = intake_dir / f"{intake_id}.md"

    header = f"<!-- collector-intake id={intake_id} source={source} -->\n\n"
    payload = header + body.strip() + "\n"

    if args.dry_run:
        print(f"would write: {dest}")
        print(f"manifest: {manifest_path}")
        return 0

    intake_dir.mkdir(parents=True, exist_ok=True)
    dest.write_text(payload, encoding="utf-8")

    manifest: dict = {"agent": agent, "slug": slug, "intakes": [], "versions": []}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    manifest.setdefault("intakes", []).append(
        {
            "id": intake_id,
            "path": str(dest.relative_to(ROOT)),
            "at": ts,
            "note": args.note,
            "source": source,
        }
    )
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(dest.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
