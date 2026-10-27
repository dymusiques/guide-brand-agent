"""Shared IP / adversarial gold paths for daily GM 10/11/12 and fused verify."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ADVERSARIAL_GOLD = (
    ROOT / "content/evolution/00-manager/ip-adversarial-drill-2026-10-27/reference/gold.md"
)
IP_BRIEF_FALLBACK = ROOT / "content/personal-ip/ip-positioning-brief-2026-10-05.md"


def resolve_ip_gold_path() -> Path:
    if ADVERSARIAL_GOLD.is_file():
        return ADVERSARIAL_GOLD
    return IP_BRIEF_FALLBACK


def resolve_ip_gold_text(max_chars: int | None = 2000) -> str:
    p = resolve_ip_gold_path()
    if not p.is_file():
        return ""
    text = p.read_text(encoding="utf-8")
    if max_chars is not None and len(text) > max_chars:
        return text[:max_chars]
    return text


def gold_min_length() -> int:
    return 80
