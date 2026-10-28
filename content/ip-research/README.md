# IP 研究 · Artist 对标 watchlist

- **维护者：** Agent（GM10）· Owner 不必手填  
- **配置：** [artist-watchlist.json](./artist-watchlist.json) · 筛查 [artist-watchlist-screened.md](./artist-watchlist-screened.md) · **全员详表** [2026-10-27-watchlist-four-metrics-full.md](./2026-10-27-watchlist-four-metrics-full.md)
- **四指标（替代 SWOT）：** [docs/BENCHMARK-FRAMEWORK-ARTIST.md](../../docs/BENCHMARK-FRAMEWORK-ARTIST.md) · `python scripts/screen-artist-watchlist.py`  
- **日更脚本：** `python scripts/daily-gm-10-artist-benchmark.py`  
- **产出：** `content/daily-brief/<date>-owner-daily-brief.md` § Artist 对标

## 范围

**艺术门类**内创作者/IP 均可（音乐、视觉、戏剧、舞蹈、装置、数字艺术等）— **不限定**某一细分专业。

## 换人或加人（Owner Must · 2026-10-27）

**凡会话/调研/intake 里出现、与 Owner IP 可对标的 artist/IP，Agent 必须写入 `artist-watchlist.json`（含 `urls`），并随认知更新 `notes`。** Owner 裁决见 `artist-intel-review-state.json`；catalog 见 `artist-intel-catalog.json`。

Agent 更新本 JSON 后 **无需 Owner 重启**；下一轮 GM10 自动轮换。  
大规模改 **daily 频率/成本** 先问 Owner（见 `BACKGROUND-CYCLE-INTERVAL-TRIGGER.md`）。

## 优先级 P1 / P2 / P3（Agent 建议档 · 非 JSON 字段）

| 档 | 含义 | GM10 怎么用 |
|----|------|-------------|
| **P1** | 与 Owner **阶段/渠道/目标最接近**，优先轮换、优先写 Brief 候选 | 默认先跑完 P1 再 P2 |
| **P2** | **可借鉴但有明显 caveat**（vanity、单品类风险等） | 分析里必须写 `avoid` |
| **P3** | **参照尺度**（名人/机构/纯 campaign IP），只取结构不取人设 | 借鉴分通常保守 |

Owner 可改序；改序后 Agent 同步 JSON 可选字段 `priority_tier`: `"P1"|"P2"|"P3"`。
