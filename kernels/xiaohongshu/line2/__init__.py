"""Core classifier for Xiaohongshu topic / brief alignment."""

from .is_xhs_growth_aligned import (
    evaluate_xhs_growth_content,
    is_xhs_growth_aligned,
    normalize_xhs_content,
)

__all__ = [
    "evaluate_xhs_growth_content",
    "is_xhs_growth_aligned",
    "normalize_xhs_content",
]
