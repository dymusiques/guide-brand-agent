---
context_version: "2026-10-30-l012"
repo_path: "content/xiaohongshu/BRIEF-REDTEAM-PRE.md"
goal: "Brief 前红队 · 2 条/篇（Owner 固定 · 2026-10-27）"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "6f88ba45fd00cf69"
---

# Brief 前红队 · 2 条/篇（Owner 固定 · 2026-10-27）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **给 Owner 一句话：`redteam-pre` 是什么？**  
> 写 Brief **之前**，Agent 内部用 [X1–X12 错误库](../personal-ip/2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md) 挑 **2 条最相关攻击**（如：像硬广、像教学号、同质化），写清 **怎么
- **Path:** `content/xiaohongshu/BRIEF-REDTEAM-PRE.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **谁做**: | 角色 | 动作 |
- **菜单**: - **X1–X12：** [2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md §2](../personal-ip/2026-10-27-ip-adver…
- **前置（Must · 2026-10-28）**: - 先完成 [BRIEF-PITFALLS-RESEARCH-SOP.md](./BRIEF-PITFALLS-RESEARCH-SOP.md) → `research/<slug>-pitfalls…
- **落盘（Must）**: 路径：`content/xiaohongshu/redteam/<YYYY-MM-DD-slug>-pre.md`
- **指挥链位置**: [AUTO-WORKFLOW.md](../../agents/00-manager/AUTO-WORKFLOW.md) **步 1c** → 步 2 写 Brief → 步 3 evaluate →…


---

## L2 正文

# Brief 前红队 · 2 条/篇（Owner 固定 · 2026-10-27）

> **给 Owner 一句话：`redteam-pre` 是什么？**  
> 写 Brief **之前**，Agent 内部用 [X1–X12 错误库](../personal-ip/2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md) 挑 **2 条最相关攻击**（如：像硬广、像教学号、同质化），写清 **怎么改方向**；落盘 `redteam/<日期-slug>-pre.md`。  
> **你不用看红队稿**；完整交稿前 Agent 必须 **每篇都有这个文件**，并跑 `evaluate-xhs-brief-complete.py`（6 项 L1 + Gemini evaluate）。

> **Owner 确认：** **要固定** — 每篇小红书 Brief **动笔前**，Agent **内部** 做红队 2 条；Owner 无需选 X 编号、无需审红队稿。

## 谁做

| 角色 | 动作 |
|------|------|
| **00 CEO** | 派 04 slug；指定本篇最相关的 2 条攻击来源（X1–X12 / §D） |
| **04 GM** | 写 2 条攻击 + 各 1 句驳/改方向（可顺带 01/09 视角） |
| **Owner** | 无；只看 **红队后的 Brief**（仍走 CEO Gate） |

## 菜单

- **X1–X12：** [2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md §2](../personal-ip/2026-10-27-ip-adversarial-FULL-DRILL-REPORT.md#2--高挑战错误库本轮新增--含外部调研)  
- **§D 分岗表：** [2026-10-27-ip-adversarial-red-team.md §D](../personal-ip/2026-10-27-ip-adversarial-red-team.md#d-分-agent-红队攻击每个-agent动起来干什么)

**选条原则：** 与 **本篇选题/受众/CTA** 最相关；至少 1 条偏 **L2–L3**（非纯禁词）。

## 前置（Must · 2026-10-28）

- 先完成 [BRIEF-PITFALLS-RESEARCH-SOP.md](./BRIEF-PITFALLS-RESEARCH-SOP.md) → `research/<slug>-pitfalls.md`  
- 总纲：[OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md](../../docs/OWNER-XHS-ADVERSARIAL-AND-EVOLUTION-MANDATE.md)

## 落盘（Must）

路径：`content/xiaohongshu/redteam/<YYYY-MM-DD-slug>-pre.md`

```markdown
# Redteam pre · <slug>
- 攻击 1：（来源 X? / §D·04）
- 驳/改：
- 攻击 2：（来源 …）
- 驳/改：
- CEO：允许写 Brief / 需改选题（一句）
```

无此文件 **不得** 新建对应 `*-brief.md`（CEO 门控）。

## 指挥链位置

[AUTO-WORKFLOW.md](../../agents/00-manager/AUTO-WORKFLOW.md) **步 1c** → 步 2 写 Brief → 步 3 evaluate → Owner Gate。