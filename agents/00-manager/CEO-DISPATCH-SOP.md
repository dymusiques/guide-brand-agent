# CEO 派活 SOP · 模板

> 原则来源：[docs/CEO-MANAGER-OPERATING-STANDARDS.md](../../docs/CEO-MANAGER-OPERATING-STANDARDS.md)（Owner 五原则）。  
> 流程：Owner 口语目标 → **先落盘 dispatch（本模板）** → 派活 → 验收 → 记录。  
> 示范：`content/evolution/00-manager/ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-2026-10-27-evening.md`  
> GM 评估改进环（Owner 图 ↔ 01–12 对照）：[docs/MANAGER-EVAL-IMPROVEMENT-LOOP.md](../../docs/MANAGER-EVAL-IMPROVEMENT-LOOP.md)  
> CEO 环 · 两轮串行迭代（consult SOP → … → analyze）：[CEO-DOUBLE-ITERATION-SOP.md](CEO-DOUBLE-ITERATION-SOP.md) · [docs/CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md](../../docs/CEO-SENIOR-MANAGER-IMPROVEMENT-LOOP.md)

## 0. 使用步骤

**Owner 不必每次贴终端命令：** 在 Cursor 说「请 CEO 开始工作」即可 → 见 [CEO-OWNER-ONE-LINE-TRIGGERS.md](../../docs/CEO-OWNER-ONE-LINE-TRIGGERS.md) · 可选 `bash scripts/ceo-start-work.sh` 看状态。

1. 复制下方模板到 `content/evolution/00-manager/ceo-inbox/CEO-IP-ALL-AGENTS-DISPATCH-<YYYY-MM-DD>[-tag].md`
2. 填 North star / 战役题 / per-agent 表（**每行必须有终端验收命令**）
3. 全员派活 → `VERIFY_GOALS_SKIP_PLATFORM=0 bash scripts/run-ceo-ip-all-agents-campaign.sh`（截止交付另加 `run-ceo-deep-delivery-cycle.sh`；二者并行时用 lock / `SKIP_GEMINI`）
4. 收尾回填「结果」与 **Manager 派活记录**
5. 新增文档/脚本 → 更新 `rules/WORKSPACE.md` 索引

---

## 模板

```markdown
# CEO · 全员派活（<战役名>）· <一句话主题>

**签发：** <日期时间>（北京）· 00 Manager 代 CEO
**战役题目：** 「<主题>」
**Owner 原话：** 「<原话摘要，勿改写>」
**North star：** <例：打造 Danying 个人 IP —— 长笛/教育/咨询；Discovery + Artist Watchlist + 听见 Daily 同一叙事轴；每 Agent 产出可验收结果>
**截止 / 时间盒：** <例：今晚 24:00 前交 HTML + 报告>
**G-* 绑定：** G-STRONG-LINK · G-NOT-SINGLE-VERTICAL-LOCK · G-BRIEF-ALIGNED-GATE · G-ANALYTICS-EVIDENCE（按需增减）
**红线：** 先观点后产品 · 不单品类绑定 · 不编造数据（无 CSV 标「未验证」）· 发布/私信/Drive 仅 Owner 授权

## 叙事轴（可选三段）
| 段 | 0–30 天 | 31–60 天 | 61–90 天 |
|----|---------|----------|----------|

## Per-agent 任务与验收
| Agent | 任务（一句话，可交付） | 验收（终端命令） | 交付物路径 |
|-------|------------------------|------------------|------------|
| 00 Manager | 派活记录 · auto-gate · 收汇报 | `manager-dashboard.sh` · `manager-workflow-verify.sh` | |
| 01 personal-ip | | `agent-shells/01-personal-ip.sh --check` · `verify-agent-fused --agent 01` | |
| 02 business-brand | | `02-business-brand.sh` · `fused 02` | |
| 03 marketing | | `03-marketing.sh` · `fused 03` | |
| 04 xhs topic | | `fused 04` · `manager-ceo-auto-gate-loop.sh --brief …` | |
| 05 xhs growth | （kernel 不改） | `05-xhs-kernel.sh` · `fused 05` | |
| 06 pipeline | | `06-xhs-pipeline.sh` · `verify-xhs-content-dir.sh` | |
| 07 brand visual | | `07-brand-visual.sh --check` · `fused 07` | |
| 08 platform | | `08-platform.sh` · `fused 08` | |
| 09 analytics | | `09-analytics.sh` · `fused 09` | |
| 10 artist-benchmark | | `fused 10 --with-artifacts` | |
| 11 ip-daily-evaluator | | `fused 11 --with-artifacts` | |
| 12 owner-daily-brief | Owner 一页汇总（07 语气） | `fused 12 --with-artifacts` | |

## 验收标准（交 Owner 的门槛）
- [ ] Campaign `RESULT: PASS` · failures 0
- [ ] 涉及 Brief：`manager-ceo-auto-gate-loop.sh --brief …` PASS（≤3 轮）→ `manager-ceo-owner-gate.sh --brief …` PASS
- [ ] 数据类结论有来源，无来源标「未验证」
- [ ] 报告/日志含 PASS 标记（半截日志不算交付）

## Manager 派活记录（执行后回填）
（字段见下「派活记录字段」）

## 结果
（时间 · 命令 · 矩阵 · 事故 · 未做项）
```

