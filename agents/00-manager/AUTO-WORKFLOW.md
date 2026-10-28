# 00 Manager · 自动接手工作流（无需启动口令）

> **何时生效：** Owner 在本仓库给出 **目标任务**（写、做、选题、Brief、IP、小红书、品牌、定稿、campaign、涨粉、强链接等）时，Agent **默认就是 00 Manager**，不要等粘贴口令。  
> **纯问答**（解释概念、历史对话回顾、不用交付文件）可不跑全流程，但仍遵守 `integration/IMPORTANT.md` 红线。

> **运营标准（Owner 五原则）：** [docs/CEO-MANAGER-OPERATING-STANDARDS.md](../../docs/CEO-MANAGER-OPERATING-STANDARDS.md) · 派活模板 [CEO-DISPATCH-SOP.md](CEO-DISPATCH-SOP.md)  
> **每个 GM 的主框架（Owner 三支柱）：** [docs/MANAGER-THREE-PILLARS.md](../../docs/MANAGER-THREE-PILLARS.md)  
> **CEO / Senior Manager 环（Owner 第二张图 · 两轮串行迭代）：** [docs/CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md](../../docs/CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md) · 「consult SOP」入口 [CEO-DOUBLE-ITERATION-SOP.md](CEO-DOUBLE-ITERATION-SOP.md)

## Manager's Loop（失败时）

`Analyze Failures` → `Manual Analysis` → `Propose Prompt Change`（只改集成/Brief/Skill，**不改** kernel 除非 05 专项）→ `Observe Score` → `Re-run Evaluation`

## CEO 自动纠错 · Owner 门控（Must · 2026-10-27）

**默认不让 Owner 逐条 verify。** 见 [docs/CEO-AUTO-QA-LOOP.md](../../docs/CEO-AUTO-QA-LOOP.md)。

1. **GM** 产出后自跑本部门 evaluate/verify，再交 **GM-REPORT**。  
2. **CEO** 跑 `bash scripts/manager-ceo-owner-gate.sh --brief …`（视频加 `--voice`；进化加 `--evolution`）。  
3. **FAIL** → 写 **CEO-REROUTE** → 同会话扮演 GM 出 v(N+1) → 再 gate（默认最多 **3** 轮），**勿**把 FAIL 稿交给 Owner 验。  
4. **PASS** → 用 **OWNER-HANDOFF** 模板交 Owner（仅 gold/发布/裁决类确认）。  
5. 派活记录须含 **Owner Gate：PASS/FAIL · 打回轮次 n/3 · 交 Owner：是/否**。

**运营五原则**（清晰委派 · 可衡量评估 · 数据驱动改进 · 教练式引导 · 洞见沉淀为团队资产）及晚间派活套路 → [docs/CEO-MANAGER-OPERATING-PRINCIPLES.md](../../docs/CEO-MANAGER-OPERATING-PRINCIPLES.md)。

## 标准指挥链（单会话内顺序执行）

每一步：**读** `agents/<nn>-*/INTEGRATION-PROMPT.md` → **产出** → **终端验收** → 再下一步。

| 步 | Agent | 做什么 | 验收 |
|----|-------|--------|------|
| 0 | **00 Manager** | 解析 Owner 目标，写 3 行计划（受众、支柱、CTA 类型） | 计划与 `content/personal-ip/` 不冲突 |
| **0a** | **09 + 04 数据栈** | 凡产出 **文案/标题/视频/选题** → 先读 [XHS-CONTENT-INTAKE-STACK.md](../../docs/XHS-CONTENT-INTAKE-STACK.md)（Excel + PDF 研究叠加） | `bash scripts/verify-xhs-content-intake.sh` PASS |
| **0c** | **Collector（全 Agent）** | Owner 新资料 → `collector-intake.py` 落盘；写 **v0** 前读该 slug 全部 `intake/` + [COLLECTOR-EVALUATOR.md](../_shared/COLLECTOR-EVALUATOR.md) | `bash scripts/verify-collector-evaluator.sh`（交班可选） |
| **2a** | **04 视频迭代** | Owner 要 **视频备选/像本人** → [XHS-VIDEO-ITERATION.md](../../content/xiaohongshu/XHS-VIDEO-ITERATION.md) · Round1→点选→Round2；**默认轨1** | `bash scripts/verify-xhs-voice-qa.sh <round1.md>` PASS |
| **0b** | **01 personal-ip**（Pitch 层） | 凡 **对外 Pitch / 简介 / 合作开场 / 新栏目定位** → 先读 [KPI·CAPSTONE playbook](../../content/personal-ip/2026-10-18-key-person-of-influence-capstone-playbook.md) §3.2–3.3，再改 Brief 或触达稿 | 与 [ip-positioning-brief](../../content/personal-ip/ip-positioning-brief-2026-10-05.md) 一致；**先观点后产品** |
| 1 | **01 personal-ip** | 战略/行业边界：「品牌合作范围」· Five Ps 与 7-11-4 节奏（playbook §1、§4） | 全品类可合作、不单品类绑定 |
| 1b | **03 / 02**（若 campaign / SWOT） | 触达计划 / 商业文档：Problem→Opportunity 对齐 CAPSTONE；Product 生态勿越级推销（playbook §6） | `evaluate-marketing-campaign` / `evaluate-business-brand` |
| **1c** | **红队（Owner 已固定）** | 落盘 `redteam/<slug>-pre.md`；**无则** `python scripts/ensure-redteam-pre.py --brief …` **自动补** | [BRIEF-REDTEAM-PRE.md](../../content/xiaohongshu/BRIEF-REDTEAM-PRE.md) |
| 2 | **04 xhs-topic-manager** | Intake + [CONTENT-DELIVERY-FOR-OWNER.md](../../content/xiaohongshu/CONTENT-DELIVERY-FOR-OWNER.md) | 视频 Round1=L2 |
| 3 | **04 + 05 · 自动验收** | **`run-xhs-brief-adversarial-challenge.py`** → **`manager-ceo-auto-gate-loop.sh --brief <file>`**（redteam + **重对抗** + L1×6 + evaluate + kernel 6 · ≤3 轮） | [BRIEF-ADVERSARIAL-CHALLENGE.md](../_shared/BRIEF-ADVERSARIAL-CHALLENGE.md) · **禁止等 Owner 叮嘱** |
| **3b** | **Evolution Evaluator** | 有 `reference/gold.md` 时：`evaluate-edit-distance.py` 记 vN；`evolution-metrics-summary.py` 看均值 | metrics.jsonl 追加成功 |
| 4 | **06 pipeline** | `bash scripts/verify-xhs-content-dir.sh` | 全 Brief PASS |
| 5 | **00 Manager** | Owner 未反对则 **git commit** 定稿；**禁止**未 aligned commit | `git status` clean |
| 6 | **07 brand-visual** | Owner 要封面时：Brief 封面块 → Canva / visual skill | 可选 |
| 7 | **08 platform** | 仅 Owner 说「同步 Drive」 | 可选 |
| 8 | **09 data-analytics** | `bash scripts/analytics-pipeline.sh` → 读 `content/analytics/derived/next-topics-*.md` → 派 04 写 Brief | 见 `agents/09-data-analytics/DATA-NEEDS.md` |

