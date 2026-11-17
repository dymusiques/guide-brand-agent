"""Owner hard phrases · 派活给 CEO full stack."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
TRIGGERS = ROOT / "integration/handoff/owner-owner-triggers.json"


def _load() -> dict:
    if not TRIGGERS.is_file():
        return {}
    return json.loads(TRIGGERS.read_text(encoding="utf-8"))


def ceo_full_stack_goal(goal: str) -> bool:
    g = (goal or "").strip()
    if not g:
        return False
    data = _load()
    phrases = data.get("ceo_full_stack", {}).get("phrases_any") or []
    return any(p in g for p in phrases)