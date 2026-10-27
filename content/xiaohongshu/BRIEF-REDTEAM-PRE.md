# Brief 前红队 · 2 条/篇（Owner 固定 · 2026-10-27）

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
