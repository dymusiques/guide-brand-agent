"""Schema validation for GM10 artist benchmark JSON (6-test L1 + 4-metric framework)."""

from __future__ import annotations

from benchmark_framework import METRIC_IDS, validate_benchmark_metrics

REQUIRED_TOP = (
    "artist_slug",
    "borrow_score",
    "why_evaluate",
    "alignment_points",
    "timeline",
    "benchmark_metrics",
)
TIMELINE_KEYS = ("phase", "year_or_era", "what_happened")


def validate_payload(data: dict) -> list[str]:
    errs: list[str] = []
    if not isinstance(data, dict):
        return ["root not object"]
    for k in REQUIRED_TOP:
        if k not in data:
            errs.append(f"missing {k}")
    score = data.get("borrow_score")
    if score is not None:
        if not isinstance(score, (int, float)) or not (0 <= float(score) <= 100):
            errs.append("borrow_score out of 0-100")
    ap = data.get("alignment_points")
    if ap is not None:
        if not isinstance(ap, list) or len(ap) < 3:
            errs.append("alignment_points need >=3")
    tl = data.get("timeline")
    if tl is not None:
        if not isinstance(tl, list) or len(tl) < 3:
            errs.append("timeline need >=3 events")
        else:
            for i, ev in enumerate(tl):
                if not isinstance(ev, dict):
                    errs.append(f"timeline[{i}] not object")
                    continue
                for tk in TIMELINE_KEYS:
                    if tk not in ev or not str(ev.get(tk, "")).strip():
                        errs.append(f"timeline[{i}] missing {tk}")
    why = data.get("why_evaluate")
    if why is not None and len(str(why).strip()) < 40:
        errs.append("why_evaluate too short")
    errs.extend(validate_benchmark_metrics(data.get("benchmark_metrics")))
    return errs
