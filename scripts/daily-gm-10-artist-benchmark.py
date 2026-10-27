#!/usr/bin/env python3
"""GM10 · Daily artist benchmark: baseline → Gemini → challenge stub → evaluator metrics."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "kernels" / "xiaohongshu"))
sys.path.insert(0, str(ROOT / "kernels" / "daily-gm"))

from artist_benchmark_schema import validate_payload  # noqa: E402
from benchmark_framework import composite_borrow_score, metrics_prompt_block  # noqa: E402
from config.gemini_config import get_api_key, get_model  # noqa: E402
from google import genai  # noqa: E402
from google.genai import types  # noqa: E402

WATCH = ROOT / "content/ip-research/artist-watchlist.json"
RUBRIC = ROOT / "content/evolution/_template/artist-benchmark-gold-rubric.md"
IP_BRIEF = ROOT / "content/personal-ip/ip-positioning-brief-2026-10-05.md"


def pick_artist(watch: dict) -> dict:
    artists = watch.get("artists") or []
    if not artists:
        raise SystemExit("artist-watchlist.json has no artists")
    day_index = date.today().toordinal()
    return artists[day_index % len(artists)]


def run_gemini(artist: dict, owner_ctx: str, rubric: str) -> dict:
    client = genai.Client(api_key=get_api_key())
    model = get_model()
    urls = artist.get("urls") or []
    queries = artist.get("search_queries") or []
    prompt = f"""You are GM10 Artist Benchmark for an arts-domain personal IP (any discipline within arts: music, visual, performance, etc.) × cross-industry brand (China Xiaohongshu context).
Owner baseline (excerpt):
{owner_ctx[:4000]}

Rubric:
{rubric[:2000]}

Artist to benchmark:
{json.dumps(artist, ensure_ascii=False)}

Public URLs (if any): {urls}
Search hints: {queries}

Return ONLY one JSON object with keys:
artist_slug, borrow_score (0-100, should align with weighted benchmark_metrics),
why_evaluate (>=2 sentences Chinese, cite DB/PLD/APO/CTD),
alignment_points (array >=3 strings Chinese),
timeline (array >=3 objects with phase, year_or_era, what_happened),
worth_borrowing (array bullets), avoid (array bullets),
sources_note (tier: say if inferred vs URL-backed; no fabricated deals),
benchmark_metrics (object, each metric: score 0-100 + rationale Chinese >=20 chars).

{metrics_prompt_block()}

Use public knowledge; if uncertain, lower scores and say in sources_note."""
    resp = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    text = (resp.text or "").strip()
    return json.loads(text)


def main() -> int:
    today = date.today().isoformat()
    watch = json.loads(WATCH.read_text(encoding="utf-8"))
    artist = pick_artist(watch)
    slug = artist.get("slug") or "artist"
    base = ROOT / "content/evolution/10-artist-intel" / today / slug
    base.mkdir(parents=True, exist_ok=True)
    (base / "intake").mkdir(exist_ok=True)
    (base / "reference").mkdir(exist_ok=True)
    (base / "versions").mkdir(exist_ok=True)

    rubric = RUBRIC.read_text(encoding="utf-8")
    owner = IP_BRIEF.read_text(encoding="utf-8") if IP_BRIEF.is_file() else ""
    (base / "reference/gold.md").write_text(rubric + "\n\n---\n\n" + owner[:1500], encoding="utf-8")
    (base / "intake/watchlist.json").write_text(json.dumps(artist, ensure_ascii=False, indent=2), encoding="utf-8")

    try:
        payload = run_gemini(artist, owner, rubric)
    except Exception as e:
        (base / "versions/v0-error.md").write_text(f"Gemini failed: {e}\n", encoding="utf-8")
        print(f"FAIL GM10 gemini: {e}")
        return 1

    bm = payload.get("benchmark_metrics")
    if isinstance(bm, dict):
        calc = composite_borrow_score(bm)
        if abs(calc - int(payload.get("borrow_score") or 0)) > 8:
            payload["borrow_score"] = calc
    errs = validate_payload(payload)
    v0 = base / "versions/v0-benchmark.json"
    v0.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    challenge = base / "challenge-log.md"
    challenge.write_text(
        f"# Challenge · GM10 · {today}\n\n"
        "- 攻击：是否 vanity 对标？→ 检查 borrow_score 与 alignment 是否含强链接\n"
        "- 攻击：timeline 是否编造？→ sources_note Must 标注推断\n\n"
        f"Schema errs: {errs or 'none'}\n",
        encoding="utf-8",
    )

    metrics = base / "metrics.jsonl"
    row = {
        "label": "v0",
        "borrow_score": payload.get("borrow_score"),
        "schema_ok": not errs,
        "schema_errs": errs,
    }
    with metrics.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

    report = base / "GM-REPORT.md"
    report.write_text(
        f"# GM-REPORT · 10 Artist Benchmark · {slug} · {today}\n\n"
        f"- borrow_score: {payload.get('borrow_score')}\n"
        f"- schema: {'PASS' if not errs else 'FAIL ' + str(errs)}\n"
        f"- v0: `{v0.relative_to(ROOT)}`\n",
        encoding="utf-8",
    )

    if errs:
        print("FAIL GM10 schema:", errs)
        return 1
    print("PASS GM10", slug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