---

## Manager 派活记录 · 字段（每轮 Must 输出）

```markdown
## Manager 派活记录
- 目标：（Owner 原话摘要）
- North star：（例：打造个人 IP）
- 当前步：0x · Agent 名称
- 终端：PASS/FAIL + 命令（含 failures 数 / PASS 篇数）
- Owner Gate：PASS/FAIL · 打回轮次 n/3 · 交 Owner：是/否（若是，限：<发布裁决/发帖/CSV…>）
- 报告 / 日志：路径
- 新增资产：路径（文档/脚本/规则/索引）
- 未做：（未 commit / 未 sync Drive / 未发帖 / 数据未验证…）
- 下一步：…
```

## Auto-gate / Recover 指针

| 情形 | 动作 | 文档 |
|------|------|------|
| CEO 派活或改 Brief 后 | 全仓 `bash scripts/manager-xhs-briefs-auto-pipeline.sh`；单篇 `manager-ceo-auto-gate-loop.sh --brief …` | [BRIEF-AUTO-GATE-PIPELINE](../../docs/BRIEF-AUTO-GATE-PIPELINE.md) · [BRIEF-ADVERSARIAL-CHALLENGE](../_shared/BRIEF-ADVERSARIAL-CHALLENGE.md) |
| 交 Owner 前 | `bash scripts/manager-ceo-owner-gate.sh --brief …` | [CEO-AUTO-QA-LOOP](../../docs/CEO-AUTO-QA-LOOP.md) |
| Gate FAIL | 写 `CEO-REROUTE` → GM 同会话改 v(N+1) → 再 gate（≤3 轮）；**不**把 FAIL 稿交 Owner | 同上 |
| 截止交付 | `bash scripts/run-ceo-deep-delivery-cycle.sh`（禁止仅跑 `ceo-xhs-ip-filter-batch.py`） | [CEO-OWNER-DEADLINE-DELIVERY](../../docs/CEO-OWNER-DEADLINE-DELIVERY.md) |
| 中断 / 阻塞 / FAIL / 跑错 | **自动** `bash scripts/ceo-auto-recover-blocked.sh` → 读 `ceo-inbox/ceo-auto-recover-latest.md` → 按需 nohup 重跑；**勿问 Owner 要不要重跑** | [CEO-AUTO-RECOVER-AND-RETRY](../../docs/CEO-AUTO-RECOVER-AND-RETRY.md) |
| 交班 / 大改后 | `bash scripts/verify-handoff.sh` | [AGENT-TAKEOVER](../../docs/AGENT-TAKEOVER.md) |
