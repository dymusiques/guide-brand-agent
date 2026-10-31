# 鸭哥 · Personal IP 与 CEO 体系 · GitHub 导读

> **仓库根目录：** [github.com/dymusiques/guide-brand-agent](https://github.com/dymusiques/guide-brand-agent)  
> **说明：** 本仓当前为 **Private**。鸭哥需被添加为 **Collaborator** 后，下文所有 `blob/main/…` 链接才可点击；未授权时会显示 404（不是文件不存在）。  
> **公开备用入口（无需登录）：** [Gist · 摘要 + 思维导图](https://gist.github.com/dymusiques/1efd20ba040828b8e9def78de9e56672) · [htmlpreview · 总流程导图](https://htmlpreview.github.io/?https://gist.githubusercontent.com/dymusiques/1efd20ba040828b8e9def78de9e56672/raw/owner-stack-openwebui-mindmap.html)

---

## 1. 建议阅读顺序（30 分钟扫一遍）

| 顺序 | 看什么 | GitHub 链接 |
|------|--------|-------------|
| ① | 仓库总规则与路由 | [AGENTS.md](https://github.com/dymusiques/guide-brand-agent/blob/main/AGENTS.md) · [rules/WORKSPACE.md](https://github.com/dymusiques/guide-brand-agent/blob/main/rules/WORKSPACE.md) |
| ② | 新 Agent / CEO 接手 | [docs/AGENT-TAKEOVER.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/AGENT-TAKEOVER.md) · [docs/HANDOFF-MD-MANIFEST.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/HANDOFF-MD-MANIFEST.md) |
| ③ | Personal IP 定位与 KPI | [content/personal-ip/ip-positioning-brief-2026-10-05.md](https://github.com/dymusiques/guide-brand-agent/blob/main/content/personal-ip/ip-positioning-brief-2026-10-05.md) · [content/personal-ip/2026-10-18-key-person-of-influence-capstone-playbook.md](https://github.com/dymusiques/guide-brand-agent/blob/main/content/personal-ip/2026-10-18-key-person-of-influence-capstone-playbook.md) |
| ④ | CEO 全量怎么跑 | [docs/CEO-FULL-EXECUTION-MANDATE.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/CEO-FULL-EXECUTION-MANDATE.md) · [agents/00-manager/AUTO-WORKFLOW.md](https://github.com/dymusiques/guide-brand-agent/blob/main/agents/00-manager/AUTO-WORKFLOW.md) |
| ⑤ | 六项测评 + evolution | [docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md) · [docs/MANAGER-EVAL-IMPROVEMENT-LOOP.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/MANAGER-EVAL-IMPROVEMENT-LOOP.md) |
| ⑥ | 可点击总导图（HTML） | [docs/owner-stack-openwebui-mindmap.html](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/owner-stack-openwebui-mindmap.html)（浏览器打开 raw 或本机 file） |

---

## 2. 仓库里「文件分布」一览（目录树）

点文件夹即可浏览 GitHub 上的全部文件分布：

| 区域 | 含义 | 目录链接 |
|------|------|----------|
| **Personal IP 定稿** | 定位、Pitch、intake、红队、CAPSTONE 参考 | [content/personal-ip/](https://github.com/dymusiques/guide-brand-agent/tree/main/content/personal-ip) |
| **小红书 Brief / 长稿** | 选题、Brief、pipeline | [content/xiaohongshu/](https://github.com/dymusiques/guide-brand-agent/tree/main/content/xiaohongshu) |
| **营销 / Discovery** | 认知期、campaign | [content/marketing/](https://github.com/dymusiques/guide-brand-agent/tree/main/content/marketing) |
| **00–12 部门 Agent** | 各部门 INTEGRATION-PROMPT | [agents/](https://github.com/dymusiques/guide-brand-agent/tree/main/agents) |
| **CEO / GM 集成胶水** | Python 壳、`a01`–`a09` | [integration/agents/](https://github.com/dymusiques/guide-brand-agent/tree/main/integration/agents) |
| **Handoff / 机器可读** | manifest、CEO 周期 JSON | [integration/handoff/](https://github.com/dymusiques/guide-brand-agent/tree/main/integration/handoff) |
| **验收脚本** | CEO pipeline、gate、evolution | [scripts/](https://github.com/dymusiques/guide-brand-agent/tree/main/scripts) |
| **Cursor 规则 / Skills** | 自动 CEO、xhs 文风 | [.cursor/rules/](https://github.com/dymusiques/guide-brand-agent/tree/main/.cursor/rules) · [.cursor/skills/](https://github.com/dymusiques/guide-brand-agent/tree/main/.cursor/skills) |
| **Open WebUI RAG（随仓）** | Drive/corpus sync 脚本 | [integration/openwebui-rag/](https://github.com/dymusiques/guide-brand-agent/tree/main/integration/openwebui-rag) |
| **进化 / 对抗留痕** | 按 slot 的 gap、metrics | [content/evolution/](https://github.com/dymusiques/guide-brand-agent/tree/main/content/evolution) |

---

## 3. Personal IP · 构建相关内容（全部入口）

### 3.1 战略与 Owner 材料

| 文件 | 用途 |
|------|------|
| [ip-positioning-brief-2026-10-05.md](https://github.com/dymusiques/guide-brand-agent/blob/main/content/personal-ip/ip-positioning-brief-2026-10-05.md) | IP 一句话、边界、强链接 |
| [2026-10-18-key-person-of-influence-capstone-playbook.md](https://github.com/dymusiques/guide-brand-agent/blob/main/content/personal-ip/2026-10-18-key-person-of-influence-capstone-playbook.md) | KPI / CAPSTONE 对齐 |
| [2026-10-18-danying-capstone-pitch-draft.md](https://github.com/dymusiques/guide-brand-agent/blob/main/content/personal-ip/2026-10-18-danying-capstone-pitch-draft.md) | Pitch 稿 |
| [2026-10-18-capstone-pitch-ip-plus-practice-app.md](https://github.com/dymusiques/guide-brand-agent/blob/main/content/personal-ip/2026-10-18-capstone-pitch-ip-plus-practice-app.md) | Pitch + 产品线 |
| [cv-source-2026-09-15.md](https://github.com/dymusiques/guide-brand-agent/blob/main/content/personal-ip/cv-source-2026-09-15.md) | CV 源 |
| [IP-SUBAGENT-ROSTER.md](https://github.com/dymusiques/guide-brand-agent/blob/main/content/personal-ip/IP-SUBAGENT-ROSTER.md) | IP 子 Agent 编制 |
| [reference/INDEX.md](https://github.com/dymusiques/guide-brand-agent/blob/main/content/personal-ip/reference/INDEX.md) | CAPSTONE 截图 / KPI PDF 索引 |

### 3.2 Intake（CEO / Open WebUI → Cursor 源稿）

| 文件 | 用途 |
|------|------|
| [intake/2026-10-29-ngv-flute-curation-theme.md](https://github.com/dymusiques/guide-brand-agent/blob/main/content/personal-ip/intake/2026-10-29-ngv-flute-curation-theme.md) | NGV×MSO / LinkedIn 口播 intake |
| [intake/2026-10-29-e2e-kpi-longform-source.md](https://github.com/dymusiques/guide-brand-agent/blob/main/content/personal-ip/intake/2026-10-29-e2e-kpi-longform-source.md) | KPI 长文 e2e 源 |

### 3.3 对抗 / 红队（IP 向）

| 文件 | 用途 |
|------|------|
| [2026-10-27-ip-adversarial-red-team.md](https://github.com/dymusiques/guide-brand-agent/blob/main/content/personal-ip/2026-10-27-ip-adversarial-red-team.md) | IP 红队 |
| [2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md](https://github.com/dymusiques/guide-brand-agent/blob/main/content/personal-ip/2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md) | FULL-DRILL 报告 |

### 3.4 01 IP GM · Skill · 脚本

| 文件 | 用途 |
|------|------|
| [agents/01-personal-ip/INTEGRATION-PROMPT.md](https://github.com/dymusiques/guide-brand-agent/blob/main/agents/01-personal-ip/INTEGRATION-PROMPT.md) | 01 部门 Must 读 |
| [integration/agents/a01_personal_ip.py](https://github.com/dymusiques/guide-brand-agent/blob/main/integration/agents/a01_personal_ip.py) | 01 集成胶水 |
| [scripts/evaluate_personal_ip.py](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/evaluate_personal_ip.py) | IP evaluate / `--check` |
| [.cursor/skills/personal-ip/SKILL.md](https://github.com/dymusiques/guide-brand-agent/blob/main/.cursor/skills/personal-ip/SKILL.md) | Cursor Personal IP skill |

### 3.5 层级与 Open WebUI 个人 IP 通道

| 文件 | 用途 |
|------|------|
| [docs/IP-MANAGEMENT-HIERARCHY.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/IP-MANAGEMENT-HIERARCHY.md) | IP / 部门 GM 层级 |
| [docs/OPENWEBUI-CEO-ROUTER.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/OPENWEBUI-CEO-ROUTER.md) | Router · outbox（含 Personal IP 路径） |
| [docs/OPENWEBUI-INTAKE-PROMPT-TEMPLATE.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/OPENWEBUI-INTAKE-PROMPT-TEMPLATE.md) | intake 模板 |

---

## 4. CEO · 派活 · 自动化 Workflow

### 4.1 00 Manager / 一句话触发

| 文件 | 用途 |
|------|------|
| [agents/00-manager/AUTO-WORKFLOW.md](https://github.com/dymusiques/guide-brand-agent/blob/main/agents/00-manager/AUTO-WORKFLOW.md) | CEO 步序（派 GM → gate → 交付） |
| [agents/00-manager/CEO-DISPATCH-SOP.md](https://github.com/dymusiques/guide-brand-agent/blob/main/agents/00-manager/CEO-DISPATCH-SOP.md) | 派活 SOP |
| [docs/CEO-OWNER-ONE-LINE-TRIGGERS.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/CEO-OWNER-ONE-LINE-TRIGGERS.md) | 「CEO 开始执行」等口令 |
| [docs/CEO-FULL-EXECUTION-MANDATE.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/CEO-FULL-EXECUTION-MANDATE.md) | 全量执行 Must |
| [scripts/ceo-full-execution-pipeline.sh](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/ceo-full-execution-pipeline.sh) | 一条命令 CEO 链 |
| [scripts/run_ceo_full_execution.py](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/run_ceo_full_execution.py) | 步骤编排 + manifest |
| [integration/handoff/ceo-full-execution-cycle.json](https://github.com/dymusiques/guide-brand-agent/blob/main/integration/handoff/ceo-full-execution-cycle.json) | 机器可读步骤表 |

### 4.2 派活 · Autopilot · 09→04

| 文件 | 用途 |
|------|------|
| [docs/AUTOPILOT.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/AUTOPILOT.md) | 日常 autopilot |
| [scripts/manager-autopilot.sh](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/manager-autopilot.sh) | 一条命令仪表盘 + 派活块 |
| [agents/09-data-analytics/DATA-NEEDS.md](https://github.com/dymusiques/guide-brand-agent/blob/main/agents/09-data-analytics/DATA-NEEDS.md) | 09 数据 GM |
| [docs/CEO-AGENT-ROSTER-AND-PARALLELISM.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/CEO-AGENT-ROSTER-AND-PARALLELISM.md) | 01–12 谁 invoked |

### 4.3 Workflow L0–L4（自动跑、勿反复问 Owner）

| 文件 | 用途 |
|------|------|
| [docs/WORKFLOW-AUTOMATION-MATRIX.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/WORKFLOW-AUTOMATION-MATRIX.md) | 自动化矩阵说明 |
| [integration/handoff/workflow-automation-manifest.json](https://github.com/dymusiques/guide-brand-agent/blob/main/integration/handoff/workflow-automation-manifest.json) | L0_BOOT … L4_CAMPAIGN |
| [integration/handoff/workflow-automation-catalog-l1.json](https://github.com/dymusiques/guide-brand-agent/blob/main/integration/handoff/workflow-automation-catalog-l1.json) | L1 命令目录 |
| [scripts/run-workflow-from-manifest.py](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/run-workflow-from-manifest.py) | `--phrase "CEO 开始执行"` |

### 4.4 小红书交付链（与 IP 强相关）

| 文件 | 用途 |
|------|------|
| [docs/CEO-XHS-OWNER-DELIVERY-AUTOPILOT.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/CEO-XHS-OWNER-DELIVERY-AUTOPILOT.md) | 进化 + HTML 交付 |
| [docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md) | 对抗 + evolution Must |
| [content/xiaohongshu/OWNER-LONGFORM-XHS-SPEC.md](https://github.com/dymusiques/guide-brand-agent/blob/main/content/xiaohongshu/OWNER-LONGFORM-XHS-SPEC.md) | 长稿规范 |
| [scripts/manager-ceo-xhs-owner-delivery.sh](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/manager-ceo-xhs-owner-delivery.sh) | Owner HTML rebuild |

---

## 5. 测评 · 六项 6-case · Baseline · Evolution · 压测

| 环节 | 文档 | 脚本 |
|------|------|------|
| **成功目标 G-\*** | [integration/GOALS-REGISTRY.md](https://github.com/dymusiques/guide-brand-agent/blob/main/integration/GOALS-REGISTRY.md) · [integration/goals/registry.json](https://github.com/dymusiques/guide-brand-agent/blob/main/integration/goals/registry.json) | [scripts/verify-goals.sh](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/verify-goals.sh) |
| **六项 6-case 矩阵** | [docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/CEO-SIX-CASE-GM-TO-CEO-WORKFLOW.md) | [scripts/ceo-six-case-battery.sh](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/ceo-six-case-battery.sh) |
| **Triple eval + baseline 距离** | [docs/MANAGER-EVAL-IMPROVEMENT-LOOP.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/MANAGER-EVAL-IMPROVEMENT-LOOP.md) · [docs/BRIEF-AUTO-GATE-PIPELINE.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/BRIEF-AUTO-GATE-PIPELINE.md) | [scripts/ceo-triple-eval-baseline-loop.sh](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/ceo-triple-eval-baseline-loop.sh) |
| **Evolution gap / READY** | [docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md) | [scripts/analyze-brief-evolution-gap.py](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/analyze-brief-evolution-gap.py) · [scripts/manager-brief-evolution-until-gap.sh](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/manager-brief-evolution-until-gap.sh) |
| **Double stress** | [docs/OWNER-LONGFORM-CLEVER-ADVOCATE.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/OWNER-LONGFORM-CLEVER-ADVOCATE.md) | [scripts/ceo-double-stress.sh](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/ceo-double-stress.sh) |
| **Autopilot 闭环** | [docs/OWNER-CHAT-DELIVERY-FORMAT.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/OWNER-CHAT-DELIVERY-FORMAT.md) | [scripts/run_ceo_xhs_autopilot.py](https://github.com/dymusiques/guide-brand-agent/blob/main/scripts/run_ceo_xhs_autopilot.py) |

**GM 集成壳（sub-agent manager 胶水）：** [integration/agents/](https://github.com/dymusiques/guide-brand-agent/tree/main/integration/agents)（`a00_manager.py` … `a09_analytics.py`）

---

## 6. CEO / GM 接手包（鸭哥若要改 SOP）

| 文件 | 链接 |
|------|------|
| CEO/GM SOP Pack | [docs/HANDOFF-CEO-GM-SOP-PACK.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/HANDOFF-CEO-GM-SOP-PACK.md) |
| Operating manifest | [integration/handoff/ceo-gm-operating-manifest.json](https://github.com/dymusiques/guide-brand-agent/blob/main/integration/handoff/ceo-gm-operating-manifest.json) |
| 三支柱 / 标准 | [docs/MANAGER-THREE-PILLARS.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/MANAGER-THREE-PILLARS.md) · [docs/CEO-MANAGER-OPERATING-STANDARDS.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/CEO-MANAGER-OPERATING-STANDARDS.md) |
| 双轮迭代 | [agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md](https://github.com/dymusiques/guide-brand-agent/blob/main/agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md) |
| Workflow 思维导图（部门向） | [docs/workflow-handoff-mindmap.html](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/workflow-handoff-mindmap.html) |

---

## 7. Open WebUI · 上下文（辅助 Personal IP，非 Git 定稿）

| 文件 | 链接 |
|------|------|
| RAG 脚本说明 | [integration/openwebui-rag/README.md](https://github.com/dymusiques/guide-brand-agent/blob/main/integration/openwebui-rag/README.md) |
| L0/L1/L2 标准 | [docs/PROMPT-CONTEXT-STANDARD.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/PROMPT-CONTEXT-STANDARD.md) · [docs/CONTEXT-WINDOW-AND-DATA-ROUTING.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/CONTEXT-WINDOW-AND-DATA-ROUTING.md) |
| Handoff 快照 | [integration/handoff/openwebui-context-reorg-latest.json](https://github.com/dymusiques/guide-brand-agent/blob/main/integration/handoff/openwebui-context-reorg-latest.json) |

定稿与测评在 **Cursor + 本仓 scripts**；Open WebUI 负责本机 RAG（含 Drive 背书库 `brand-ip-knowledge`）。

---

## 8. 鸭哥若要直接改：推荐方式

1. **Comment / Issue：** 在任意 MD 文件页 · **Add file comment** 或开 Issue 链到路径。  
2. **Pull Request：** Fork 不可用（私有仓）→ 需 **Write** 权限开分支 PR，或由 Owner 开 branch 给鸭哥 push。  
3. **优先改哪些：** Personal IP 看 §3；CEO 派活与 workflow 看 §4–§5；集成边界看 [integration/IMPORTANT.md](https://github.com/dymusiques/guide-brand-agent/blob/main/integration/IMPORTANT.md)。

---

## 9. Owner 本地命令（鸭哥可不跑）

```bash
git clone git@github.com:dymusiques/guide-brand-agent.git   # 需 Collaborator
bash scripts/verify-handoff.sh
bash scripts/ceo-full-execution-pipeline.sh --goal "<Owner 原话>"
```

---

*文档路径：`docs/YAGE-PERSONAL-IP-CEO-REVIEW-GUIDE.md` · 与 [SHARE-FOR-鸭哥.md](https://github.com/dymusiques/guide-brand-agent/blob/main/docs/SHARE-FOR-%E9%B8%AD%E5%93%A5.md) 互补：本文为 **GitHub 全链接索引**，后者为 **公开 Gist 入口说明**。*
