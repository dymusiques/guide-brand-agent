---
context_version: "2026-10-30-l012"
repo_path: "content/xiaohongshu/PIPELINE.md"
goal: "content/xiaohongshu/ 管线"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "41175a92b5ff93d7"
---

# content/xiaohongshu/ 管线

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** content/xiaohongshu/ 管线
- **Path:** `content/xiaohongshu/PIPELINE.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **在总顺序中的位置**: ```
- **Owner 数据叠加栈（写 Brief / 视频 / 标题前 · Must）**: **先读：** [docs/XHS-CONTENT-INTAKE-STACK.md](../../docs/XHS-CONTENT-INTAKE-STACK.md)（Excel 笔记数据 + PDF …
- **三阶段与状态（摘录 · 分阶段工作法）**: 本管线对齐 **采集 → 本地处理 → Owner 确认发布**（参考 [grapeot staged approach](https://github.com/grapeot/context-inf…
- **时间敏感表述（摘录 · temporal）**: Brief 或听见类内容若出现 **具体日期、档期、「最新/刚发布」、产品或模型版本号**，Agent **不得**仅凭记忆断言；应检索或标注待 Owner 确认（详见 [check.md](../.…
- **文件约定**: | 项 | 规则 |
- **单篇流程（必会）**: 1. 复制模板 → 填 Brief + **同步改 classifier JSON**
- **批量流程（交班 / 发版前）**: 扫描目录内所有 `*-brief.md`：
- **与 kernel 6 case 的分工**: | 命令 | 何时跑 |


---

## L2 正文

# content/xiaohongshu/ 管线

Git 真相源下的 **小红书选题 → Brief → Gemini 对齐 → 定稿 commit** 流程。Kernel / Skill 已就绪；本文件定义 **重复执行** 时的状态与命令。

## 在总顺序中的位置

```
Kernel (6 case) → Topic Manager Skill → 单篇 Brief 闭环 ✅
→ 【本管线】文档 + 批量 verify + 交班习惯
→ brand-visual（封面）→ 可选 Drive → P 层 KPI 复盘
```

## Owner 数据叠加栈（写 Brief / 视频 / 标题前 · Must）

**先读：** [docs/XHS-CONTENT-INTAKE-STACK.md](../../docs/XHS-CONTENT-INTAKE-STACK.md)（Excel 笔记数据 + PDF 研究 MD + IP + 认知期）。  
**交付：** [CONTENT-DELIVERY-FOR-OWNER.md](./CONTENT-DELIVERY-FOR-OWNER.md) — Agent 写稿 → **Owner 确认** → App 发布。  
**Brief 前红队（Owner 固定 · 2 条/篇）：** [BRIEF-REDTEAM-PRE.md](./BRIEF-REDTEAM-PRE.md) → `redteam/<slug>-pre.md`，**再**写 `*-brief.md`。  
**验收：** `bash scripts/verify-xhs-content-intake.sh`

## 三阶段与状态（摘录 · 分阶段工作法）

本管线对齐 **采集 → 本地处理 → Owner 确认发布**（参考 [grapeot staged approach](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/bestpractice_staged_approach.md)，本仓不装全文）。

| Stage | 本管线在做什么 | 对应状态 / 动作 |
|-------|----------------|-----------------|
| **1 · 采集** | 选题、调研、CSV/证据落盘 `content/`、`content/analytics/` inbox | 材料进 Git 或 Brief 引用；**不**代 Owner 在小红书发帖 |
| **2 · 本地处理** | 写/改 Brief + classifier JSON；跑 `evaluate` | `draft` → `verified`（`aligned: true`）；可重复改稿 + evaluate |
| **3 · 确认与发布** | Owner 审阅定稿、实际上线、填 `## 发布状态` | `verified` + **git commit** → **定稿**；封面 / Drive **仅 Owner 明确要求** |

**Dry Run（发布侧）：** Agent **不**代替 Owner 点击发布、不代发私信 mass、不 sync Drive，除非 Owner 当轮明确授权。批量改 Brief / 跑 verify 前确认路径：`content/xiaohongshu/*-brief.md` only。全仓破坏性检查清单见 [integration/IMPORTANT.md](../../integration/IMPORTANT.md#dry-run破坏性--发布侧--摘录)。

## 时间敏感表述（摘录 · temporal）

Brief 或听见类内容若出现 **具体日期、档期、「最新/刚发布」、产品或模型版本号**，Agent **不得**仅凭记忆断言；应检索或标注待 Owner 确认（详见 [check.md](../../check.md)）。

| 情况 | 做法 |
|------|------|
| 活动/演出/展览日期 | 核对官方来源或 Owner 提供的链接；写不进 Brief 则改模糊表述或留 `[待核实]` |
| 「最新专辑/政策/平台规则」 | Web 检索或 Owner 确认；避免 cutoff 幻觉 |
| 技术名（如 Gemini 模型 ID） | 以本仓脚本/env 实际使用的名为准；与 kernel evaluate 一致 |

听见 Daily / 强资讯验证见 [rules/skills/bestpractice_temporal_info_verification.md](../../rules/skills/bestpractice_temporal_info_verification.md)；认知期品牌 Brief **以上表 + 该 skill 边界为准**。

## 文件约定

| 项 | 规则 |
|----|------|
| **命名** | `YYYY-MM-DD-<slug>-brief.md` |
| **模板** | [kernels/templates/xhs-content-brief.template.md](../../kernels/templates/xhs-content-brief.template.md) |
| **Classifier** | 必须含 `<!-- xhs-classifier -->` + JSON 的 `subject` / `body` |
| **Verify log** | Brief 末尾记录每次 `evaluate` 结果（日期、版本、aligned、exit code） |

### 状态（人工标记，写在 Brief「与品牌」或 Verify log）

| 状态 | 含义 | 允许的动作 |
|------|------|------------|
| **draft** | 文案或未 evaluate | 可改 JSON；不可称定稿、不可 sync Drive |
| **verified** | `evaluate --brief` → `aligned: true` | 可 commit；仍非最终发布稿 |
| **定稿** | Owner 确认 + **已 git commit** | 可交 `brand-visual`；Owner 要求时可 sync Drive |

## 单篇流程（必会）

1. 复制模板 → 填 Brief + **同步改 classifier JSON**  
2. **交 Owner 前完整验收（Must）：**  
   `.venv/bin/python scripts/evaluate-xhs-brief-complete.py --brief content/xiaohongshu/<file>.md`  
   （redteam-pre + 本篇 L1×6 + Gemini evaluate + kernel 6 回归）  
3. 或仅改稿循环：`python scripts/evaluate-xhs-topic.py --brief …`  
4. **`aligned: true` + complete PASS** → 更新 Verify log → **git commit**  
4. 封面需求 → `.cursor/skills/brand-visual/`  
5. **仅** Owner 说「同步 Drive」→ `05-xiaohongshu/`（overlay folder ID）

正式路径用 **`--brief`**，不用裸 `--subject/--body` 代替定稿。

## 批量流程（交班 / 发版前）

扫描目录内所有 `*-brief.md`：

```bash
bash scripts/verify-xhs-content-dir.sh
```

- 每篇调用与单条相同的 `evaluate-xhs-topic.py --brief`  
- 任一篇 **未 aligned** 或 **API/格式错误** → 脚本 exit 1  
- 需要 `Guide/0/.env` 中 `GEMINI_API_KEY`（与 kernel 6 case 相同）

## 与 kernel 6 case 的分工

| 命令 | 何时跑 |
|------|--------|
| `bash scripts/verify-xhs-topic.sh` | 修改 `kernels/xiaohongshu/line2/` 或 classifier 规则后 |
| `bash scripts/verify-xhs-content-dir.sh` | 新增/改 Brief 后、交班前、发版前 |
| `python scripts/evaluate-xhs-topic.py --brief …` | 单篇改稿循环 |

## 交班清单（Agent）

1. `bash scripts/verify-handoff.sh`  
2. 若有 `content/xiaohongshu/*-brief.md`：`bash scripts/verify-xhs-content-dir.sh`  
3. 改过 kernel：`bash scripts/verify-xhs-topic.sh`  
4. （有 OAuth 时）`bash scripts/verify-integration.sh`  

## 红线（勿提前做）

- 不要把粉丝数 **5000/10k** 写进 classifier 单测  
- **未 aligned** 不要 sync Drive  
- **不要** 只写 Drive 不 commit Git  

## 相关链接

- Skill：[.cursor/skills/xiaohongshu/topic-manager.md](../../.cursor/skills/xiaohongshu/topic-manager.md)  
- Kernel：[kernels/xiaohongshu/README.md](../../kernels/xiaohongshu/README.md)  
- 路由：[integrations/index.md](../../integrations/index.md)  
- Meta（改脚本/集成）：[rules/skills/bestpractice_ai_programming_mindset.md](../../rules/skills/bestpractice_ai_programming_mindset.md)