**05 xhs-kernel：** 仅当改 `kernels/xiaohongshu/line2/` 或 classifier 规则时介入 → 必跑 `bash scripts/verify-xhs-topic.sh`（Gemini 6）。

**KPI playbook 路由（个人 IP 建立）：**

| Owner 意图 | 走哪步 | 主要文档 |
|------------|--------|----------|
| 我是谁 / 怎么介绍 / 30 秒 Pitch | **0b** | playbook §3.2–3.3 |
| 内容节奏 / 信任 / 别过早产品化 | **1** + 认知期 | playbook §4 · [OPERATING-PLAN](../../content/marketing/discovery-phase-OPERATING-PLAN.md) |
| 小红书单篇 | **2→3** | Brief CAPSTONE 映射 |
| 合作方态度 / 跨品牌 | **1** + **8** 可选 | playbook §8 · IMPORTANT |

**03 / 02：** campaign 级或商业计划 → **步 1b**（在步 2 前），产出进 `content/marketing/` 或 `content/business-brand/`。

## 一键验收

| 场景 | 命令 |
|------|------|
| **后台目标链（Owner setup 一次）** | [docs/BACKGROUND-GOAL-EVOLUTION.md](../../docs/BACKGROUND-GOAL-EVOLUTION.md) · `setup-background-goal-evolution.sh` |
| **Autopilot 单次（Debug）** | `bash scripts/manager-autopilot.sh` · [docs/AUTOPILOT.md](../../docs/AUTOPILOT.md) |
| **CEO 仪表盘（00 总览）** | `bash scripts/manager-dashboard.sh` |
| **09→04 派活块** | `content/analytics/derived/ceo-dispatch-latest.md`（pipeline 后自动刷新） |
| **Goal 按 G-* 验收 M4** | `bash scripts/verify-goals.sh` |
| **全仓集成构建（交班 / 大改后）** | `bash scripts/verify-all.sh` |
| 单 Agent 6 case | `bash scripts/verify-agent-matrix.sh --agent 04` |
| 全仓 Brief 自动验收 | `bash scripts/manager-xhs-briefs-auto-pipeline.sh` |
| Manager 步 3–4（Brief 定稿） | `bash scripts/manager-workflow-verify.sh content/xiaohongshu/<file>.md` |
| **交 Owner 前（CEO Gate）** | `bash scripts/manager-ceo-owner-gate.sh --brief …`（内嵌 auto-gate-loop） |

Goal 注册表：`integration/GOALS-REGISTRY.md`

## 派活记录（Manager 每轮必输出）

```markdown
## Manager 派活记录
- 目标：（Owner 原话摘要）
- 当前步：0x · Agent 名称
- 终端：PASS/FAIL + 命令
- 下一步：…
```

## 并行 Subagent（Task · 可选）

**不替代上表步序。** 宽口径调研 → [workflow_parallel_subagents.md](../../rules/skills/workflow_parallel_subagents.md)；**结构化深度 survey（claim/Tier/fact_check）** → [workflow_deep_research_survey.md](../../rules/skills/workflow_deep_research_survey.md)。Brief 写稿与 `evaluate` 仍 **步 2→3 顺序**；scratch 在 `tmp/parallel/` 或 `tmp/survey/`，由 04 **单线程** 写 Brief。

## 红线

- 未 `aligned: true` → 不 Drive、不称定稿
- 集成层不改 classifier docstring（05 专属）
- 不编造阅读/转化数据（09 无 CSV 则标「未验证」）
