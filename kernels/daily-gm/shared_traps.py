"""X1–X12 trap ids · shared by GM11 challenge + Brief redteam-pre."""

from __future__ import annotations

# Canonical index: content/personal-ip/2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md §2
TRAP_CATALOG: dict[str, str] = {
    "X1": "单品类绑定 / 垂类锁号",
    "X2": "履历堆叠无 moment",
    "X3": "硬广转化无认知",
    "X4": "vanity 流量无 DM",
    "X5": "AI 腔 / 无具体场景",
    "X6": "弱 CTA / 无强链接",
    "X7": "跨行业 open 口号但案例单一",
    "X8": "教育线抢戏压过 IP 主线",
    "X9": "数据好看但品牌 DM 不增",
    "X10": "对标抄袭无 Owner 语境",
    "X11": "法派专业被娱乐化稀释",
    "X12": "多平台不同人设撕裂",
}

# GM11 daily: pick 2 (rotate by weekday elsewhere if needed)
DAILY_GM11_TRAP_IDS = ("X9", "X2")


def daily_challenge_lines() -> list[str]:
    return [f"{tid}: {TRAP_CATALOG[tid]}" for tid in DAILY_GM11_TRAP_IDS if tid in TRAP_CATALOG]
