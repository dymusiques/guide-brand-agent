#!/usr/bin/env python3
"""Write ceo-action-needed.md for Agent (no Owner prompt)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "content/evolution/00-manager/ceo-inbox"
OUT = INBOX / "ceo-action-needed.md"
EVO_04 = ROOT / "content/evolution/04-xhs-topic-manager"


def main() -> int:
    INBOX.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")
    reroutes: list[str] = []
    if EVO_04.is_dir():
        for p in sorted(EVO_04.glob("*/CEO-REROUTE.md")):
            reroutes.append(str(p.relative_to(ROOT)))
    queue = INBOX / "agent-work-queue.md"
    lines = [
        f"# CEO action needed · auto · {now}",
        "",
        "> Agent Must — do NOT ask Owner to evaluate. Read workflow-automation-manifest.json § agent_playbook.",
        "",
        "## Brief GM-loop (CEO-REROUTE)",
    ]
    if reroutes:
        lines.extend(f"- `{r}`" for r in reroutes)
        lines.append("")
        lines.append("```bash")
        lines.append("# per brief:")
        lines.append("bash scripts/manager-ceo-gate-one-round.sh --brief content/xiaohongshu/<slug>-brief.md")
        lines.append("```")
    else:
        lines.append("- (none under evolution/04-xhs-topic-manager)")
    lines.extend(["", "## Work queue", ""])
    if queue.is_file():
        lines.append(f"See `{queue.relative_to(ROOT)}`")
    else:
        lines.append("(missing — run background cycle or manager-autopilot)")
    lines.extend(["", "## Recover", "", "```bash", "bash scripts/ceo-auto-recover-blocked.sh", "```", ""])
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"ok": True, "out": str(OUT.relative_to(ROOT)), "reroutes": len(reroutes)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
