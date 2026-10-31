---
context_version: "2026-10-30-l012"
repo_path: "agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md"
goal: "CEO 双轮串行迭代 SOP（「consult SOP.md」入口）"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "98d08f411e3ea80d"
---

# CEO 双轮串行迭代 SOP（「consult SOP.md」入口）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Owner 口令（例）：** 「consult SOP，对当前 prompt / Brief 跑 **两轮改进迭代**。」  
> **图与审计：** [docs/CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md](../../docs/CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md)  
>
- **Path:** `agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **0. 铁律**: 1. **串行：** 迭代 1 → **Analyze（落盘）** → 迭代 2。迭代 2 **只能**依据迭代 1 的分析改动。
- **1. Consult SOP · 必读栈（步骤 1）**: 按顺序读（**不复制内容，只引用**），并在 `ITERATION-LOG` 写一行「已读：…」：
- **2. 迭代模板（每次迭代 = 一圈图 2）**: ```text
- **3. Propose Prompt Change · 提案格式（补缺口 A/E）**: ```markdown
- **4. ITERATION-LOG 约定（phase 2 脚本强制）**: **命令：** `bash scripts/manager-ceo-double-iteration.sh --brief … --phase 1` → AI 填 log → `--phase 2`（…
- **迭代 1**: - 提案：（§3）
- **迭代 2**: - Consult：已读迭代 1 分析
- **对比**: | 指标 | 基线 | 迭代 1 | 迭代 2 |


---

## L2 正文

# CEO 双轮串行迭代 SOP（「consult SOP.md」入口）

> **Owner 口令（例）：** 「consult SOP，对当前 prompt / Brief 跑 **两轮改进迭代**。」  
> **图与审计：** [docs/CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md](../../docs/CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md)  
> **本文性质：** 纯文档 + 清单；**不改脚本**。把 Owner 第二张图（Consult SOP → Propose Prompt Change → Observe Score → Re-run Evaluation → Analyze Failures → 回 Consult SOP）落成 Agent 可照做的步骤。

## 0. 铁律

1. **串行：** 迭代 1 → **Analyze（落盘）** → 迭代 2。迭代 2 **只能**依据迭代 1 的分析改动。  
2. **不并行改同一 prompt：** 并行调研 / 其它目标（deep-delivery、campaign）属**额外**，不得冒充迭代 2。  
3. **每次迭代内只用 1 轮 gate：** `--max-rounds 1`，让 AI 在轮间介入（默认 3 轮脚本会连跑，轮间无人改稿 = 重跑而非迭代）。  
4. 不改 kernel（除非 05 专项）；不把 FAIL 稿交 Owner；无 CSV 的增长结论标「未验证」。

## 1. Consult SOP · 必读栈（步骤 1）

按顺序读（**不复制内容，只引用**），并在 `ITERATION-LOG` 写一行「已读：…」：

| # | 文件 | 为什么 |
|---|------|--------|
| 1 | [AUTO-WORKFLOW.md](AUTO-WORKFLOW.md) | 指挥链 · Manager's Loop |
| 2 | 对应 GM 的 `agents/<nn>-*/INTEGRATION-PROMPT.md`（Brief 类 = 04） | 要改的 prompt 本体 |
| 3 | [../_shared/BRIEF-ADVERSARIAL-CHALLENGE.md](../_shared/BRIEF-ADVERSARIAL-CHALLENGE.md) | challenge 节（Brief 类） |
| 4 | [../../docs/CEO-MANAGER-OPERATING-STANDARDS.md](../../docs/CEO-MANAGER-OPERATING-STANDARDS.md) §3–4 | 数据驱动 · 同类第 2 次必沉淀 |
| 5 | [../../docs/MANAGER-THREE-PILLARS.md](../../docs/MANAGER-THREE-PILLARS.md) | 观察 / 衡量 / 沉淀自检 |
| 6 | 上一轮 `content/evolution/<nn>-*/<slug>/CEO-REROUTE.md`（若有）· 最近 `verify-logs/<slug>-complete-*.json` | 已知失败与理由 |

## 2. 迭代模板（每次迭代 = 一圈图 2）

```text
[Consult SOP] → [Propose Prompt Change] → [Observe Score] → [Re-run Evaluation] → [Analyze Failures]
```

| 步 | 动作 | 命令 / 产物 |
|----|------|-------------|
| 1 Consult | §1 栈；若是迭代 2，**额外必读** 迭代 1 分析 | ITERATION-LOG 「Consult」行 |
| 2 Propose | 写 **提案**（见 §3 格式）再改：Brief / `INTEGRATION-PROMPT` / challenge 节 / SOP | 提案落 ITERATION-LOG；改动文件路径 |
| 3 Observe | 先记**基线分**（改前）再改后跑 | `bash scripts/manager-ceo-auto-gate-loop.sh --brief content/xiaohongshu/<file>-brief.md --max-rounds 1` |
| 4 Re-run | 同一把尺子重跑（需要时对比 JSON） | 同上；`content/xiaohongshu/verify-logs/<slug>-complete-<ts>.json` |
| 5 Analyze | **无论 PASS/FAIL 都写**：哪项变好/变差 · 为什么 · 下一轮改什么 | ITERATION-LOG 「迭代 n 分析」 |

> 非 Brief 目标（02/03/10/11/12 等）：把第 3–4 步命令换成 [MANAGER-EVAL §3.1](../../docs/MANAGER-EVAL-IMPROVEMENT-LOOP.md) 里对应岗的 evaluate / `verify-agent-fused.sh --agent NN`。

## 3. Propose Prompt Change · 提案格式（补缺口 A/E）

```markdown
### 提案（迭代 n）
- 改什么：<文件路径 + 段落>
- 一句 diff：<例：challenge 节加「必须引用 1 个外部类似命题」>
- 依据（来自哪条 FAIL / 日志）：<verify-logs 路径 / REROUTE 行>
- 预期哪条 gate 变绿：<L1-x / aligned / adversarial schema …>
- 风险：<可能让哪条变差>
```

## 4. ITERATION-LOG 约定（phase 2 脚本强制）

**命令：** `bash scripts/manager-ceo-double-iteration.sh --brief … --phase 1` → AI 填 log → `--phase 2`（`verify-ceo-iteration-log.py` 校验）。

落盘位置（任选其一，**须入 git 才算交付**）：

- Brief 类：`content/evolution/04-xhs-topic-manager/<slug>/ITERATION-LOG.md`
- CEO 层 / 跨 GM：`content/evolution/00-manager/ceo-inbox/ITERATION-LOG-<YYYY-MM-DD>-<tag>.md`

```markdown
# ITERATION-LOG · <target> · <date>
- Owner 口令：
- 已读 SOP：（§1 列表）
- 基线分：<命令 + RESULT + failures + 关键 JSON 路径>

