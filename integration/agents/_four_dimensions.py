"""Shared manager test: four scores, each out of 100, pass at 80."""

from __future__ import annotations

from integration.agents._paths import ROOT

NEEDLES = ("角度满分 100", "爆款满分 100", "口吻满分 100", "引用满分 100", "过线 80")


def case_four_dimension_contract() -> tuple[bool, str]:
    doc = ROOT / "docs/PLATFORM-HIT-STANDARDS.md"
    script = ROOT / "scripts/evolve-platform-hits.py"
    if not doc.is_file() or not script.is_file():
        return False, "missing standards or scorer"
    text = doc.read_text(encoding="utf-8")
    code = script.read_text(encoding="utf-8")
    for needle in NEEDLES:
        if needle not in text:
            return False, f"standards missing {needle}"
    if "FOUR_PASS = 80" not in code or "HIT_BAR = 80" not in code:
        return False, "pass line drifted"
    if "score_voice" not in code or "score_citations" not in code:
        return False, "voice or citation scorer missing"
    if "压测" not in text:
        return False, "stress line missing"
    return True, "angle hit voice cite · 100/80"
