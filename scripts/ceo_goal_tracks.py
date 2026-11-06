"""CEO dual-track goal detection · FluteBuddy product vs personal IP ecosystem."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IP_TRACK = ROOT / "integration/handoff/owner-ip-track.json"
PRODUCT_NAMES = ["flutebuddy", "flute buddy", "flute practice buddy"]


def _load_ip_triggers() -> list[str]:
    if not IP_TRACK.is_file():
        return []
    data = json.loads(IP_TRACK.read_text(encoding="utf-8"))
    return [t.casefold() for t in (data.get("goal_triggers") or [])]


def is_flutebuddy_goal(goal: str) -> bool:
    g = goal.casefold()
    return any(n in g for n in PRODUCT_NAMES) or ("长笛" in goal and ("app" in g or "软件" in goal or "练习" in goal and "ip" not in g))


def is_ip_ecosystem_goal(goal: str) -> bool:
    g = goal.casefold().replace(" ", "")
    triggers = _load_ip_triggers()
    if any(t.replace(" ", "") in g for t in triggers):
        return True
    if "personalip" in g or "ip生态链" in g or "ip生态" in g:
        return True
    return False


def primary_track(goal: str) -> str:
    """product | personal_ip | mixed | general"""
    fb = is_flutebuddy_goal(goal)
    ip = is_ip_ecosystem_goal(goal)
    if fb and ip:
        return "mixed"
    if fb:
        return "product"
    if ip:
        return "personal_ip"
    return "general"
