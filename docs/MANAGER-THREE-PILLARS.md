---
context_version: "2026-10-30-l012"
repo_path: "docs/MANAGER-THREE-PILLARS.md"
goal: "Manager 三支柱 · 每位 GM（01–12）真正在做什么"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "06313028308ec59d"
---

# Manager 三支柱 · 每位 GM（01–12）真正在做什么

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **签发：** 2026-10-27 · 00 Manager 代 CEO · **来源：** Owner 口述（重述每个 Manager 的本质工作）  
> **定位：** 这是 **主框架（primary framing）**。其余文档（五原则、五步环、auto-gate、verify 矩阵）都是它的**落地细节**，不与之冲突。  
> **读序
- **Path:** `docs/MANAGER-THREE-PILLARS.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **0. Owner 原话（三支柱）**: 每一位 Manager（GM 01–12；00 Manager 在 CEO 层同理）真正在做的是三件事：
- **2. 支柱 2 · 可衡量基准 → 本仓落点**: | 基准层 | 命令 / 产物 | 它是什么 dataset | 回答什么 |
- **4. 桥接：Owner 五步环 = 支柱 3 的**执行**（不矛盾）**: [Owner 五步图（顺时针，每条箭头 = Manager）](./MANAGER-EVAL-IMPROVEMENT-LOOP.md#2-五步顺时针与manager箭头) 是**支柱 3 在一个 ar…
- **6. 与五原则的对应（不替代，只是换一个切面）**: | Owner 五原则（[STANDARDS](./CEO-MANAGER-OPERATING-STANDARDS.md)） | 主要落在支柱 |
- **7. 诚实边界（本文**没有**做的事）**: - 未改任何脚本；未实施「REROUTE 增加 Prompt Change 提案节」「GM-REPORT 加每轮分析一行」「metrics 加 `prompt_rev`」——均为**建议，待 Owne…
- **8. 相关**: [MANAGER-EVAL-IMPROVEMENT-LOOP](./MANAGER-EVAL-IMPROVEMENT-LOOP.md) · [CEO-MANAGER-OPERATING-STANDAR…


---

## L2 正文

# Manager 三支柱 · 每位 GM（01–12）真正在做什么

> **签发：** 2026-10-27 · 00 Manager 代 CEO · **来源：** Owner 口述（重述每个 Manager 的本质工作）  
> **定位：** 这是 **主框架（primary framing）**。其余文档（五原则、五步环、auto-gate、verify 矩阵）都是它的**落地细节**，不与之冲突。  
> **读序：** 本文 → [MANAGER-EVAL-IMPROVEMENT-LOOP](./MANAGER-EVAL-IMPROVEMENT-LOOP.md)（五步环 = 支柱 3 的执行）→ [CEO-MANAGER-OPERATING-STANDARDS](./CEO-MANAGER-OPERATING-STANDARDS.md)（五原则）

## 0. Owner 原话（三支柱）

每一位 Manager（GM 01–12；00 Manager 在 CEO 层同理）真正在做的是三件事：

| # | 支柱 | Owner 一句话 |
|---|------|--------------|
| **1** | **可观察性（Observability）** | 让 AI **输出理由** → 系统变得**可观察**；为**自我批判**提供原始材料。 |
| **2** | **可衡量基准（Measurable Benchmark）** | 设计**有代表性的 dataset** → **稳定基准**；把「靠猜测的改进」变成**可衡量的工程问题**。 |
| **3** | **教练 → SOP 资产（Coach → SOP Asset）** | 教练式引导**沉淀为 SOP** → AI 处理改进工作的**行动手册**。 |

```text
        ┌──────────── 支柱 1 ────────────┐
        │ AI 不只给结论，还给「为什么」    │
        │ → 日志/理由落盘 → 可被审、可被批判 │
        └───────────────┬────────────────┘
                        ▼ 原始材料
        ┌──────────── 支柱 2 ────────────┐
        │ 代表性 dataset + 固定 case 集     │
        │ → 同一把尺子反复量 → 改进可比较   │
        └───────────────┬────────────────┘
                        ▼ 哪里差、差多少
        ┌──────────── 支柱 3 ────────────┐
        │ 教练式 REROUTE → 同类错第 2 次    │
        │ 固化进 SOP / Prompt / rule        │
        │ → 下一轮 AI 默认照做              │
        └───────────────┬────────────────┘
                        └──────► 回到支柱 1（新一轮输出继续带理由）
