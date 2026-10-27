"""Structure / hygiene validation for GM12 Owner daily brief (6-test L1)."""

from __future__ import annotations

REQUIRED_HEADINGS = (
    "# Owner Daily Brief",
    "## Artist",
    "## IP 自检",
    "## 今日派活",
    "## 请你",
)
FORBIDDEN_OWNER_VERIFY = ("bash scripts/verify", "verify-agent-matrix", "manager-workflow-verify")


def validate_brief_markdown(text: str) -> list[str]:
    errs: list[str] = []
    if not text.strip():
        return ["empty brief"]
    for h in REQUIRED_HEADINGS:
        if h not in text:
            errs.append(f"missing heading: {h}")
    if "- [ ]" not in text:
        errs.append("missing Owner decision checkbox '- [ ]'")
    owner_zone = text.split("## 请你", 1)[-1]
    for bad in FORBIDDEN_OWNER_VERIFY:
        if bad in owner_zone:
            errs.append(f"Owner section must not push verify commands: {bad}")
    if len(text) > 12000:
        errs.append("brief too long (>12000 chars)")
    return errs


def validate_brief_gold(text: str) -> list[str]:
    need = ("artist", "gm11", "dispatch", "decision")
    low = text.lower()
    missing = [k for k in need if k not in low]
    if missing:
        return [f"gold rubric missing tokens: {', '.join(missing)}"]
    return []