## 迭代 1
- 提案：（§3）
- 改后分：
- 分析（Analyze）：<变好/变差 · 原因 · 未解决项>
- 迭代 2 将只改：<来自分析的 1–3 条>

## 迭代 2
- Consult：已读迭代 1 分析
- 提案：（§3，须引用迭代 1 分析条目）
- 改后分：
- 分析：

## 对比
| 指标 | 基线 | 迭代 1 | 迭代 2 |
|------|------|--------|--------|
| RESULT | | | |
| failures / L1×6 | | | |
| aligned | | | |

## 沉淀（同类第 2 次必填）
- 固化到：<INTEGRATION-PROMPT / challenge / SOP 路径> · 一句 diff · 预期 gate
## 未做
- 未 commit / 未 sync Drive / 未发帖 / 数据未验证 …
```

## 5. 与现有脚本的关系（谁做哪一步）

| 步 | 脚本能做 | 必须 AI 做 |
|----|----------|------------|
| Observe / Re-run | ✅ `manager-ceo-auto-gate-loop.sh --max-rounds 1` | — |
| 机械 Analyze | ✅ `ceo-auto-fix-brief.py`（FAIL 时写 REROUTE） | 写**语义**分析（含 PASS 轮）|
| Propose Prompt Change | ❌ | ✅ 全部 |
| Consult SOP | ❌ | ✅ 全部 |
| 进程自愈 | ✅ `ceo-auto-recover-blocked.sh` | — |

**别用的做法（会假装迭代）：** 直接 `manager-ceo-auto-gate-loop.sh`（默认 3 轮）当「三次迭代」· `CEO_DEEP_ROUNDS=2` 当「两轮迭代」。后者是 **两遍复验**（见 CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP §5.2）。

## 6. 与 deep-delivery / campaign 的组合（extras）

| 目标 | 做法 |
|------|------|
| **截止交付 / 深筛** | 先按本 SOP 对**关键 Brief** 跑双迭代；再 `bash scripts/run-ceo-deep-delivery-cycle.sh` 做**复验 + Phase A/B/G 收集与交付**（其 2 轮 = 复验，不算迭代）|
| **01–12 全员 campaign** | 与 deep 并行时 lock / `SKIP_GEMINI`；各 GM 自己的 prompt 改进仍按本 SOP **串行**|
| **阻塞 / 中断** | **自动** `bash scripts/ceo-auto-recover-blocked.sh`，勿问 Owner |

**已实施（2026-10-28）：** `manager-ceo-double-iteration.sh` + `verify-ceo-iteration-log.py`；REROUTE/GM-REPORT 模板与 `ceo-auto-fix-brief.py` 含提案节与分析行。

## 7. 检查清单（交 Owner 前自检）

- [ ] 已 Consult §1 栈并在 ITERATION-LOG 记录  
- [ ] 基线分已记录（改前）  
- [ ] 迭代 1：提案 → 改 → `--max-rounds 1` 看分 → **分析已落盘**  
- [ ] 迭代 2：Consult 含迭代 1 分析；提案引用其条目；**未并行**  
- [ ] 对比表有数字/路径（无数据写「未验证」）  
- [ ] 同类 FAIL 第 2 次 → 已固化 SOP/prompt，并入 `rules/WORKSPACE.md`  
- [ ] 交 Owner 前：`bash scripts/manager-ceo-owner-gate.sh --brief …` PASS  
- [ ] Manager 派活记录含：**Owner Gate PASS/FAIL · 打回轮次 n/3 · 交 Owner：是/否**  
- [ ] 新增资产已 `bash scripts/verify-handoff.sh`