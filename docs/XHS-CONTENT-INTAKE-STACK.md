# 小红书内容 · Owner 数据叠加栈（每次产出必读）

> **用途：** 00 Manager / 04 / 09 在产出 **任何** 文案、标题、视频脚本、选题思路前，**按序读完本栈**；再写稿 → `evaluate` → **交 Owner 确认**（不代发 App）。  
> **交付约定：** [CONTENT-DELIVERY-FOR-OWNER.md](../content/xiaohongshu/CONTENT-DELIVERY-FOR-OWNER.md)

> **命名消歧（易混）：** 本文件下文 **Layer 1 / 2 / 3** = **写稿前要读的数据与产出类型**（Excel · PDF · Brief）。  
> **不是** [EXTENSION-POINTS.md](../integration/EXTENSION-POINTS.md) / 生态图里的 **「Layer 3 · Vendor 工具箱」**（gdocs · writing · IP 13 技能等）。  
> **MANIFEST** 在本栈 = 唯一文件 [`DATA-MANIFEST.json`](../content/analytics/xiaohongshu/DATA-MANIFEST.json)（09 维护 · 0a/04 **读**）。

---

## 栈顶 · 一键顺序（Agent Must）

| # | 读什么 | 路径 |
|---|--------|------|
| 1 | **数据注册表**（23 篇 · Excel 已导入） | [DATA-MANIFEST.json](../content/analytics/xiaohongshu/DATA-MANIFEST.json) |
| 2 | **行级快照**（无 CSV 也能读数） | [notes-snapshot-2026-10-20.json](../content/analytics/xiaohongshu/notes-snapshot-2026-10-20.json) |
| 3 | **数据→选题策略** | [xhs-data-strategy-2026-10-20.md](../content/analytics/derived/xhs-data-strategy-2026-10-20.md) |
| 4 | **Pipeline 最新建议**（若存在） | `content/analytics/derived/next-topics-*.md` · `ceo-dispatch-latest.md` |
| 5 | **平台 PDF 研究（MD 摘录）** | [xhs-platform-research-index.md](../content/marketing/research/xhs-platform-research-index.md) |
| 6 | **04 一页约束** | [platform-notes-2026.md](../content/xiaohongshu/platform-notes-2026.md) |
| 7 | **认知期 program** | [2026-10-brand-discovery-phase.md](../content/marketing/2026-10-brand-discovery-phase.md) · [discovery-phase-signal-baseline.md](../content/marketing/discovery-phase-signal-baseline.md) |
| 8 | **IP 红线** | [rules/USER.md](../rules/USER.md) · [ip-positioning-brief-2026-10-05.md](../content/personal-ip/ip-positioning-brief-2026-10-05.md) |
| 9 | **视频迭代 + 声音** | [XHS-VIDEO-ITERATION.md](../content/xiaohongshu/XHS-VIDEO-ITERATION.md) · [VOICE-ANCHOR.md](../content/xiaohongshu/VOICE-ANCHOR.md) · [voice-anchor-sources.json](../content/xiaohongshu/voice-anchor-sources.json) |
| 10 | **CV 事实（Git）** | [cv-source-2026-09-15.md](../content/personal-ip/cv-source-2026-09-15.md) |

**原始 Excel（换机拷贝 · gitignore）：** 见 [XHS-DATA-LAYER.md](./XHS-DATA-LAYER.md) · `content/analytics/raw/xiaohongshu/`  
**原始 PDF（gitignore）：** `content/marketing/research/raw/*.pdf`

---

## Layer 1 · Owner 导出的笔记数据（Excel → 仓内）

| 资产 | 说明 |
|------|------|
| 列表总表 | `raw/.../notes-detail.xlsx` → 驱动 `notes.csv` / snapshot |
| 23 篇单篇明细 | `raw/.../note-details/*数据明细表.xlsx` → `detail-json/*.json` |
| 链接回填 | `note-links.csv` · `笔记链接回填表.xlsx` |
| 强链接定义 | 品牌向私信/聊聊；**约课 ≠ KPI**（signal-baseline） |

**写稿时怎么用数据：**

- 钩子结构优先 **故事 + 判断**（高曝光/互动帖），认知期 **不** 以纯教程为主轴。  
- 标题/首屏对照 **已验证帖**（snapshot 里 impressions/views/collects）。  
- **不编造** 未在 snapshot/CSV/MANIFEST 中的阅读、转化、私信数。

刷新数据（Owner 新导出 xlsx 后）：

```bash
python scripts/analytics/xhs_convert_notes_detail.py --xlsx content/analytics/raw/xiaohongshu/2026-10-20/notes-detail.xlsx
bash scripts/analytics-fetch.sh && bash scripts/analytics-pipeline.sh
```

---

## Layer 2 · Owner 提供的平台 PDF（已落盘 → MD）

| PDF（raw/） | Agent MD |
|-------------|----------|
| WILL 导读/原文 | [xhs-platform-2026-will-momentum.md](../content/marketing/research/xhs-platform-2026-will-momentum.md) |
| Momentum 2026 | [xhs-momentum-2026-agent-brief.md](../content/marketing/research/xhs-momentum-2026-agent-brief.md) |
| 10 大搜索趋势 | [xhs-search-trends-2024-agent-brief.md](../content/marketing/research/xhs-search-trends-2024-agent-brief.md) |
| 01/02 课件 | [xhs-foundation-slides-01-02.md](../content/marketing/research/xhs-foundation-slides-01-02.md) |
| 爆款黄金公式 | [xhs-content-structure-2025-notes.md](../content/marketing/research/xhs-content-structure-2025-notes.md) |

**叠加规则：** 平台风向 **校准** 钩子/搜索/语气；**不覆盖** Layer 1 对你账号的真实结论。

---

## Layer 3 · 产出类型（均须 Owner 确认后发布）

| 类型 | 默认落盘 | 说明 |
|------|----------|------|
| Brief + 成稿 | `content/xiaohongshu/*-brief.md` | 含 classifier · evaluate |
| 可粘贴正文队列 | `content/xiaohongshu/*-publish-ready-queue.md` | 标题/正文/标签/CTA |
| 视频脚本 | Brief 内 `## 视频脚本` 或 `content/xiaohongshu/video/` | 同栈约束 |
| 选题/标题清单 | `content/analytics/derived/` 或当轮 chat | 须引用数据依据 |

---

## 验收

```bash
bash scripts/verify-xhs-content-intake.sh
```

---

## 维护

- 新 Excel 批次 → 更新 `DATA-MANIFEST.json` · 新 `notes-snapshot-*.json` · 刷新 derived strategy。  
- 新 PDF → 放入 `research/raw/` + 补 MD + 更新 [research index](../content/marketing/research/xhs-platform-research-index.md)。
