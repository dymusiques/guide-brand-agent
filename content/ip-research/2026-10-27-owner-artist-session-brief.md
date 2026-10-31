---
context_version: "2026-10-30-l012"
repo_path: "content/ip-research/2026-10-27-owner-artist-session-brief.md"
goal: "Owner Session Brief · Artist 对标与相关 IP 推荐 · 2026-10-27"
openwebui_route: "intake_l2"
cursor_route: "exec_gate"
content_sha256: "ff2f9e71d034a0b8"
---

# Owner Session Brief · Artist 对标与相关 IP 推荐 · 2026-10-27

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** Owner Session Brief · Artist 对标与相关 IP 推荐 · 2026-10-27
- **Path:** `content/ip-research/2026-10-27-owner-artist-session-brief.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `exec_gate`

## 章节锚点
- **二、Artist 对标 · 待你裁决（catalog · 四指标 DB/PLD/APO/CTD · 非 SWOT）**: 审阅后回复：**适合 / 不适合 + 一句原因**。Agent 写入 `artist-intel-review-state.json`。
- **四、请你本轮决策（复制回复即可）**: 1. **catalog 条目 `crossover-classical-creator`：** 适合 / 不适合？原因？


---

## L2 正文

# Owner Session Brief · Artist 对标与相关 IP 推荐 · 2026-10-27

> **用途：** 模拟「下次打开对话」— GM10 已收集项 + watchlist 队列 + 请你一次性裁决。  
> **自动链：** daily 09:00 → `run-daily-gm-trio` → `merge-artist-intel-catalog` · 会话内读 catalog（不每日 ping）。


## 二、Artist 对标 · 待你裁决（catalog · 四指标 DB/PLD/APO/CTD · 非 SWOT）

审阅后回复：**适合 / 不适合 + 一句原因**。Agent 写入 `artist-intel-review-state.json`。  
**全 watchlist 筛查表：** [artist-watchlist-screened.md](./artist-watchlist-screened.md) · SOP：[docs/SOP-ARTIST-BENCHMARK-AND-HANDOFF.md](../../docs/SOP-ARTIST-BENCHMARK-AND-HANDOFF.md)

| 日期 | slug | composite | DB/PLD/APO/CTD | 说明 |
|------|------|-----------|----------------|------|
| 2026-10-27 | crossover-classical-creator（占位） | 62 | 75/40/35/70 | **非真人** · 建议裁决 **不适合** 作对标 |
| — | **ThatViolaKid**（P1 · 未进 catalog 直至 GM10 跑日） | **73** | 95/63/68/60 | 见 screened 表 · **当前 P1 优先深读** |

**细节（值得借鉴 / 避开）：**

- **值得借鉴：** 听觉不可替代性→品牌空间体验；人即品牌框架；日更轻量+周更深度分层。  
- **避开：** 早期垂直行业露出致「单品类号」误判；vanity 流量；一次性营销不沉淀 IP 资产。  
- **时间线（模型）：** 2016–19 蓄力 → 2020–23 小红书+跨行业联名 → 2024– 一人公司+AI/数字资产。

**Agent 建议（待你拍板）：** 本条 **不宜当「真人对标」采纳**；可作 **结构 rubric 参考**。明天起 GM10 会按 watchlist 产出 **具名** 分析。


## 四、请你本轮决策（复制回复即可）

1. **catalog 条目 `crossover-classical-creator`：** 适合 / 不适合？原因？  
2. **watchlist 优先级：** 是否同意 P1 先 **ThatViolaKid → 小福象 → 土豆人**？要调序请说。  
3. **是否指定一篇小红书 Brief：** 例如「借 ThatViolaKid 学古典×品牌共创，写法派长笛版认知期」— 指定后走 04→05→CEO Gate。


_生成：00 Manager 会话模拟 · 对齐 `docs/OWNER-ARTIST-CATALOG-ON-OPEN.md`_