---
context_version: "2026-10-30-l012"
repo_path: "docs/CEO-OWNER-DEADLINE-DELIVERY.md"
goal: "CEO · Owner 截止交付（24:00 北京时间）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "90a927a4708ad12e"
---

# CEO · Owner 截止交付（24:00 北京时间）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Owner 意图：** 只对 CEO 说一次目标 → 各 GM 被派活 → **持续收集** → **多轮**筛选与测试 → **24:00 前** HTML/邮件交付。  
> **不是** 5 分钟跑一条 shell 就称「认真筛选」。
- **Path:** `docs/CEO-OWNER-DEADLINE-DELIVERY.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **你对 CEO 说什么（示例）**: 口语即可，例如：
- **深交付 vs 应付式 batch**: | | 应付式（旧） | 深交付（Must） |
- **一条命令（Owner 或 Agent 跑）**: ```bash
- **怎么「测试」整个机制**: 1. **干跑计时：** 看 log 是否含 `C1` `D1` `E1` `C2`… 多阶段时间戳。
- **能力边界（诚实）**: | 能自动 | 不能自动（除非另开 Cursor 会话/Task） |
- **相关**: - [BRIEF-AUTO-GATE-PIPELINE.md](./BRIEF-AUTO-GATE-PIPELINE.md)


---

## L2 正文

# CEO · Owner 截止交付（24:00 北京时间）

> **Owner 意图：** 只对 CEO 说一次目标 → 各 GM 被派活 → **持续收集** → **多轮**筛选与测试 → **24:00 前** HTML/邮件交付。  
> **不是** 5 分钟跑一条 shell 就称「认真筛选」。

## 你对 CEO 说什么（示例）

口语即可，例如：

「今晚 12 点前把小红书认知期队列 + Artist 四指标 + Discovery 对抗复查交给我；要深筛，不要应付。」

CEO **Must**（Cursor 规则 + 本脚本）：

1. 读 [AUTO-WORKFLOW.md](../agents/00-manager/AUTO-WORKFLOW.md) 派 01/04/09/10…  
2. **启动深交付循环**（见下），不是只跑旧的轻量 batch。  
3. FAIL → GM 改稿 → 再测（≤ `CEO_GATE_MAX_ROUNDS`），**不问 Owner「要不要 evaluate」**。

## 深交付 vs 应付式 batch

| | 应付式（旧） | 深交付（Must） |
|---|-------------|----------------|
| 命令 | 仅 `ceo-xhs-ip-filter-batch.py` | **`run-ceo-deep-delivery-cycle.sh`** |
| 轮次 | 1 次汇总 | **默认 2 轮**：pipeline → gate loop → 刷新 adversarial → 再 pipeline |
| 测试 | 可能只 gate 1 篇 | **全 Brief** redteam + adversarial + L1×6 + evaluate + kernel 6 |
| 时长 | ~5–15 分钟 | **约 30–90+ 分钟**（Gemini 次数多） |
| 交付 | MD | **HTML** + Gmail + `ceo-deep-delivery-*.md` 报告 |

## 一条命令（Owner 或 Agent 跑）

```bash
# 默认 2 轮深循环 · 每篇最多 3 轮 gate
bash scripts/run-ceo-deep-delivery-cycle.sh

# 更重：3 轮深循环
CEO_DEEP_ROUNDS=3 bash scripts/run-ceo-deep-delivery-cycle.sh
```

等价于旧 overnight 入口（已升级）：

```bash
bash scripts/run-ceo-xhs-filter-batch.sh
```

## 怎么「测试」整个机制

1. **干跑计时：** 看 log 是否含 `C1` `D1` `E1` `C2`… 多阶段时间戳。  
2. **产物：**  
   - `content/xiaohongshu/challenge/*-challenge.md`（6 篇）  
   - `content/xiaohongshu/verify-logs/*-complete-*.json`（每 Brief 至少 2 轮深循环时多次）  
   - `ceo-inbox/ceo-deep-delivery-*.md`  
3. **Owner 打开：** `OPEN-OWNER-REPORT-IN-BROWSER.command` 或 HTML 双击。

## 能力边界（诚实）

| 能自动 | 不能自动（除非另开 Cursor 会话/Task） |
|--------|----------------------------------------|
| 脚本链多轮测试 + 写 REROUTE | **并行** 9 个真实独立 subagent 进程 24h 盯盘 |
| 后台 **daily 09:00** cycle | 你 **没启动脚本** 时，不会 magically 在 23:59 交稿 |
| Cursor **单会话 CEO 顺序扮演** GM | 替 Owner **小红书发帖** |

**要对 CEO「说一声」并交付 tonight：** 在同一会话让 Agent **执行** `run-ceo-deep-delivery-cycle.sh`（或后台 `nohup`），不是只聊天不跑终端。

## 相关

- [BRIEF-AUTO-GATE-PIPELINE.md](./BRIEF-AUTO-GATE-PIPELINE.md)  
- [BRIEF-ADVERSARIAL-CHALLENGE.md](../agents/_shared/BRIEF-ADVERSARIAL-CHALLENGE.md)