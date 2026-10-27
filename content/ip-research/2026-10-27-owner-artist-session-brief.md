# Owner Session Brief · Artist 对标与相关 IP 推荐 · 2026-10-27

> **用途：** 模拟「下次打开对话」— GM10 已收集项 + watchlist 队列 + 请你一次性裁决。  
> **自动链：** daily 09:00 → `run-daily-gm-trio` → `merge-artist-intel-catalog` · 会话内读 catalog（不每日 ping）。

---

## 一、后台现在能自动跑什么（交班后预期）

| 能力 | 是否自动（Launcher + setup 一次） |
|------|-----------------------------------|
| 验收链（goals、collector、rollups、dispatch） | ✅ daily cycle |
| GM10 Artist 分析（watchlist 轮换 1 人/天） | ✅ |
| GM11 IP challenge + redteam-pre 卫生 | ✅ |
| GM12 Owner daily brief 拼装 | ✅ |
| 10+11+12 L1 六 case（`verify-agent-fused`） | ✅ trio 末尾 |
| 05 Brief Gemini Gate | ⚠️ 仅 `GOAL_EVOLUTION_DEEP=1` 或你写 Brief 时 CEO Gate |
| 01–09 自动写 Brief / 全 matrix | ❌ 刻意不做 |
| 未 Gate 稿自动丢给你 | ❌ 刻意不做 |

**全域自动 = 验收 + 日更 trio + 队列提醒**；**写稿与 aligned 定稿**仍在你下任务 + Cursor CEO 链。

---

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

---

## 三、Watchlist · 与你相关、尚未跑完 GM10 的 8 位（队列）

维护：`content/ip-research/artist-watchlist.json` · **one_artist_per_day** 轮换。

| 优先级建议 | slug | 名称 | 门类 | 为何与你相关（Agent 初判） |
|------------|------|------|------|---------------------------|
| **P1** | drew-forde-thatviolakid | ThatViolaKid | 弦乐×社媒×品牌 | 古典+流行并列、Fortune500 共创仍保持演奏者 — **最接近 Owner 阶段+乐器 IP** |
| **P1** | grace-xhs-visual-ip | 画画的小福象 | 小红书视觉 IP | 粉丝量级接近 ~1700 阶段；AI+国风商业插画+自有文创线 |
| **P1** | tudou-man-aigc | 土豆人 | AIGC×奢侈品牌 | 对齐 **AI×艺术×跨行业 open** 叙事 |
| **P2** | erlich-illustrator | 儿力力 | 插画 IP×情绪 | 小红书情感共鸣+联名；学 **认知期名片** 勿绑单品类 |
| **P2** | hauser-cellist | HAUSER | 大提琴×短视频 | 学平台分轨与节点；**慎学 pure vanity** |
| **P3** | lang-lang-piano-ip | 郎朗 | 全球古典名人 | 只取「古典+可合作语言」勿照搬 celebrity |
| **P3** | fuzzy-hug-digital-ip | Fuzzy hug | 数字 IP×快消 | 学 campaign 结构，非人设对标 |
| **P3** | lincoln-center-digital | Lincoln Center | 机构号 | 只借鉴内容分层，**勿做成场馆号** |

---

## 四、请你本轮决策（复制回复即可）

1. **catalog 条目 `crossover-classical-creator`：** 适合 / 不适合？原因？  
2. **watchlist 优先级：** 是否同意 P1 先 **ThatViolaKid → 小福象 → 土豆人**？要调序请说。  
3. **是否指定一篇小红书 Brief：** 例如「借 ThatViolaKid 学古典×品牌共创，写法派长笛版认知期」— 指定后走 04→05→CEO Gate。

---

## 五、内部验收（本 session 已跑）

```bash
SKIP_GEMINI=1 bash scripts/verify-agent-fused.sh --agent all-daily --with-artifacts
```

定稿小红书 Brief 时另跑：`bash scripts/manager-ceo-owner-gate.sh --brief content/xiaohongshu/<file>.md`

---

_生成：00 Manager 会话模拟 · 对齐 `docs/OWNER-ARTIST-CATALOG-ON-OPEN.md`_
