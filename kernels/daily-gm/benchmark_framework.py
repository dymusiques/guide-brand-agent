"""GM10 · Directional Benchmarking framework (replaces SWOT for artist screening).

Metrics (0–100 each):
- directional_benchmarking (DB)
- pixel_level_deconstruction (PLD)
- audience_persona_overlap (APO)
- core_topic_density (CTD)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

METRIC_IDS = (
    "directional_benchmarking",
    "pixel_level_deconstruction",
    "audience_persona_overlap",
    "core_topic_density",
)

METRIC_LABELS = {
    "directional_benchmarking": "Directional Benchmarking (DB)",
    "pixel_level_deconstruction": "Pixel-Level Deconstruction (PLD)",
    "audience_persona_overlap": "Audience Persona Overlap (APO)",
    "core_topic_density": "Core Topic Density (CTD)",
}

# Owner direction axes (ip-positioning-brief-2026-10-05)
OWNER_DIRECTION = {
    "pillars": (
        "艺术专业高度（法派长笛/听见Daily）",
        "跨界品牌策划（跨行业open·不绑单品类）",
        "AI创新×数字藏品",
    ),
    "audience": ("品牌方", "艺术家", "教育链", "AI/数字藏品从业者"),
    "kpi": "强链接/DM·非vanity",
    "stage": "小红书认知期 ~1700→5000",
    "platform_primary": "xiaohongshu",
}

BORROW_WEIGHTS = {
    "directional_benchmarking": 0.30,
    "pixel_level_deconstruction": 0.25,
    "audience_persona_overlap": 0.25,
    "core_topic_density": 0.20,
}


@dataclass
class MetricScore:
    score: float
    rationale: str

    def as_dict(self) -> dict[str, Any]:
        return {"score": round(float(self.score), 1), "rationale": self.rationale}


def composite_borrow_score(metrics: dict[str, dict[str, Any]]) -> int:
    total = 0.0
    for mid, w in BORROW_WEIGHTS.items():
        block = metrics.get(mid) or {}
        total += w * float(block.get("score", 0))
    return int(round(max(0, min(100, total))))


def validate_benchmark_metrics(metrics: Any) -> list[str]:
    errs: list[str] = []
    if not isinstance(metrics, dict):
        return ["benchmark_metrics not object"]
    for mid in METRIC_IDS:
        block = metrics.get(mid)
        if not isinstance(block, dict):
            errs.append(f"missing benchmark_metrics.{mid}")
            continue
        sc = block.get("score")
        if sc is None or not isinstance(sc, (int, float)) or not (0 <= float(sc) <= 100):
            errs.append(f"{mid}.score out of 0-100")
        rat = block.get("rationale")
        if not rat or len(str(rat).strip()) < 20:
            errs.append(f"{mid}.rationale too short")
    return errs


def metrics_prompt_block() -> str:
    lines = ["Return benchmark_metrics object with each key having score (0-100) and rationale (Chinese >=1 sentence):"]
    for mid in METRIC_IDS:
        lines.append(f"- {mid}: {METRIC_LABELS[mid]}")
    lines.append(
        "DB=战略方向是否与 Owner（法派×跨界×强链接×不绑单品类×AI可选）同向; "
        "PLD=封面/钩子/栏目/CTA/日周更结构是否可像素级拆解迁移; "
        "APO=受众是否与 Owner（品牌/艺术/教育/AI）重叠且非纯vanity; "
        "CTD=核心题是否集中在专业+跨界+叙事而非垂直锁号."
    )
    return "\n".join(lines)


def _clamp(n: float, lo: float = 0, hi: float = 100) -> float:
    return max(lo, min(hi, n))


def screen_artist_heuristic(artist: dict[str, Any]) -> dict[str, MetricScore]:
    """Rule-based screen for watchlist (no Gemini). Agent/Gemini refines on daily GM10."""
    slug = artist.get("slug") or ""
    domain = (artist.get("domain") or "").lower()
    notes = (artist.get("notes") or "").lower()
    urls = artist.get("urls") or []

    db = 50.0
    pld = 50.0
    apo = 50.0
    ctd = 50.0
    db_r = pld_r = apo_r = ctd_r = ""

    if "thatviolakid" in slug or "forde" in slug:
        db += 12
        pld += 8
        apo += 8
        ctd += 10
        db_r = "弦乐×品牌共创且保持演奏者，与法派×跨界强链接高度同向。"

    # Directional
    if any(k in domain for k in ("品牌", "跨界", "aigc", "ip")):
        db += 18
        db_r = "领域含品牌/IP/跨界或AIGC，与 Owner 策划向同向。"
    if any(k in domain for k in ("音乐", "演奏", "古典", "长笛", "弦乐", "大提琴", "钢琴")):
        db += 15
        db_r = (db_r or "") + "艺术专业表演向，与法派专业锚点同向。"
    if "机构" in domain or "lincoln" in slug:
        db -= 25
        db_r = "机构传播非个人 IP 方向，与「人即品牌」错位。"
    if "数字角色" in domain or "fuzzy" in slug:
        db -= 10
        db_r = "非真人 IP，方向仅 campaign 结构可参考。"

    # PLD
    if "小红书" in domain or "xiaohongshu" in str(urls).lower():
        pld += 22
        pld_r = "小红书可观测，利于像素级拆封面/标签/栏目。"
    if "shorts" in notes or "短视频" in domain:
        pld += 8
        pld_r = (pld_r or "") + "短视频分轨可拆节点模板。"
    if "lang" in slug or "lincoln" in slug:
        pld -= 15
        pld_r = "名人/机构尺度，像素模板难直接迁移到 Owner 阶段。"

    # APO
    if "小红书" in domain or "grace" in slug:
        apo += 20
        apo_r = "受众阶段接近 Owner 小红书认知期。"
    if "vanity" in notes or "hauser" in slug:
        apo -= 12
        apo_r = "偏 C 端 fame，与强链接 B 端重叠有限，需筛 vanity。"
    if "品牌" in domain or "奢侈" in domain or "fortune" in notes.lower():
        apo += 10
        apo_r = (apo_r or "") + "品牌/商业受众与 Owner B 端重叠。"
    if "教育" in notes or "lang" in slug:
        apo += 8
        apo_r = (apo_r or "") + "教育链叙事有重叠。"

    # CTD
    if "单一 ip" in notes or "儿力力" in slug or "白日梦" in artist.get("name", ""):
        ctd += 18
        ctd_r = "单一 IP 形象，核心题密度高。"
    if "单品类" in notes or "勿绑" in notes:
        ctd += 5
        ctd_r = (ctd_r or "") + "已提示勿绑单品类，题密度策略可对齐。"
    if "campaign" in notes or "fuzzy" in slug:
        ctd -= 15
        ctd_r = "偏单次 campaign，核心题易稀释。"
    if "机构" in domain:
        ctd -= 20
        ctd_r = "机构多栏目并行，非个人核心题密度模型。"

    if len(urls) >= 2:
        pld += 5
    elif not urls:
        pld -= 10
        db -= 5

    return {
        "directional_benchmarking": MetricScore(_clamp(db), db_r or "方向需 GM10 Gemini 复核。"),
        "pixel_level_deconstruction": MetricScore(_clamp(pld), pld_r or "拆解度待 URL 深读。"),
        "audience_persona_overlap": MetricScore(_clamp(apo), apo_r or "受众重叠待复核。"),
        "core_topic_density": MetricScore(_clamp(ctd), ctd_r or "题密度待复核。"),
    }


def metrics_to_dict(scores: dict[str, MetricScore]) -> dict[str, dict[str, Any]]:
    return {k: v.as_dict() for k, v in scores.items()}


def tier_from_composite(composite: int) -> str:
    if composite >= 72:
        return "P1"
    if composite >= 58:
        return "P2"
    return "P3"
