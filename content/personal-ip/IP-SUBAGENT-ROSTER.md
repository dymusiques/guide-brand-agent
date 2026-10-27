# IP 打造 · Sub-Agent 岗位表（与 00 CEO 编制）

> **直接回答：** 本仓 **没有** 在后台常驻、自动并行跑 IP 的「Sub-Agent 进程」。  
> **有** 两类东西容易混叫 Sub-Agent，下面分开写清。

---

## 两类「Sub-Agent」分别是什么

| 类型 | 是什么 | IP 打造里怎么用 |
|------|--------|-----------------|
| **A · 职能 Sub-Agent（主编制）** | `agents/01`–`09` 九个角色 + 集成 prompt | **单会话内顺序扮演**（读 `INTEGRATION-PROMPT.md` → 产出 → verify），由 **00 CEO** 派活 |
| **B · Cursor Task Sub-Agent（临时工）** | `explore` / `generalPurpose` / `bugbot` 等 | **仅** 宽调研、红队、独立 review；产出在 `tmp/parallel/`，**不** 并行写同一 Brief |
| **C · Collector + Evaluator（全 Agent Must）** | `collector-intake.py` · `evaluate-edit-distance.py` | v0 吸收全部 intake；v1+ 进化；`metrics.jsonl` 平均编辑距离 · [COLLECTOR-EVALUATOR.md](../../agents/_shared/COLLECTOR-EVALUATOR.md) |
| **D · 日更 GM 三件套（10–12）** | `run-daily-gm-trio.sh` · 后台 09:00 | Artist 对标 · IP 日评 · **Owner daily brief** · [DAILY-GM-TRIO-SOP.md](../../docs/DAILY-GM-TRIO-SOP.md) |

**不是 Sub-Agent：** `vendor/` 工具箱（gdocs、writing、IP×13）、`05 kernel` 里的 **Gemini 函数**（是质检引擎，不是写手岗位）。

权威边界：[parallel-subagents-adoption.md](../../integration/parallel-subagents-adoption.md) · [AUTO-WORKFLOW](../../agents/00-manager/AUTO-WORKFLOW.md) §并行 Subagent。

---

## 组织图（IP 打造）

```text
Owner（目标 · 发布 · 数据 · 终审）
    │
    ▼
00 · CEO / 总 Manager（派活 · 收 GM 汇报 · commit 门控）→ 见 IP-MANAGEMENT-HIERARCHY.md
    │
    ├── 01–09 · 部门总经理（二级 Manager：Collector + v0→vN + Evaluator + GM-REPORT）
    ├── 0a · 数据读栈 · 0b · Pitch（01 GM）
    ├── 01 IP GM · 02 商业 GM · 03 营销 GM · 04 小红书 GM（含 2a）
    ├── 05 质检 GM · 06 管线 GM · 07 视觉 GM · 08 平台 GM · 09 数据 GM
```

---

## 职能 Sub-Agent 岗位卡（A 类 · 一人一会话扮演）

