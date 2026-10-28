# 接手包 · CEO / GM 运营体系（2026-10-28）

> **给谁：** 新 Cursor Agent、换机后的第一次会话、Owner 要确认「是不是都写进程序了」。  
> **机器可读索引：** [integration/handoff/ceo-gm-operating-manifest.json](../integration/handoff/ceo-gm-operating-manifest.json)  
> **新机口令：** 在 chat 说 **`danying-brand-agent`** 或 **`请 CEO 开始工作`**（见 [CEO-OWNER-ONE-LINE-TRIGGERS.md](./CEO-OWNER-ONE-LINE-TRIGGERS.md)）。

---

## 1. Owner 确认：是不是都写进「程序」了？

**是 — 在 Git 仓库里分三层：**

| 层 | 是什么 | 你/新 Agent 怎么用 |
|----|--------|-------------------|
| **规则（自动生效）** | `.cursor/rules/danying-manager-auto.mdc` 等 | 打开本仓即加载；Owner 给目标 → **00 Manager 自动接手**，不必贴 bash |
| **SOP / 文档** | 下文 §2 清单 | 新 Agent **按读序读一遍**；日常查路径 |
| **脚本（可执行）** | `scripts/*.sh` · `scripts/*.py` | Agent **Must 自己跑**；Owner 只说「CEO 开始工作」即可 |

**不在 Git 的（需 Owner 本机一次）：** Google OAuth（`vendor/gdocs-skill/secrets/`）、Cursor **Customize → MCPs** Connect、Gemini API key（`.env`）。见 [SETUP.md](../SETUP.md)。

---

## 2. 框架与 SOP 文件清单（Must 知道）

### 2.1 Owner 目标与原则

| 文件 | 内容 |
|------|------|
| [CEO-MANAGER-OPERATING-STANDARDS.md](./CEO-MANAGER-OPERATING-STANDARDS.md) | Owner **五原则**（委派 · 可衡量 · 数据驱动 · 教练 · 资产化） |
| [CEO-MANAGER-OPERATING-PRINCIPLES.md](./CEO-MANAGER-OPERATING-PRINCIPLES.md) | 五原则 → **脚本映射** · 晚间 8 步 |
| [MANAGER-THREE-PILLARS.md](./MANAGER-THREE-PILLARS.md) | 每个 GM 真正做的 **三支柱**（主框架） |

### 2.2 两张流程图（GM vs CEO）

| 角色 | 图 | 文档 |
|------|-----|------|
| **每个 Manager (01–12)** | `docs/assets/manager-eval-improvement-loop.png` | [MANAGER-EVAL-IMPROVEMENT-LOOP.md](./MANAGER-EVAL-IMPROVEMENT-LOOP.md) |
| **Senior Manager / CEO** | `docs/assets/ceo-senior-manager-improvement-loop.png` | [CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md](./CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md) |

### 2.3 CEO 执行 SOP（派活 · 双轮 · 一句话触发）

| 文件 | 内容 |
|------|------|
| [agents/00-manager/AUTO-WORKFLOW.md](../agents/00-manager/AUTO-WORKFLOW.md) | CEO **自动接手** · Manager's Loop · auto-gate Must |
| [agents/00-manager/CEO-DISPATCH-SOP.md](../agents/00-manager/CEO-DISPATCH-SOP.md) | **派活模板** · dispatch · campaign |
| [agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md](../agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md) | **consult SOP** · 迭代1 → analyze → 迭代2 |
| [CEO-OWNER-ONE-LINE-TRIGGERS.md](./CEO-OWNER-ONE-LINE-TRIGGERS.md) | Owner **不必贴命令** |
| [CEO-AUTO-RECOVER-AND-RETRY.md](./CEO-AUTO-RECOVER-AND-RETRY.md) | 中断/FAIL **自动 recover** |
| [BRIEF-AUTO-GATE-PIPELINE.md](./BRIEF-AUTO-GATE-PIPELINE.md) | evaluate / adversarial / 6-test **无人值守** |
| [CEO-OWNER-DEADLINE-DELIVERY.md](./CEO-OWNER-DEADLINE-DELIVERY.md) | 截止 **深交付** |

