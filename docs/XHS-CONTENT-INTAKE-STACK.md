---
context_version: "2026-10-30-l012"
repo_path: "docs/XHS-CONTENT-INTAKE-STACK.md"
goal: "小红书内容 · Owner 数据叠加栈（每次产出必读）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "029d840a98a2db25"
---

# 小红书内容 · Owner 数据叠加栈（每次产出必读）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **用途：** 00 Manager / 04 / 09 在产出 **任何** 文案、标题、视频脚本、选题思路前，**按序读完本栈**；再写稿 → `evaluate` → **交 Owner 确认**（不代发 App）。  
> **交付约定：** [CONTENT-DELIVERY-FOR-OWNER.md](../content/xiaohongs
- **Path:** `docs/XHS-CONTENT-INTAKE-STACK.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **Layer 1 · Owner 导出的笔记数据（Excel → 仓内）**: | 资产 | 说明 |
- **Layer 3 · 产出类型（均须 Owner 确认后发布）**: | 类型 | 默认落盘 | 说明 |
- **维护**: - 新 Excel 批次 → 更新 `DATA-MANIFEST.json` · 新 `notes-snapshot-*.json` · 刷新 derived strategy。


---

## L2 正文

# 小红书内容 · Owner 数据叠加栈（每次产出必读）

> **用途：** 00 Manager / 04 / 09 在产出 **任何** 文案、标题、视频脚本、选题思路前，**按序读完本栈**；再写稿 → `evaluate` → **交 Owner 确认**（不代发 App）。  
> **交付约定：** [CONTENT-DELIVERY-FOR-OWNER.md](../content/xiaohongshu/CONTENT-DELIVERY-FOR-OWNER.md)

> **命名消歧（易混）：** 本文件下文 **Layer 1 / 2 / 3** = **写稿前要读的数据与产出类型**（Excel · PDF · Brief）。  
> **不是** [EXTENSION-POINTS.md](../integration/EXTENSION-POINTS.md) / 生态图里的 **「Layer 3 · Vendor 工具箱」**（gdocs · writing · IP 13 技能等）。  
> **MANIFEST** 在本栈 = 唯一文件 [`DATA-MANIFEST.json`](../content/analytics/xiaohongshu/DATA-MANIFEST.json)（09 维护 · 0a/04 **读**）。


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


## Layer 3 · 产出类型（均须 Owner 确认后发布）

| 类型 | 默认落盘 | 说明 |
|------|----------|------|
| Brief + 成稿 | `content/xiaohongshu/*-brief.md` | 含 classifier · evaluate |
| 可粘贴正文队列 | `content/xiaohongshu/*-publish-ready-queue.md` | 标题/正文/标签/CTA |
| 视频脚本 | Brief 内 `## 视频脚本` 或 `content/xiaohongshu/video/` | 同栈约束 |
| 选题/标题清单 | `content/analytics/derived/` 或当轮 chat | 须引用数据依据 |


## 维护

- 新 Excel 批次 → 更新 `DATA-MANIFEST.json` · 新 `notes-snapshot-*.json` · 刷新 derived strategy。  
- 新 PDF → 放入 `research/raw/` + 补 MD + 更新 [research index](../content/marketing/research/xhs-platform-research-index.md)。