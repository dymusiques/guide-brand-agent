#!/usr/bin/env python3
"""周三/周日导表提醒 · 供 Cursor Automation 或本机 cron 调用。"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "integration/handoff/owner-xhs-export-reminder-latest.json"
TZ = ZoneInfo("Asia/Shanghai")

REMINDER_DOW = {2: "周三", 6: "周日"}  # Monday=0
MESSAGE = """\
【小红书数据导表提醒】
建议今晚导出「近7日」+ 笔记列表（或全量列表明细）→ 丢进 Drive「我的小红书数据」。
你当前节奏约每周 2–3 条：双次导表（周三+周日）够覆盖首波与长尾，不必每篇 24h 导一次。
导出后无需口令；次日 Drive 日检或复盘时 Agent 会自动 sync。
手册：docs/OWNER-MULTICHANNEL-POST-FLYWHEEL.md
"""


def main() -> int:
    now = datetime.now(TZ)
    dow = now.weekday()
    is_reminder_day = dow in REMINDER_DOW
    payload = {
        "schema": "owner_xhs_export_reminder_v1",
        "as_of": now.isoformat(),
        "timezone": "Asia/Shanghai",
        "is_reminder_day": is_reminder_day,
        "weekday_zh": REMINDER_DOW.get(dow),
        "schedule_zh": "每周三、周日 20:30 Automation 发本提醒",
        "message_zh": MESSAGE if is_reminder_day else "今日非固定导表提醒日（仍可在发帖后 48–72h 自愿导一次）",
        "drive_folder_handoff": "integration/handoff/owner-xhs-data-drive.json",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False))
    return 0 if is_reminder_day else 0


if __name__ == "__main__":
    raise SystemExit(main())