| 岗位 ID | 目录 | 负责板块 | 典型触发 | 主要产出 | 验收 / 函数壳 |
|---------|------|----------|----------|----------|----------------|
| **00** | `agents/00-manager/` | **CEO** · 拆目标 · 步序 · 汇总 PASS/FAIL | Owner 任何写/做/IP/小红书目标 | 派活记录 · commit 门控 | `manager-autopilot.sh` · `verify-all.sh` |
| **01** | `agents/01-personal-ip/` | **IP 方向** · 受众 · 三支柱 · 不绑垂直 · Pitch | 我是谁 / 合作范围 / CAPSTONE | `content/personal-ip/` | IP Brief 一致 · playbook §3–4 |
| **02** | `agents/02-business-brand/` | **商业文档** · SWOT · 定位商业侧 | 商业计划 / SWOT / 竞品框 | `content/business-brand/` | `evaluate-business-brand` · G-BUSINESS-BRAND |
| **03** | `agents/03-marketing-strategy/` | **触达 / campaign** · 渠道节奏 | 触达计划 · 认知期 program | `content/marketing/` | `evaluate-marketing-campaign` · G-MARKETING-CAMPAIGN |
| **04** | `agents/04-xhs-topic-manager/` | **小红书写稿** · 选题 · Brief/packages · 2a 口播 | 笔记 / 视频 / 标题 / pivot 系列 | `content/xiaohongshu/` | `evaluate-xhs-topic.py` · voice-qa |
| **05** | `agents/05-xhs-kernel/` | **对齐判定**（Gemini yes/no） | 改 classifier / 专项对齐 | `kernels/xiaohongshu/line2/` | `verify-xhs-topic.sh` **6 case** |
| **06** | `agents/06-xhs-content-pipeline/` | **Brief 目录** · 批量规范 | 多 Brief 齐检 · 交班 | 同目录批量 | `verify-xhs-content-dir.sh` |
| **07** | `agents/07-brand-visual/` | **封面** · Canva · kit | 「要封面」 | Brief 封面块 · 视觉稿 | agent 07 verify 6 · G-BRAND-VISUAL |
| **08** | `agents/08-platform-integration/` | **Drive/gdocs** · OAuth | 「同步 Drive」 | Drive Doc（可选） | `verify-integration.sh` · G-PLATFORM-SYNC |
| **09** | `agents/09-data-analytics/` | **CSV→策略** · next-topics · ceo-dispatch | 新 xlsx/CSV · 发帖后复盘 | `content/analytics/derived/` | `analytics-pipeline.sh` · G-ANALYTICS-EVIDENCE |

**步 2a（视频迭代）：** 不是第十个 Agent，是 **04 的子工序**（Round1→点选→Round2），见 [XHS-VIDEO-ITERATION.md](../xiaohongshu/XHS-VIDEO-ITERATION.md)。

**步 0a：** **09 + 04 读栈**，见 [XHS-CONTENT-INTAKE-STACK.md](../../docs/XHS-CONTENT-INTAKE-STACK.md)。

---

## Cursor Task Sub-Agent（B 类 · 按需临时工）

| Task 类型 | 建议谁（CEO）派给 | 可做什么 | **禁止** |
|-----------|-------------------|----------|----------|
| `explore` | 00 → 任意板块查仓 | 快搜路径、INTEGRATION-PROMPT、历史 Brief | 写定稿 Brief |
| `generalPurpose` | 00 → 01/02/03 调研 | 红队、行业坑、竞品一句 | 代替 04 写口播 |
| `bugbot` / `security-review` | 00（Owner 明确要求） | 改 scripts/verify 后的 review | 改 kernel 规则 |
| `ci-investigator` | 00 | CI 失败摘要 | 内容 IP |

**落盘：** `tmp/parallel/<session>/` · 定稿仍 **04 单线程** → evaluate → 06。

---

## Goal 注册表 ↔ Sub-Agent（派活时标注 G-*）

见 [integration/GOALS-REGISTRY.md](../../integration/GOALS-REGISTRY.md)。CEO 派活时写：`本任务 G-STRONG-LINK + G-NOT-SINGLE-VERTICAL-LOCK`，由 **01/04/05** 分工落实。

---

## 和「红队文档」的关系

[2026-10-27-ip-adversarial-red-team.md](./2026-10-27-ip-adversarial-red-team.md) · **[FULL-DRILL-REPORT](./2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md)**（CEO+Evaluator+9 GM 评分）= 职能 Sub-Agent **对抗演练**；可用 **B 类 Task** 并行加深 02/03/09，但 **不** 增加新编制岗位。

---

## Owner 一句话

- **日常 IP 打造：** 只有 **1 个 Cursor 对话 + 00 CEO**，里面 **轮流扮演 01–09**（顺序见 AUTO-WORKFLOW）。  
- **Sub-Agent：** 指的就是这 **9 个职能岗位**；不是 9 个自动运行的机器人。  
- **要「全员动起来」：** 说「按 IP-SUBAGENT-ROSTER 轮询派活」或「跑红队 §F」— CEO 按表让每个岗位出一段产出或攻击，再进 04 写稿。
