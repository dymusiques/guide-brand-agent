#!/usr/bin/env python3
"""List Owner「我的小红书数据」Drive folder → drive-listing-latest.json."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HANDOFF = ROOT / "integration/handoff/owner-xhs-data-drive.json"
OUT_DIR = ROOT / "content/personal-ip/intake/_raw/owner-xhs-data"
OUT_FILE = OUT_DIR / "drive-listing-latest.json"
SECRETS = ROOT / "vendor/gdocs-skill/secrets"


def main() -> int:
    cfg = json.loads(HANDOFF.read_text(encoding="utf-8"))
    folder_id = cfg["drive_folder_id"]

    sys.path.insert(0, str(ROOT / "vendor/gdocs-skill"))
    from gdocs.drive_client import DriveClient

    client = DriveClient(SECRETS)
    files = []
    for item in client.children(folder_id):
        fid = item.get("id") or ""
        files.append(
            {
                "id": fid,
                "name": item.get("name") or "",
                "mimeType": item.get("mimeType") or "",
                "size": str(item.get("size") or ""),
                "modifiedTime": item.get("modifiedTime") or "",
                "webViewLink": item.get("webViewLink")
                or f"https://drive.google.com/file/d/{fid}/view?usp=drivesdk",
            }
        )

    payload = {
        "as_of": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "drive_folder_id": folder_id,
        "drive_link": cfg.get("drive_link"),
        "file_count": len(files),
        "files": sorted(files, key=lambda x: x.get("name") or ""),
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_FILE} ({len(files)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
