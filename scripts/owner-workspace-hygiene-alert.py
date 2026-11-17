#!/usr/bin/env python3
"""Print hygiene alerts (stdout JSON + human lines). Hook: weekly · post-CEO · agent plan."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEDULE = ROOT / "integration/handoff/owner-workspace-hygiene-schedule.json"
INBOX = ROOT / "content/evolution/00-manager/ceo-inbox"
ANALYTICS_XHS = ROOT / "content/analytics/xiaohongshu"


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    return (r.stdout or "").strip()


def days_since_last_archive() -> int | None:
    line = git("log", "-1", "--format=%ci", "--grep=Archive", "HEAD")
    if not line:
        line = git("log", "-1", "--format=%ci", "HEAD")
    if not line:
        return None
    try:
        dt = datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        delta = (now - dt).total_seconds() // 86400
        return max(0, int(delta))
    except ValueError:
        return None


def untracked_count() -> int:
    out = git("status", "--short")
    return sum(1 for ln in out.splitlines() if ln.startswith("??"))


def main() -> int:
    alerts: list[dict] = []
    days = days_since_last_archive()
    untr = untracked_count()
    deep = list(INBOX.glob("ceo-deep-delivery-*.md"))
    xlsx = list(ANALYTICS_XHS.glob("*.xlsx")) if ANALYTICS_XHS.is_dir() else []
    undated_owner_html = [
        p
        for p in INBOX.glob("OWNER-*-20*.html")
        if "-latest" not in p.name and p.is_file()
    ]

    if days is not None and days >= 7:
        alerts.append(
            {
                "id": "hygiene_weekly",
                "severity": "info",
                "message_zh": f"距上次 Git 提交已 {days} 天：建议跑归档/保洁（restore 滚动层 · 清 latest handoff）",
            }
        )
    if untr >= 20:
        alerts.append(
            {
                "id": "hygiene_untracked",
                "severity": "warn",
                "message_zh": f"未跟踪文件 {untr} 个：检查表 C（xlsx / deep-delivery / platform-hits）",
            }
        )
    if len(deep) >= 8:
        alerts.append(
            {
                "id": "layer_c_batch_monthly",
                "severity": "info",
                "message_zh": f"ceo-deep-delivery 日志 {len(deep)} 个：可删本地或写入 .gitignore",
            }
        )
    if xlsx:
        alerts.append(
            {
                "id": "xlsx_after_xhs_sync",
                "severity": "warn",
                "message_zh": f"发现 {len(xlsx)} 个 xlsx：走 Drive 同步，不要 commit",
            }
        )

    # Uncommitted dated deliverables (exist on disk but not in last commit tree — heuristic)
    stale = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "content/evolution/00-manager/ceo-inbox/OWNER-*-20*.html"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    extra_html = [ln for ln in (stale.stdout or "").splitlines() if ln and "-latest" not in ln]
    if extra_html:
        alerts.append(
            {
                "id": "archive_after_campaign",
                "severity": "warn",
                "message_zh": f"有 {len(extra_html)} 个 dated Owner HTML 未进 Git：战役结束请「定稿」后 archive commit",
                "paths_sample": extra_html[:5],
            }
        )

    payload = {
        "schema": "owner_workspace_hygiene_alert_v1",
        "as_of": datetime.now(timezone.utc).isoformat(),
        "untracked_count": untr,
        "days_since_last_commit": days,
        "alerts": alerts,
        "schedule": str(SCHEDULE.relative_to(ROOT)),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    for a in alerts:
        tag = a["severity"].upper()
        print(f"[{tag}] {a['id']}: {a['message_zh']}", file=sys.stderr)
    return 0 if not any(a["severity"] == "warn" for a in alerts) else 1


if __name__ == "__main__":
    raise SystemExit(main())