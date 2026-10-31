---
context_version: "2026-10-30-l012"
repo_path: "docs/AGENT-TAKEOVER.md"
goal: "新 Agent 接手 · 当前程序状态与指挥手册"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "75467ade311103d1"
---

# 新 Agent 接手 · 当前程序状态与指挥手册

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **更新：** 2026-10-28（CEO/GM 三支柱 · 双图 · 双轮迭代 · 一句话触发 · 接手 JSON）  
> **验证：** `bash scripts/verify-handoff.sh`（含本文件检查）· `bash scripts/verify-agent-takeover.sh`  
> **CEO/GM 接手包（Must）：
- **Path:** `docs/AGENT-TAKEOVER.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **1. Owner 成功目标（G-* · 指挥时不丢）**: 注册表：[integration/GOALS-REGISTRY.md](../integration/GOALS-REGISTRY.md) · JSON：`integration/goals/regi…
- **3. 运营快照（新 Agent 接手后第一眼）**: - **下一执行动作（Owner）：** 发 discovery **#1**，回填 `## 发布状态`（已发布 + 日期 + 笔记链接）→ `bash scripts/manager-dashboa…
- **5. 验收命令（新 Agent Must 跑）**: **一条命令（推荐 · 含 MD 锚点 + 10×6 + M4 + Gemini 6 + autopilot）：**


---

## L2 正文

# 新 Agent 接手 · 当前程序状态与指挥手册

> **更新：** 2026-10-28（CEO/GM 三支柱 · 双图 · 双轮迭代 · 一句话触发 · 接手 JSON）  
> **验证：** `bash scripts/verify-handoff.sh`（含本文件检查）· `bash scripts/verify-agent-takeover.sh`  
> **CEO/GM 接手包（Must）：** [HANDOFF-CEO-GM-SOP-PACK.md](HANDOFF-CEO-GM-SOP-PACK.md) · JSON [integration/handoff/ceo-gm-operating-manifest.json](../integration/handoff/ceo-gm-operating-manifest.json)  
> **接手 SOP：** [NEW-AGENT-WORKFLOW-SOP.md](NEW-AGENT-WORKFLOW-SOP.md) · 思维导图 [workflow-handoff-mindmap.html](workflow-handoff-mindmap.html)  
> **一页纸：** [HANDOFF-SOP.md](HANDOFF-SOP.md) · **存储策略：** [HANDOFF-COMPLETENESS.md](HANDOFF-COMPLETENESS.md)


## 1. Owner 成功目标（G-* · 指挥时不丢）

注册表：[integration/GOALS-REGISTRY.md](../integration/GOALS-REGISTRY.md) · JSON：`integration/goals/registry.json`

| 目标 | 含义（摘要） |
|------|----------------|
| **G-STRONG-LINK** | B2B 强链接 CTA（私信/合作/评估），非 vanity 流量 |
| **G-QUALITY-GROWTH** | 小红书 1700→5000→10000 **里程碑**；**仅 Owner/CSV 验证**，不进 kernel 硬断言 |
| **G-NOT-SINGLE-VERTICAL-LOCK** | 全品类可合作；**不**把账号绑成任一垂直主攻号（家居仅为曾误绑示例） |
| **G-CROSS-INDUSTRY** | 品牌合作跨行业 open |
| **G-BRIEF-ALIGNED-GATE** | Brief 须 `evaluate --brief` → **aligned: true** 才算定稿 |
| **G-ANALYTICS-EVIDENCE** | 有 CSV 才写 derived；无数据不编造 |
| **G-PLATFORM-SYNC** | gdocs/Drive/Git 读路径可靠 |
| **G-MARKETING-CAMPAIGN** | 触达/campaign 文档在 `content/marketing/` |
| **G-BUSINESS-BRAND** | 商业品牌文档在 `content/business-brand/` |
| **G-BRAND-VISUAL** | 封面块进 Brief；Canva skill |

IP 一句话：[content/personal-ip/ip-positioning-brief-2026-10-05.md](../content/personal-ip/ip-positioning-brief-2026-10-05.md)

### 1.1 Owner 架构三要求（本对话 · 已写入 Git）

| # | 要求 | 实现方式 | 文档 / 命令 |
|---|------|----------|-------------|
| **1** | **总 CEO** | Cursor 会话内 **00 Manager** 解析 Owner 目标、派活、汇总；规则自动生效 | [AUTO-WORKFLOW.md](../agents/00-manager/AUTO-WORKFLOW.md) · `.cursor/rules/danying-manager-auto.mdc` |
| **2** | **Workflow 可自动跑** | 一条命令串 Goal 验收 → 仪表盘 → 09 → CEO 派活块（**不含** App 发帖 / CSV 导入） | [AUTOPILOT.md](AUTOPILOT.md) · `bash scripts/manager-autopilot.sh` |
| **3** | **每步有 Manager，检细步再交 CEO** | **01–09** 各角色 = 部门 Manager；每步读 `INTEGRATION-PROMPT.md` → 产出 → **verify/evaluate PASS** → 00 读 dashboard / derived / 终端 Summary 再派下一步 | [agents/README.md](../agents/README.md) · `integration/agents/a*.py`（**10×6 glue**）· `scripts/agent-shells/*.sh` · kernel **6 case**（05/02/03） |

**反馈回 CEO 的三条总线：** ① 终端 `RESULT: PASS/FAIL` ② `content/analytics/derived/manager-dashboard-*.md` ③ `ceo-dispatch-latest.md`（09→04 半自动派活）。监督环：[DANYING-BRAND-AGENT-INTEGRATION.md](DANYING-BRAND-AGENT-INTEGRATION.md) · Manager's Loop。

**刻意不做：** 多进程后台 CEO、自动发帖、自动爬小红书数据（Owner → inbox CSV）。


## 3. 运营快照（新 Agent 接手后第一眼）

- **下一执行动作（Owner）：** 发 discovery **#1**，回填 `## 发布状态`（已发布 + 日期 + 笔记链接）→ `bash scripts/manager-dashboard.sh`
- **15 天快检：** 自 **#1 发布日** 起算；未填发布日期则仪表盘提示「尚未记录首发发布日期」
- **派活块（09→04）：** `content/analytics/derived/ceo-dispatch-latest.md`（autopilot 自动刷新）
- **听见 Daily：** 日更，独立 skill；认知期不强制每条转化


## 5. 验收命令（新 Agent Must 跑）

**一条命令（推荐 · 含 MD 锚点 + 10×6 + M4 + Gemini 6 + autopilot）：**

```bash
bash scripts/verify-handoff-program.sh
```

**分项：**

```bash
bash scripts/verify-agent-takeover.sh   # 本文 + MANIFEST + 口令规则
bash scripts/verify-handoff.sh
bash scripts/manager-autopilot.sh
bash scripts/verify-manager-integration.sh
# 交班 capstone：
VERIFY_TIER=release bash scripts/verify-all.sh
```

**2026-10-17 实测摘要：** goals 10/10、matrix 60/60、autopilot PASS、CI verify-all PASS；Release 下 05/02/03 Gemini 6 均 PASS；verify-all 嵌套跑时矩阵步曾偶发 FAIL，单独 matrix 重跑 PASS。


**给 Owner：** Agent 侧 workflow 已按成功目标闭环；你只需 **发帖 + CSV + 运营复盘**。新 Agent 读本文 + 跑 §5 即可接手派活。