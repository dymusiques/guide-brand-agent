#!/usr/bin/env python3
"""Learning 2 deliverable: function shell + docstring (rules live in docstring)."""


def is_xhs_growth_aligned(content: dict) -> bool:
    """
    Classify whether a Xiaohongshu note aligns with IP, growth, and strong-link goals.

    Input: dict with ``subject`` and ``body``. Implementation: line2/is_xhs_growth_aligned.py.

    Classification rules (Gemini answers yes when ALL apply):

    - Personal IP: French-school flute × brand strategy; AI innovation; 数字藏品.
    - Audience: brands (any industry), artists, education (students/parents),
      AI/digital-collectible innovators. Not a 家居/建材-focused account;
      富森美 case only as brief historical example, not default topic angle.
    - Strong link: consultation, collaboration, DM — not empty virality.
    - Growth: ~1700 → 5000 → 10000 quality followers.

    Answer no for unrelated content, clickbait without body value, or title/body conflict
    (judge primarily by body).

    Args:
        content: ``{"subject": str, "body": str}``

    Returns:
        bool

    Raises:
        ValueError: If Gemini response is not yes or no.
    """
    pass
