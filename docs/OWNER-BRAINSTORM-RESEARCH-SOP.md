# Brainstorm 调研 SOP（Owner 拍板 · Agent 不偷升 advice）

## 原则

| 谁 | 做什么 |
|----|--------|
| **Owner** | **拍板**（投哪、定稿、就这条）— 没说前 Agent **不得**交付最终投流/标题定稿 |
| **Agent** | **brainstorm**：多方案、对比、引材料；调研 **全文** 读完再聊 |

**Owner 不必记口令**：谈小红书 / 待发 / Drive 背书 / 战略讨论时，Agent **自动**跑 `agent-brainstorm-preflight.py`（见 monorepo Rule `08`）。

## 三层材料（均禁止只读标题 / 表头 / preview）

1. **小红书后台** — `verify-xhs-analytics-freshness.py`；新 xlsx 自动 `xhs-owner-data-auto-sync.sh`
2. **待发字幕** — 全文 facts（`--intent brainstorm` 刷新，非拍板）
3. **Drive 背书** — **全库 catalog refresh + screen**（`screen-xhs-drive-corpus.py --refresh-catalog`），再打开入选 **原件全文**

## 自动执行（Agent Must · 无需 Owner 口令）

```bash
# Agent 在品牌仓根自动跑（参数用 Owner 当句原话）
python3 scripts/agent-brainstorm-preflight.py --goal "<chat 原话>"
```

- 命中：小红书数据 / pending / Drive / 战略 / 薯条讨论  
- **仅 Owner 说拍板** 时再跑：`agent-gate-pending-videos-advice.py --intent advice`

handoff：`integration/handoff/owner-brainstorm-preflight-latest.json`

### 深度链（已发复盘 / 监督 / 补全 — 自动 `--deep`）

Owner 原话含 **已发、后台、复盘、监督、补全、为什么、数据分析** 时：

```bash
python3 scripts/agent-brainstorm-preflight.py --deep --goal "<原话>"
# 或 monorepo：agent-workflow.py brand content-session --goal "<原话>"
```

依次：`catalog refresh`（gdocs venv）→ screen → **`agent-hydrate-drive-priority.py` 全文抽取**（PDF/docx/xlsx/pptx）→ `ceo-six-case-battery` → monorepo `prompt-six-case --domain xhs` → `run_ceo_full_execution` 切片 → `qc handoff`。

| handoff | 用途 |
|---------|------|
| `owner-brainstorm-deep-preflight-latest.json` | 各层 exit / 监督 |
| `owner-drive-hydrate-latest.json` | 每文件 `char_count` + `read_complete`（禁止只读文件名） |

---

## Owner 决策边界（战略 · 花钱 · 改库）

| 类型 | Agent | Owner |
|------|--------|--------|
| **战略材料**（Drive PDF/心法/投放逻辑） | 全库 listing refresh → screen → **读入选全文**；与 notes 数据、待发 facts 对照；给 2–3 方案 + 引用 | **定主线、定口径、定发不发表述** |
| **花钱**（薯条/聚光） | 实验设计、排序、引 Drive+后台规则；**不代下单** | **金额上限、点支付、拍板投哪条** |
| **改库 A**（补词 overlay、screen 产物） | 可做 | 可选扫一眼 |
| **改库 B**（新增 Drive 根、audit 链接入库） | 草案 + `--apply` 前说明 | **一句确认纳入** |
| **改库 C**（合并口径、删整库、改 DATA-MANIFEST 真源） | 只出 diff/影响 | **必须拍板** |

---

## Drive：全库 sync / Git / RAG / 换机（推荐）

| 需求 | 推荐（不要用错） |
|------|----------------|
| **日常 brainstorm** | **全库 catalog sync（live JSON）+ screen + 读入选全文** ✅；**不要**每次把 380 份 PDF 全 mirror 进 Git |
| **整库塞进 RAG** | ❌ 与 L1 裁定冲突；易偷懒只信 RAG 摘要。**T1 精选** 子集可 RAG |
| **换机 / 新 Agent 永久认识** | **Git：L1 + MANIFEST + handoff + 规则/脚本**；**intake：你认定的战略 PDF 少量 mirror**；**T2：其余按需 search** |
| **优于单选** | **组合**：L1（地图）+ 全库 listing（地址真源）+ screen（当次必读）+ 关键战略 **intake mirror**（换机不丢） |

战略 PDF **进 Git**：只进 **你已拍板「这是长期真源」** 的少量件（B→C）；其余 Drive 原件 + listing 即可。  
**进 RAG**：仅 **T1 精选文件夹**（短问 + Sources）；不是 380 全库。

## 拍板时（Owner 明示后）

```bash
python3 scripts/agent-gate-pending-videos-advice.py --intent advice
```

## 补词（classify · Agent 维护）

`propose-pending-goal-phrase.py --phrase "…" --bucket owner_decision --apply`

关联：`OWNER-PENDING-VIDEOS-EVAL-SOP.md` · `docs/agent/AGENT-BRAINSTORM-RESEARCH.json`