```

**对每个 GM 的一句话判断标准：** 做完一轮，我是否 ① 留下了「为什么」 ② 用同一把尺子量了 ③ 把学到的写进了下次会自动读的地方？三个都「是」才算在做 Manager 的事，而不是只在改稿。


## 2. 支柱 2 · 可衡量基准 → 本仓落点

> **原则：** 「我觉得更好了」不算。必须有**代表性 dataset + 固定 case**，用**同一把尺子**前后对比；没有数据就**明说「未验证」**。

| 基准层 | 命令 / 产物 | 它是什么 dataset | 回答什么 |
|--------|-------------|-------------------|----------|
| **L1 × 6 case（每篇 Brief）** | `evaluate-xhs-brief-complete.py` → JSON `l1_six_on_this_brief` | 6 类代表性判例：正例×2 / 负例 / 歧义×2 / 边界（见 JSON `kernel_ref`） | 这篇稿是否过 IP + 强链接 + 防标题党 + 非空 |
| **Kernel 6（回归）** | `bash scripts/verify-xhs-topic.sh`（05 Gemini 6 case；黑盒，集成层**不改**） | 固定 6 个判例，防 classifier 漂移 | 判定是否仍稳定（批量末步一次） |
| **verify-agent-fused 6-case 矩阵** | `bash scripts/verify-agent-fused.sh --agent NN [--with-artifacts]` · [VERIFY-AGENT-FUSED](./VERIFY-AGENT-FUSED.md) | A：00–09 matrix 6 glue；B：仅 04/05 挂 05 Gemini 6；C：10/11/12 本地 6 case（`kernels/daily-gm/tests/`：`test_artist_benchmark_6.py` / `test_ip_daily_eval_6.py` / `test_owner_daily_brief_6.py`）+ `kernels/daily-gm/shared_gold.py` / `shared_traps.py`（X1–X12） | 每岗各自的稳定基准 |
| **SEO / 卫生 lint** | `scripts/seo-lint-xhs-briefs.py` · `bash scripts/verify-xhs-content-dir.sh`（H1≤40 字等 6 项） | 小红书标题/结构规则集 | 06 批量是否合规 |
| **战略文档 lint + 评估** | `lint-strategic-doc.py` · `evaluate-business-brand.py` · `evaluate-marketing-campaign.py` | 02/03 的 SWOT / campaign 判例 | 商业/营销稿是否过线 |
| **编辑距离（有 gold）** | `evaluate-edit-distance.py` → `metrics.jsonl` → `evolution-metrics-summary.py` | Owner 确认的 `reference/gold.md` | 稿离 gold 越来越近吗（趋势，不是单点） |
| **目标注册表** | [GOALS-REGISTRY](../integration/GOALS-REGISTRY.md) · `integration/goals/registry.json` · `bash scripts/verify-goals.sh` | `G-STRONG-LINK` · `G-BRIEF-ALIGNED-GATE` · `G-ANALYTICS-EVIDENCE` 等 | 总目标钩子是否仍成立（**G-QUALITY-GROWTH 无自动断言**，靠 CSV/Owner） |
| **Analytics CSV（当有）** | `content/analytics/inbox/` → `bash scripts/analytics-pipeline.sh` → `content/analytics/derived/next-topics-*.md` | 真实平台数据 | 选题/标题改进依据；**无 CSV → 不得写阅读/转化结论** |
| **全仓 / 交班** | `verify-all.sh` · `verify-integration.sh`（6 case）· `verify-handoff.sh` · `manager-workflow-verify.sh` | 集成层固定检查 | 工具链与接手完整性 |

**「未验证」硬规则（红线）：** 当前 `content/analytics/inbox/` 无 CSV（仅 `.gitkeep` 与 `done/`）→ 阅读量/转化/涨粉相关结论一律标 **「未验证」**；`G-QUALITY-GROWTH`（1700→5000→10k）不进 classifier，不编造。

**GM 自检（支柱 2）：** 我引用的每个「变好了」，是否对应上表某条命令的**数字或 PASS/FAIL**？否 → 写「未验证」，别写形容词。

**诚实差距：** 01–03、07–09 部分岗位只有 matrix glue（结构检查），没有「对稿的分数环」；prompt 改动前后无 A/B 记录（`metrics.jsonl` 暂无 `prompt_rev` 字段）。详见 [EVAL-LOOP §4.2](./MANAGER-EVAL-IMPROVEMENT-LOOP.md)。


## 4. 桥接：Owner 五步环 = 支柱 3 的**执行**（不矛盾）

[Owner 五步图（顺时针，每条箭头 = Manager）](./MANAGER-EVAL-IMPROVEMENT-LOOP.md#2-五步顺时针与manager箭头) 是**支柱 3 在一个 artifact 上怎么转一圈**；三支柱是**为什么 / 凭什么 / 沉淀到哪**。

| 五步环 | 主要吃哪根支柱 | 说明 |
|--------|----------------|------|
| 1 **Manual Analysis** | **支柱 1** | 读 FAIL 项、challenge、redteam-pre、verify JSON 的「理由」，判断**为什么**差 |
| 2 **Propose Prompt Change** | **支柱 3** | 提出改 Brief / `INTEGRATION-PROMPT` / challenge 节 / SOP（**不改 kernel**，除非 05 专项）；同类第 2 次 = 必改 |
| 3 **Observe Score** | **支柱 2** | `RESULT: PASS/FAIL` · failures 数 · L1×6 · 编辑距离 · aligned |
| 4 **Re-run Evaluation** | **支柱 2** | 同一把尺子重跑（`manager-ceo-auto-gate-loop.sh` ≤3 轮） |
| 5 **Analyze Failures** | **支柱 1→3** | 剩余 FAIL 逐条归因（REROUTE）→ 回到 1；重复出现的沉淀进 SOP |
| **Manager 箭头** | **支柱 3** | 教练动作：派活、贴报错、重跑、禁止未 PASS 交 Owner |

```text
五步环（执行）：1 分析 → 2 提议改 prompt → 3 看分 → 4 重跑 → 5 归因 → 回 1
三支柱（框架）：  ①可观察   ③沉淀SOP        ②基准   ②基准   ①可观察→③沉淀
```

`AUTO-WORKFLOW.md` 里的 Manager's Loop 起点是 `Analyze Failures`，与图的起点 `Manual Analysis` 不同，但**同一个环**（见 EVAL-LOOP §2）。

> **第二张图（CEO / Senior Manager 环 · 箭头 AI · 起点 Consult SOP · 两轮串行迭代）：** [CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md](./CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md) · 落地 SOP [CEO-DOUBLE-ITERATION-SOP](../agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md)。CEO 的工作 = 可观察性 + 可衡量 + 知识 → 自愈系统，与三支柱同构。


## 6. 与五原则的对应（不替代，只是换一个切面）

| Owner 五原则（[STANDARDS](./CEO-MANAGER-OPERATING-STANDARDS.md)） | 主要落在支柱 |
|----------------------------------------------------------------|--------------|
| 1 清晰的委派 | 支柱 3（dispatch = SOP 资产）+ 支柱 2（每行有验收命令） |
| 2 有把握的评估 | 支柱 2 |
| 3 数据驱动改进 | 支柱 1 + 支柱 2 |
| 4 教练式引导促成长 | 支柱 3 |
| 5 洞见 → 持久团队资产 | 支柱 3 |

## 7. 诚实边界（本文**没有**做的事）

- 未改任何脚本；未实施「REROUTE 增加 Prompt Change 提案节」「GM-REPORT 加每轮分析一行」「metrics 加 `prompt_rev`」——均为**建议，待 Owner 点头**。
- 无 analytics CSV → 增长/转化类结论 **未验证**。
- 未 commit · 未 sync Drive · 未发帖。
- 单会话内 CEO 与 GM 由同一 Agent 顺序扮演，「Manager 箭头」在实现上仍是同一角色（见 EVAL-LOOP §6）。

## 8. 相关

[MANAGER-EVAL-IMPROVEMENT-LOOP](./MANAGER-EVAL-IMPROVEMENT-LOOP.md) · [CEO-MANAGER-OPERATING-STANDARDS](./CEO-MANAGER-OPERATING-STANDARDS.md) · [CEO-MANAGER-OPERATING-PRINCIPLES](./CEO-MANAGER-OPERATING-PRINCIPLES.md) · [BRIEF-AUTO-GATE-PIPELINE](./BRIEF-AUTO-GATE-PIPELINE.md) · [CEO-AUTO-QA-LOOP](./CEO-AUTO-QA-LOOP.md) · [VERIFY-AGENT-FUSED](./VERIFY-AGENT-FUSED.md) · [GOALS-REGISTRY](../integration/GOALS-REGISTRY.md) · [COLLECTOR-EVALUATOR](../agents/_shared/COLLECTOR-EVALUATOR.md) · [IMPORTANT](../integration/IMPORTANT.md)