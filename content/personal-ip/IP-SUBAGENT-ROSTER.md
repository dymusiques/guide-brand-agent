---
context_version: "2026-10-30-l012"
repo_path: "content/personal-ip/IP-SUBAGENT-ROSTER.md"
goal: "IP 打造 · Sub-Agent 岗位表（与 00 CEO 编制）"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "b1b4652cbe5e75ae"
---

# IP 打造 · Sub-Agent 岗位表（与 00 CEO 编制）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** - **日常 IP 打造：** 只有 **1 个 Cursor 对话 + 00 CEO**，里面 **轮流扮演 01–09**（顺序见 AUTO-WORKFLOW）。  
- **Sub-Agent：** 指的就是这 **9 个职能岗位**；不是 9 个自动运行的机器人。  
- **要「全员动起来」：** 说「按 IP-SUBAGENT-ROSTER 轮询
- **Path:** `content/personal-ip/IP-SUBAGENT-ROSTER.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **L1 任务（压缩 · Open WebUI / Cursor 顶栏）**: - **Goal:** > **直接回答：** 本仓 **没有** 在后台常驻、自动并行跑 IP 的「Sub-Agent 进程」。
- **章节锚点**: - **组织图（IP 打造）**: ```text
- **Owner 一句话**: - **日常 IP 打造：** 只有 **1 个 Cursor 对话 + 00 CEO**，里面 **轮流扮演 01–09**（顺序见 AUTO-WORKFLOW）。


---

## L2 正文

# IP 打造 · Sub-Agent 岗位表（与 00 CEO 编制）

> **直接回答：** 本仓 **没有** 在后台常驻、自动并行跑 IP 的「Sub-Agent 进程」。  
> **有** 两类东西容易混叫 Sub-Agent，下面分开写清。


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


## Cursor Task Sub-Agent（B 类 · 按需临时工）

| Task 类型 | 建议谁（CEO）派给 | 可做什么 | **禁止** |
|-----------|-------------------|----------|----------|
| `explore` | 00 → 任意板块查仓 | 快搜路径、INTEGRATION-PROMPT、历史 Brief | 写定稿 Brief |
| `generalPurpose` | 00 → 01/02/03 调研 | 红队、行业坑、竞品一句 | 代替 04 写口播 |
| `bugbot` / `security-review` | 00（Owner 明确要求） | 改 scripts/verify 后的 review | 改 kernel 规则 |
| `ci-investigator` | 00 | CI 失败摘要 | 内容 IP |

**落盘：** `tmp/parallel/<session>/` · 定稿仍 **04 单线程** → evaluate → 06。


## 和「红队文档」的关系

[2026-10-27-ip-adversarial-red-team.md](./2026-10-27-ip-adversarial-red-team.md) · **[FULL-DRILL-REPORT](./2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md)**（CEO+Evaluator+9 GM 评分）= 职能 Sub-Agent **对抗演练**；可用 **B 类 Task** 并行加深 02/03/09，但 **不** 增加新编制岗位。

---

## Owner 一句话

- **日常 IP 打造：** 只有 **1 个 Cursor 对话 + 00 CEO**，里面 **轮流扮演 01–09**（顺序见 AUTO-WORKFLOW）。  
- **Sub-Agent：** 指的就是这 **9 个职能岗位**；不是 9 个自动运行的机器人。  
- **要「全员动起来」：** 说「按 IP-SUBAGENT-ROSTER 轮询派活」或「跑红队 §F」— CEO 按表让每个岗位出一段产出或攻击，再进 04 写稿。