---
context_version: "2026-10-30-l012"
repo_path: "docs/CEO-MANAGER-OPERATING-STANDARDS.md"
goal: "CEO / Manager 运营标准 · Owner 五原则（持久团队资产）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "dffbfea3f228ef1a"
---

# CEO / Manager 运营标准 · Owner 五原则（持久团队资产）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** **文件**
- 派活：`content/evolution/00-manager/ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27-evening.md`
- 日间关联：`…/CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27.md`
- 报告：`…/ceo-ip-all-agents-
- **Path:** `docs/CEO-MANAGER-OPERATING-STANDARDS.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **L1 任务（压缩 · Open WebUI / Cursor 顶栏）**: - **Goal:** > **签发：** 2026-10-27 · 00 Manager 代 CEO
- **章节锚点**: - **总览：五原则 → 落地**: | # | Owner 原则 | CEO/GM 一句话做法 | 主要产物 | 主验收 |
- **示范案例（Worked example）：2026-10-27 晚间战役**: **文件**
- **相关**: - [MANAGER-THREE-PILLARS](./MANAGER-THREE-PILLARS.md)（Owner 三支柱主框架：可观察性 / 可衡量基准 / 教练→SOP）


---

## L2 正文

# CEO / Manager 运营标准 · Owner 五原则（持久团队资产）

> **签发：** 2026-10-27 · 00 Manager 代 CEO  
> **适用：** 00 Manager（CEO）与 01–12 全部 GM。Owner 口头说一次，**写进本文件 + SOP = 团队资产**，新会话/新机/新 Agent 读本文件即继承，不依赖旧对话。  
> **主框架（Owner 三支柱）：** 可观察性 · 可衡量基准 · 教练→SOP 资产 → [MANAGER-THREE-PILLARS.md](./MANAGER-THREE-PILLARS.md)（本文五原则是其落地细则，不冲突）  
> **北极星（不变）：** **打造 Danying 个人 IP**（长笛 / 教育 / 咨询；小红书 Discovery + Artist Watchlist + 听见 Daily 同一叙事轴）。  
> **配套：** [CEO-MANAGER-OPERATING-PRINCIPLES.md](./CEO-MANAGER-OPERATING-PRINCIPLES.md)（脚本映射 · 晚间 8 步）· [AUTO-WORKFLOW](../agents/00-manager/AUTO-WORKFLOW.md) · [CEO-DISPATCH-SOP](../agents/00-manager/CEO-DISPATCH-SOP.md) · [CEO-OWNER-DEADLINE-DELIVERY](./CEO-OWNER-DEADLINE-DELIVERY.md) · [CEO-AUTO-QA-LOOP](./CEO-AUTO-QA-LOOP.md) · [CEO-AUTO-RECOVER-AND-RETRY](./CEO-AUTO-RECOVER-AND-RETRY.md)

## 总览：五原则 → 落地

| # | Owner 原则 | CEO/GM 一句话做法 | 主要产物 | 主验收 |
|---|-----------|-------------------|----------|--------|
| 1 | 清晰的委派：项目开始不含糊 | 开工前落盘 dispatch：North star + 每 Agent 任务 + 终端验收 + 截止 | `ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-<date>.md` | dispatch 文件存在且每行有验收命令 |
| 2 | 有把握的评估：可衡量进展 | 一切「完成」= 命令 PASS + 数字（failures/轮次/篇数），不用形容词 | campaign 报告 `.md/.log` · verify-logs | `RESULT: PASS` · failures 0 · Owner Gate 字段 |
| 3 | 数据驱动改进，非猜测 | 改稿依据 = 09 证据 / gate FAIL 原因 / metrics；无数据标「未验证」 | `content/analytics/derived/` · `CEO-REROUTE.md` · metrics.jsonl | `analytics-pipeline.sh` · `evolution-metrics-summary.py` |
| 4 | 教练式引导促成长 | CEO 给 GM 的是「哪条 gate 为何 FAIL + 改哪一段」，不是代写；GM 自改 v(N+1) | `CEO-REROUTE.md` · GM-REPORT | 打回轮次 n/3 递减、同类 FAIL 不复发 |
| 5 | 个人洞见 → 持久团队资产 | Owner 一句洞见 → 当天落盘成 doc/SOP/脚本/rule，并进索引 | 本文件 · SOP · WORKSPACE 索引 · `.mdc` 规则 | `verify-handoff.sh` · 索引可检索 |


## 2. 有把握的评估：可衡量进展

**CEO 必做**
- 「进展」只认三类证据：① 终端 `PASS/FAIL` + 命令；② 数字（failures、gate 轮次 n/3、PASS 篇数 x/y）；③ 落盘文件路径。
- 每轮输出 **Manager 派活记录**（字段见 SOP）：**Owner Gate PASS/FAIL · 打回轮次 n/3 · 交 Owner：是/否**。
- 交 Owner 的任何东西须 auto-gate **PASS**（见 [CEO-AUTO-QA-LOOP](./CEO-AUTO-QA-LOOP.md)）。
- 未做的事**明写**（未 commit / 未发帖 / 未 sync Drive / 0 CSV）。