### 2.4 关键脚本（Agent 跑，Owner 不背）

| 脚本 | 何时 |
|------|------|
| `scripts/ceo-auto-recover-blocked.sh` | CEO 开始 / 阻塞 / FAIL |
| `scripts/ceo-start-work.sh` | 终端只看状态（可选） |
| `scripts/manager-ceo-double-iteration.sh --phase 1\|2` | CEO 双轮改 Brief |
| `scripts/verify-ceo-iteration-log.py` | phase 2 前校验 ITERATION-LOG |
| `scripts/manager-ceo-auto-gate-loop.sh --max-rounds 1` | 单轮 gate（双轮内） |
| `scripts/run-ceo-ip-all-agents-campaign.sh` | 01–12 全员 |
| `scripts/run-ceo-deep-delivery-cycle.sh` | 深交付截止 |
| `scripts/manager-xhs-briefs-auto-pipeline.sh` | 全 Brief 管线 |

**勿混淆：** `CEO_DEEP_ROUNDS=2` ≠ CEO 双轮 prompt 迭代；gate 默认 3 轮 ≠ 两次「改 prompt 迭代」。

---

## 3. 新 Agent / 新机 · 10 分钟读序

1. 本文（你正在读）  
2. [HANDOFF-MD-MANIFEST.md](./HANDOFF-MD-MANIFEST.md) 全文表  
3. [AGENT-TAKEOVER.md](./AGENT-TAKEOVER.md) · [integration/IMPORTANT.md](../integration/IMPORTANT.md)  
4. [MANAGER-THREE-PILLARS.md](./MANAGER-THREE-PILLARS.md) → [CEO-DOUBLE-ITERATION-SOP.md](../agents/00-manager/CEO-DOUBLE-ITERATION-SOP.md)  
5. `integration/handoff/ceo-gm-operating-manifest.json`（路由用）

**命令：**

```bash
bash scripts/ensure-venv-deps.sh
bash scripts/verify-handoff.sh
bash scripts/manager-autopilot.sh
```

有 OAuth：`bash scripts/verify-integration.sh` · `VERIFY_GOALS_SKIP_PLATFORM=0 bash scripts/verify-goals.sh`

---

## 4. 新 Agent 接手后第一次 Owner 交互

Owner 说：**「请 CEO 开始工作」** → Agent Must：

1. `ceo-auto-recover-blocked.sh`  
2. 读最新 `content/evolution/00-manager/ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-*.md`  
3. 执行下一项（campaign / 双轮 Brief / 深交付 / 刷新 HTML）  
4. 输出 **Manager 派活记录**（Owner Gate · 打回轮次 · 是否交 Owner）

---

## 5. 模板与产物路径（改稿时）

| 产物 | 路径 |
|------|------|
| ITERATION-LOG | `content/evolution/04-xhs-topic-manager/<slug>/ITERATION-LOG.md` |
| CEO-REROUTE | `content/evolution/04-xhs-topic-manager/<slug>/CEO-REROUTE.md`（含 **Prompt Change 提案**） |
| GM-REPORT | 同目录或 `content/evolution/<dept>/…/GM-REPORT.md`（含 **本轮分析结论**） |
| 派活 / 报告 | `content/evolution/00-manager/ceo-inbox/` |
| Owner HTML | `ceo-inbox/OWNER-XHS-FILTER-DELIVERABLE-<date>.html` |

模板：`content/evolution/_template/CEO-REROUTE.md` · `GM-REPORT.md`

---

## 6. 相关

- [HANDOFF-COMPLETENESS.md](./HANDOFF-COMPLETENESS.md) · [SETUP.md](../SETUP.md) · [rules/WORKSPACE.md](../rules/WORKSPACE.md)（全路径索引）
