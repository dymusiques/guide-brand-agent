---
context_version: "2026-10-30-l012"
repo_path: "docs/HANDOFF-CEO-GM-SOP-PACK.md"
goal: "接手包 · CEO / GM 运营体系（2026-10-28）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "1f9805d88d616828"
---

# 接手包 · CEO / GM 运营体系（2026-10-28）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **给谁：** 新 Cursor Agent、换机后的第一次会话、Owner 要确认「是不是都写进程序了」。  
> **机器可读索引：** [integration/handoff/ceo-gm-operating-manifest.json](../integration/handoff/ceo-gm-operating-manifest.json)
- **Path:** `docs/HANDOFF-CEO-GM-SOP-PACK.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **2. 框架与 SOP 文件清单（Must 知道）**
- **4. 新 Agent 接手后第一次 Owner 交互**: Owner 说：**「请 CEO 开始工作」** → Agent Must：
- **6. 相关**: - [HANDOFF-COMPLETENESS.md](./HANDOFF-COMPLETENESS.md) · [SETUP.md](../SETUP.md) · [rules/WORKSPACE.…


---

## L2 正文

# 接手包 · CEO / GM 运营体系（2026-10-28）

> **给谁：** 新 Cursor Agent、换机后的第一次会话、Owner 要确认「是不是都写进程序了」。  
> **机器可读索引：** [integration/handoff/ceo-gm-operating-manifest.json](../integration/handoff/ceo-gm-operating-manifest.json)  
> **新机口令：** 在 chat 说 **`danying-brand-agent`** 或 **`请 CEO 开始工作`**（见 [CEO-OWNER-ONE-LINE-TRIGGERS.md](./CEO-OWNER-ONE-LINE-TRIGGERS.md)）。


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
| [OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](./OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md) | **Owner 固定** · 搜坑 · L2–L3 对抗 · 多轮 gap 直到 READY |
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
| `scripts/manager-brief-evolution-until-gap.sh` | 单篇进化直到 EVOLUTION-GAP READY |
| `scripts/analyze-brief-evolution-gap.py` | 轮间差距 · baseline / gold |

**勿混淆：** `CEO_DEEP_ROUNDS=2` ≠ CEO 双轮 prompt 迭代；gate 默认 3 轮 ≠ 两次「改 prompt 迭代」。


## 4. 新 Agent 接手后第一次 Owner 交互

Owner 说：**「请 CEO 开始工作」** → Agent Must：

1. `ceo-auto-recover-blocked.sh`  
2. 读最新 `content/evolution/00-manager/ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-*.md`  
3. 执行下一项（campaign / 双轮 Brief / 深交付 / 刷新 HTML）  
4. 输出 **Manager 派活记录**（Owner Gate · 打回轮次 · 是否交 Owner）


## 6. 相关

- [HANDOFF-COMPLETENESS.md](./HANDOFF-COMPLETENESS.md) · [SETUP.md](../SETUP.md) · [rules/WORKSPACE.md](../rules/WORKSPACE.md)（全路径索引）