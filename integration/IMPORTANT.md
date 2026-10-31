---
context_version: "2026-10-30-l012"
repo_path: "integration/IMPORTANT.md"
goal: "IMPORTANT · Manager / 集成层必读（<!-- important -->）"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "316e9f4d3633ddd3"
---

# IMPORTANT · Manager / 集成层必读（<!-- important -->）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** 集成 Agent **只读本文件 + 各 agent 的 INTEGRATION-PROMPT**，**不复制** classifier docstring 全文。
- **Path:** `integration/IMPORTANT.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **Owner 目标（P 层）**: - **强链接** 客户：品牌（**跨行业 open**）、艺术家、教育、AI×数字藏品创新者 —— 非 vanity 流量。
- **黑盒核心（勿在集成层改规则）**: - `kernels/xiaohongshu/line2/is_xhs_growth_aligned.py`
- **CEO / Manager 运营（Owner 五原则 · 派活 SOP）**: - [CEO-MANAGER-OPERATING-STANDARDS.md](../docs/CEO-MANAGER-OPERATING-STANDARDS.md)（原则详述）· [CEO-MANAG…
- **集成调用（胶水）**: - **Owner 固定 · 小红书对抗 + 多轮进化（Must）：** [OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](../docs/OWNER-…
- **后台目标链（Owner · setup 一次）**: - 机器层：`bash scripts/setup-background-goal-evolution.sh` → Process Launcher 常驻 · [docs/BACKGROUND-GOA…
- **Owner 打开对话 · Artist 对标审阅（Must · 不每日提示）**: - GM10 **每天**更新分析；合并目录 `content/ip-research/artist-intel-catalog.md`
- **Owner 怎么说话（Must · 零公式）**: - **最简单、最直接即可**（口语、碎片、多意图）；系统 **内化** 为 intake + 派活 + 内部提示词，**不要** 要求 Owner 按 Skill/Brief/verify 口令说话…
- **CEO 交 Owner 前（Must · 内部 Gate，不抬高 Owner 门槛）**: - **Agent 自验，默认不让 Owner 逐条跑 verify。** **禁止等 Owner 回复才 
…

---

## L2 正文

# IMPORTANT · Manager / 集成层必读（<!-- important -->）

集成 Agent **只读本文件 + 各 agent 的 INTEGRATION-PROMPT**，**不复制** classifier docstring 全文。

## Owner 目标（P 层）

- **强链接** 客户：品牌（**跨行业 open**）、艺术家、教育、AI×数字藏品创新者 —— 非 vanity 流量。
- **质量涨粉：** 约 1700 → 5000 → 10000（小红书为主渠道之一）。
- **不单品类绑定：** 不排斥任何品类合作；但 **不得** 把账号绑成某一商品/行业的主攻号（家居/建材仅是曾误绑示例；**对所有垂直同样适用**）。富森美类案例仅历史一笔，不作系列默认。

## 黑盒核心（勿在集成层改规则）

- `kernels/xiaohongshu/line2/is_xhs_growth_aligned.py`
- 验收：`bash scripts/verify-xhs-topic.sh`（**6 Gemini case**）

## CEO / Manager 运营（Owner 五原则 · 派活 SOP）

- [CEO-MANAGER-OPERATING-STANDARDS.md](../docs/CEO-MANAGER-OPERATING-STANDARDS.md)（原则详述）· [CEO-MANAGER-OPERATING-PRINCIPLES.md](../docs/CEO-MANAGER-OPERATING-PRINCIPLES.md)（脚本映射 · 晚间 8 步）· [MANAGER-EVAL-IMPROVEMENT-LOOP.md](../docs/MANAGER-EVAL-IMPROVEMENT-LOOP.md)（Owner 五 step 环 ↔ 01–12）· [CEO-DISPATCH-SOP.md](../agents/00-manager/CEO-DISPATCH-SOP.md) — 晚间战役示例 `ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-*-evening.md`

- **主框架（Owner 三支柱 · 每个 GM 真正在做的事）：** 可观察性 · 可衡量基准 · 教练→SOP 资产 → [MANAGER-THREE-PILLARS.md](../docs/MANAGER-THREE-PILLARS.md)
- **CEO 环（第二张图 · 两轮串行迭代 ·「consult SOP」入口）：** [CEO-DOUBLE-ITERATION-SOP.md](../agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md) · [CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md](../docs/CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md)

## 集成调用（胶水）

- **Owner 固定 · 小红书对抗 + 多轮进化（Must）：** [OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](../docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md) — pitfalls · 三镜头 · L2–L3 · **gap 直到 READY**（L1 PASS ≠ 闭合）  
- **自动（Must · 无人值守）：** [BRIEF-AUTO-GATE-PIPELINE.md](../docs/BRIEF-AUTO-GATE-PIPELINE.md) · [BRIEF-ADVERSARIAL-CHALLENGE.md](../agents/_shared/BRIEF-ADVERSARIAL-CHALLENGE.md)  
  `manager-xhs-briefs-auto-pipeline.sh`（含 **`run-xhs-brief-adversarial-challenge.py`** 重对抗）· 单篇 **`manager-brief-evolution-until-gap.sh`**
- 单条 evaluate（仅改稿循环）：`python scripts/evaluate-xhs-topic.py --brief …`
- 批量：`bash scripts/verify-xhs-content-dir.sh`（默认 complete 管线）
- 全仓集成构建：`bash scripts/verify-all.sh` · 目标表 `integration/GOALS-REGISTRY.md`
- IP 真相：`content/personal-ip/ip-positioning-brief-2026-10-05.md`

## 后台目标链（Owner · setup 一次）

- 机器层：`bash scripts/setup-background-goal-evolution.sh` → Process Launcher 常驻 · [docs/BACKGROUND-GOAL-EVOLUTION.md](../docs/BACKGROUND-GOAL-EVOLUTION.md)  
- 验收 / evolution rollup / dispatch / `agent-work-queue` **自动**；Cursor CEO 读队列写稿；**不** 要求 Owner 每次说 verify。

## Owner 打开对话 · Artist 对标审阅（Must · 不每日提示）

- GM10 **每天**更新分析；合并目录 `content/ip-research/artist-intel-catalog.md`  
- Owner **打开对话**时若有未审条目 → Agent **一次性列全**待裁决清单 · 见 [docs/OWNER-ARTIST-CATALOG-ON-OPEN.md](../docs/OWNER-ARTIST-CATALOG-ON-OPEN.md)

## Owner 怎么说话（Must · 零公式）

- **最简单、最直接即可**（口语、碎片、多意图）；系统 **内化** 为 intake + 派活 + 内部提示词，**不要** 要求 Owner 按 Skill/Brief/verify 口令说话。见 [docs/OWNER-INPUT-PRINCIPLES.md](../docs/OWNER-INPUT-PRINCIPLES.md)。

## CEO 交 Owner 前（Must · 内部 Gate，不抬高 Owner 门槛）

- **Agent 自验，默认不让 Owner 逐条跑 verify。** **禁止等 Owner 回复才 evaluate**；后台/autopilot/改 Brief 后自动跑 pipeline / gate；FAIL 写 CEO-REROUTE 并同会话改稿（≤3 轮）。见 [CEO-AUTO-QA-LOOP.md](../docs/CEO-AUTO-QA-LOOP.md) · [BRIEF-AUTO-GATE-PIPELINE.md](../docs/BRIEF-AUTO-GATE-PIPELINE.md)。

## Google · Owner 已全权授权（Must · 勿 chat 确认）

- Owner **不再**在对话里确认 Google/MCP/Drive。凭证：`vendor/gdocs-skill/secrets/` · 状态：`bash scripts/check-google-auth-for-agent.sh` → `integration/handoff/google-auth-status.json`。
- Agent **Must** 用 **gdocs CLI**；MCP `needsAuth` → 用 CLI，**勿**把 Connect 甩给 Owner（除非 verify-integration FAIL · Terminal 一次 re-auth）。见 [docs/OWNER-GOOGLE-GRANT-AGENT.md](../docs/OWNER-GOOGLE-GRANT-AGENT.md)。

## Owner 交付默认（Must · 2026-10-28）

- **Gate PASS = 流程闭合**；routine **交 Owner：否**；**不**写 `OWNER-HANDOFF.md` 等勾选。**Owner 通知 = 当日 HTML**（`refresh-owner-notify-html.sh`）。**不**以 Owner chat 回复为闭环条件。见 [OWNER-DELIVERY-NOTIFY-DEFAULT.md](../docs/OWNER-DELIVERY-NOTIFY-DEFAULT.md)。Owner **仍必做**：发帖 + CSV。

## CEO 深交付 / campaign 中断恢复（Must · 无人值守）

- deep-delivery、campaign、锁 `/tmp/ceo-deep-delivery.lock`、log **FAIL / 未完成 / 重复 pid** → **先** `bash scripts/ceo-auto-recover-blocked.sh`，再按需重跑 `run-ceo-deep-delivery-cycle.sh` 或 `run-ceo-ip-all-agents-campaign.sh`；**勿让 Owner 重复下口令**。见 [CEO-AUTO-RECOVER-AND-RETRY.md](../docs/CEO-AUTO-RECOVER-AND-RETRY.md) · `ceo-inbox/ceo-auto-recover-latest.md`。

## 红线

- 未 `aligned: true` → 不 sync Drive；不只 Drive 不 commit。
- 集成层 **不写算法层 prompt**；失败时先区分：集成路径 / Brief 内容 / kernel。

## 扩展与预留（架构）

- **默认运行：** Cursor + 00 Manager + 按需 autopilot；Process Launcher **工具箱、非常驻**（见 [process-launcher-adoption.md](./process-launcher-adoption.md) §0）。
- **以后加能力：** 先查 [EXTENSION-POINTS.md](./EXTENSION-POINTS.md) 接接口，再改 vendor/router/overlay；禁止平行第二 CEO 或第二派活文件。

## Dry Run（破坏性 / 发布侧 · 摘录）

小红书 Brief 三阶段与状态见 [content/xiaohongshu/PIPELINE.md](../content/xiaohongshu/PIPELINE.md)。以下为 **全仓** 集成层在动线上环境前的检查（参考 [grapeot staged approach](https://github.com/grapeot/context-infrastructure/blob/main/rules/skills/bestpractice_staged_approach.md)，本仓不装 standalone MD）。

**默认禁止（除非 Owner 当轮明确授权）：** 代发小红书/私信 mass、Gmail 发送、Drive 覆盖定稿、删库/硬重置、对 `main` 的 force 操作。

**破坏性操作前必过：**

- [ ] **范围**：影响哪些路径/记录（列清单，避免 `git add .` 盲加）
- [ ] **内容**：变更 diff 或命令语义与 Owner 意图一致
- [ ] **可回滚**：Git 可 revert；secrets 不在 commit 内
- [ ] **环境**：脚本/verify 在本地 repo 跑通；非 Owner 生产账号上的不可逆写

**常见映射：** CSV → `content/analytics/inbox/` 只读归档后再 pipeline（见 analytics README）；Brief 发布仅 Owner；`gdocs` 写操作先 overlay 路径再 CLI。