#!/usr/bin/env python3
"""Send Owner Gmail when CEO XHS filter batch completes. Uses gdocs CLI if available."""

from __future__ import annotations

import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DELIVERABLE = ROOT / "content/evolution/00-manager/ceo-inbox"
TODAY = datetime.now().strftime("%Y-%m-%d")


def find_deliverable() -> Path | None:
    html = DELIVERABLE / f"OWNER-XHS-FILTER-DELIVERABLE-{TODAY}.html"
    if html.is_file():
        return html
    md = DELIVERABLE / f"OWNER-XHS-FILTER-DELIVERABLE-{TODAY}.md"
    return md if md.is_file() else None


def gmail_profile_email() -> str:
    venv_py = ROOT / ".venv/bin/python"
    proc = subprocess.run(
        [
            str(venv_py),
            "-m",
            "gdocs",
            "--secrets-dir",
            str(ROOT / "vendor/gdocs-skill/secrets"),
            "gmail",
            "profile",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        return ""
    import json

    try:
        return json.loads(proc.stdout).get("emailAddress", "") or ""
    except json.JSONDecodeError:
        return ""


def send_via_gdocs(to_email: str, subject: str, body: str) -> bool:
    venv_py = ROOT / ".venv/bin/python"
    if not venv_py.is_file():
        return False
    body_file = DELIVERABLE / "gmail-notify-body.txt"
    body_file.write_text(body, encoding="utf-8")
    proc = subprocess.run(
        [
            str(venv_py),
            "-m",
            "gdocs",
            "--secrets-dir",
            str(ROOT / "vendor/gdocs-skill/secrets"),
            "gmail",
            "send",
            "--to",
            to_email,
            "--subject",
            subject,
            "--body-file",
            str(body_file),
            "--body-format",
            "text",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return proc.returncode == 0


def main() -> int:
    path = find_deliverable()
    if not path:
        print("FAIL: no deliverable", file=sys.stderr)
        return 1
    rel = path.relative_to(ROOT)
    subject = f"[danying-brand-agent] 小红书资料筛选已完成 · {TODAY}"
    body = (
        f"CEO 派活链已跑完。请打开 Cursor 仓库查看：\n\n"
        f"  {rel}\n\n"
        f"Artist Excel：content/ip-research/artist-watchlist-four-metrics.xlsx\n\n"
        f"— 自动提醒 · {datetime.now().isoformat()}\n"
    )
    to = __import__("os").environ.get("OWNER_GMAIL", "").strip() or gmail_profile_email()
    if to and send_via_gdocs(to, subject, body):
        print("PASS gdocs gmail", to)
        return 0
    # Write marker for MCP send in autopilot
    marker = DELIVERABLE / "gmail-notify-pending.json"
    marker.write_text(
        __import__("json").dumps({"subject": subject, "body": body, "to_env": "OWNER_GMAIL or self"}, indent=2),
        encoding="utf-8",
    )
    print("WARN: gdocs send skipped; wrote", marker)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
