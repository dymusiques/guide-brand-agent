#!/usr/bin/env python3
"""Write CEO-RUN-MANIFEST-latest.json + .md for Owner chat delivery."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "content/evolution/00-manager/ceo-inbox"


def main() -> int:
    raw = os.environ.get("CEO_RUN_MANIFEST_JSON", "{}")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {}
    data.setdefault("generated_at", datetime.now(timezone.utc).isoformat())
    data.setdefault("doc", "docs/OWNER-CHAT-DELIVERY-FORMAT.md")
    day = datetime.now().strftime("%Y-%m-%d")
    html = INBOX / f"OWNER-XHS-FILTER-DELIVERABLE-{day}.html"
    data.setdefault(
        "owner_html_file",
        str(html.relative_to(ROOT)) if html.is_file() else f"content/evolution/00-manager/ceo-inbox/OWNER-XHS-FILTER-DELIVERABLE-{day}.html",
    )
    data["owner_html_uri"] = f"file://{html.resolve()}#owner-latest" if html.is_file() else ""

    INBOX.mkdir(parents=True, exist_ok=True)
    jpath = INBOX / "CEO-RUN-MANIFEST-latest.json"
    jpath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    par = data.get("parallelism") or {}
    lines = [
        "# CEO Run Manifest · latest",
        "",
        f"- generated: {data.get('generated_at')}",
        f"- overall: **{data.get('overall', '—')}**",
        "",
        "## 并行说明（Owner Must 读）",
        "",
        f"- all_agents_invoked: **{par.get('all_agents_invoked', '—')}**",
        f"- invoked: **{par.get('invoked_count', '—')}/{par.get('total_agents', 12)}**",
        f"- mode: `{par.get('mode', '—')}`",
        f"- {par.get('owner_answer', '')}",
        "",
        "## 01–12 Roster（全表）",
        "",
        "| ID | Agent | 状态 | 能力 | 结果 | 并行？ |",
        "|----|-------|------|------|------|--------|",
    ]
    for row in data.get("roster", []):
        caps = row.get("capabilities") or []
        cap_s = caps[0] if isinstance(caps, list) and caps else str(caps)
        lines.append(
            f"| {row.get('id')} | {row.get('name')} | {row.get('status')} | {cap_s} | "
            f"{row.get('result', '—')} | {row.get('parallel_with_others', False)} |"
        )
    lines.extend(
        [
            "",
            "## 本次执行的脚本步骤",
            "",
            "| Agent | Capability | Result |",
            "|-------|------------|--------|",
        ]
    )
    for row in data.get("agents", []):
        lines.append(f"| {row.get('agent', '—')} | {row.get('capability', '—')} | {row.get('result', '—')} |")
    lines.extend(["", "## Steps", ""])
    for i, s in enumerate(data.get("steps", []), 1):
        lines.append(f"{i}. {s}")
    lines.extend(
        [
            "",
            "## Owner HTML",
            "",
            f"- path: `{data.get('owner_html_file')}`",
            f"- uri: {data.get('owner_html_uri')}",
            "",
        ]
    )
    (INBOX / "CEO-RUN-MANIFEST-latest.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"WROTE {jpath.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