**验证命令**
```bash
bash scripts/manager-dashboard.sh                       # 总览
bash scripts/manager-ceo-owner-gate.sh --brief <brief>  # 交 Owner 前
bash scripts/manager-workflow-verify.sh <brief>         # 步 3–4
VERIFY_GOALS_SKIP_PLATFORM=0 bash scripts/run-ceo-ip-all-agents-campaign.sh   # 01–12 全员
```
**反模式 ✗**：「差不多好了」「应该没问题」· 只跑 1 条 shell 称深筛 · 半截日志当交付（无 `RESULT: PASS` 标记即作废）· 隐藏未做项。


## 4. 教练式引导促成长

**CEO 对 GM（Agent）**
- REROUTE 写法：**症状 → 为什么违反哪条标准 → 改哪一段 → 如何自验**；让 GM 自己出 v(N+1)，CEO 不代笔。
- 同类错误第 2 次出现 → 把规则/检查**固化进 GM 的 INTEGRATION-PROMPT 或 challenge 节**（让成长可复用）。
- 打回 ≤ 3 轮；3 轮仍 FAIL → 升级 Owner **附诊断**，不甩锅。

**CEO 对 Owner**
- Owner 是方向与裁决者；CEO 把 Owner 的「判断依据」反向沉淀（例：Owner 为何否掉某标题 → 写入红队/Brief 规则），让 Owner 越来越少被打扰。
- 汇报用 12 Owner Daily Brief 的一页式口吻（07 语气），说清「做了什么 / 数字 / 需你裁决的 1–2 件事」。

**产物：** `CEO-REROUTE.md` · GM-REPORT · 更新后的 `INTEGRATION-PROMPT.md`  
**验证：** 同一 Brief 打回轮次逐篇下降（campaign 晚间：Discovery 01 round **1/3** 即过）；`ceo-auto-fix-brief.py` 记录可追溯。  
**反模式 ✗**：CEO 直接代写全文 · REROUTE 只写「不行重来」· 把 FAIL 稿交 Owner 验 · 同一错误反复出现不沉淀。


## 总反模式清单（速查）

1. 无书面 dispatch 就开工  
2. 完成度无证据（无命令/数字/路径）  
3. 编造数据或不标「未验证」  
4. 把 FAIL 稿或「要不要 evaluate」交给 Owner  
5. CEO 代写 GM 产出，不做教练式 REROUTE  
6. 洞见不落盘 / 不入索引  
7. 阻塞时问 Owner「要不要重跑」→ 应自动 `bash scripts/ceo-auto-recover-blocked.sh`  
8. 并行 heavy Gemini 重复跑（用 lock / `SKIP_GEMINI`）  
9. 只跑一轮 batch 应付截止 → 应 `run-ceo-deep-delivery-cycle.sh`

---

## 示范案例（Worked example）：2026-10-27 晚间战役

**文件**
- 派活：`content/evolution/00-manager/ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27-evening.md`
- 日间关联：`…/CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27.md`
- 报告：`…/ceo-ip-all-agents-campaign-20261027-182723.md`（`.log`）

| 原则 | 在晚间战役中的体现 |
|------|-------------------|
| 1 委派清晰 | dispatch 含 North star（打造 IP）、战役题「90 天 IP 筛选漏斗：从 Discovery 01 定稿到 Artist 强链接」、01–12 每 Agent 任务+验收命令、`G-*` 绑定 |
| 2 可衡量 | `RESULT: PASS` · failures **0** · 01–12 矩阵全 PASS · Gate **PASS 0/3 打回（round 1/3 过）** · 06 SEO 6/6 |
| 3 数据驱动 | 09 `--live` + `screen-artist-watchlist.py`；inbox 0 CSV → 数据结论明标「未验证」；06 卫生项来自 verify 报错（H1 > 40 字）而非猜测 |
| 4 教练式 | 首次 18:21 进程被回收 → `ceo-auto-recover-blocked.sh` 诊断清锁重跑，不问 Owner；Discovery 01 以 gate 为准自改 v1.1 |
| 5 持久资产 | 战役产出 dispatch/报告/HTML 落 `ceo-inbox/`；本文件与 SOP 把这套做法固化为模板 |

**诚实记录的事故/未做：** 首次启动在 03 Gemini 阶段被回收；deep-delivery 半截日志勿当交付；未 commit · 未 sync Drive · 未发帖。

## 相关
- [MANAGER-THREE-PILLARS](./MANAGER-THREE-PILLARS.md)（Owner 三支柱主框架：可观察性 / 可衡量基准 / 教练→SOP）
- [MANAGER-EVAL-IMPROVEMENT-LOOP](./MANAGER-EVAL-IMPROVEMENT-LOOP.md)（Owner 评估改进环图 ↔ 各 GM 对照）
- [CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP](./CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md)（Owner 第二张图：CEO 环 · Consult SOP · 两轮串行迭代审计）· [CEO-DOUBLE-ITERATION-SOP](../agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md)
- [WORKFLOW-CEO-ARCHITECTURE](./WORKFLOW-CEO-ARCHITECTURE.md) · [BRIEF-AUTO-GATE-PIPELINE](./BRIEF-AUTO-GATE-PIPELINE.md)