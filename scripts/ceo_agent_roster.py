"""01–12 agent roster defaults for CEO run manifest."""

from __future__ import annotations

from typing import Any

# id, display name, default capability hint
AGENT_CATALOG: list[tuple[str, str, str]] = [
    ("00", "CEO / 00-manager", "recover · dispatch · manifest · HTML gate"),
    ("01", "01-personal-ip", "evaluate_personal_ip · verify-agent-fused 01"),
    ("02", "02-business-brand", "evaluate-business-brand · fused 02"),
    ("03", "03-marketing-strategy", "evaluate-marketing-campaign · fused 03"),
    ("04", "04-xhs-topic-manager", "pitfalls · longform · gate · GM-REPORT"),
    ("05", "05-xhs-kernel", "verify-xhs-topic · verify-agent-fused 05"),
    ("06", "06-xhs-content-pipeline", "verify-xhs-content-dir"),
    ("07", "07-brand-visual", "brand-visual / Canva"),
    ("08", "08-platform-integration", "verify-integration · gdocs"),
    ("09", "09-data-analytics", "analytics-pipeline · next-topics"),
    ("10", "10-artist-benchmark", "verify-agent-fused 10"),
    ("11", "11-ip-daily-evaluator", "verify-agent-fused 11"),
    ("12", "12-owner-daily-brief", "verify-agent-fused 12"),
]

# Standard single-brief XHS full execution (not full campaign)
DEFAULT_INVOKED = {"00", "01", "04", "05", "08"}


def build_roster(
    invoked_ids: set[str] | None = None,
    capability_overrides: dict[str, list[str]] | None = None,
    result_overrides: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    invoked = invoked_ids if invoked_ids is not None else set(DEFAULT_INVOKED)
    caps = capability_overrides or {}
    results = result_overrides or {}
    out: list[dict[str, Any]] = []
    for aid, name, hint in AGENT_CATALOG:
        if aid in invoked:
            status = "invoked"
            parallel = False
        else:
            status = "skipped"
            parallel = False
        out.append(
            {
                "id": aid,
                "name": name,
                "status": status,
                "capabilities": caps.get(aid, [hint]),
                "parallel_with_others": parallel,
                "result": results.get(aid, "—" if status == "skipped" else "see steps"),
            }
        )
    return out


def parallelism_summary(roster: list[dict[str, Any]]) -> dict[str, Any]:
    invoked = [r for r in roster if r["status"] == "invoked"]
    return {
        "all_agents_invoked": len(invoked) == len(AGENT_CATALOG),
        "invoked_count": len(invoked),
        "total_agents": len(AGENT_CATALOG),
        "mode": "sequential_ceo_gm_chain",
        "owner_answer": (
            "不是全员并行；也不是 12 Agent 全调用。"
            f" 本次 invoked {len(invoked)}/{len(AGENT_CATALOG)}，主链串行（见 CEO-AGENT-ROSTER-AND-PARALLELISM.md）。"
        ),
    }
