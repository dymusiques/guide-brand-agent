"""Schema / hygiene validation for GM11 daily IP eval (6-test L1)."""

from __future__ import annotations

import re

EVAL_KEYS = ("date", "rollup_present", "briefs_missing_redteam_pre", "challenge_pass")
TRAP_LINE = re.compile(r"^-\s+X\d+:", re.MULTILINE)


def validate_eval_doc(data: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(data, dict):
        return ["root not object"]
    for k in EVAL_KEYS:
        if k not in data:
            errs.append(f"missing {k}")
    miss = data.get("briefs_missing_redteam_pre")
    if miss is not None and not isinstance(miss, list):
        errs.append("briefs_missing_redteam_pre not list")
    if data.get("challenge_pass") is not None and not isinstance(data["challenge_pass"], bool):
        errs.append("challenge_pass not bool")
    if data.get("rollup_present") is not True:
        errs.append("rollup_present should be true for pass artifact")
    return errs


def validate_challenge_log(text: str) -> list[str]:
    errs: list[str] = []
    if not text.strip():
        return ["empty challenge-log"]
    traps = TRAP_LINE.findall(text)
    if len(traps) < 2:
        errs.append("need >=2 lines matching '- Xn:' trap format")
    return errs


def validate_gold_reference(text: str, min_len: int = 80) -> list[str]:
    if len(text.strip()) < min_len:
        return [f"gold reference shorter than {min_len} chars"]
    return []
