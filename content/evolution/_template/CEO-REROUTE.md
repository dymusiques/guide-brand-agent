---
context_version: "2026-10-30-l012"
repo_path: "content/evolution/_template/CEO-REROUTE.md"
goal: "CEO-REROUTE · <部门名> · <slug>"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "827b55deac624025"
---

# CEO-REROUTE · <部门名> · <slug>

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** - 来自：00 CEO
- 日期：
- 打回轮次：n / 3（默认上限见 [CEO-AUTO-QA-LOOP.md](../../../docs/CEO-AUTO-QA-LOOP.md)）
- **Path:** `content/evolution/_template/CEO-REROUTE.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`

## 章节锚点
- **失败摘要（Gate / evaluate / verify）**: - 命令：
- **Prompt Change 提案（GM/AI 必填 · 改稿前填写）**: - 改什么：（文件路径 + 段落）
- **GM Must 做**: 1. 读上表失败原因 + 完成 **提案** + 当前 `versions/vN.md`
- **CEO 备注（集成/Brief/Skill 倾向，不改 kernel 除非 05 专项）**: -


---

## L2 正文

# CEO-REROUTE · <部门名> · <slug>

- 来自：00 CEO
- 日期：
- 打回轮次：n / 3（默认上限见 [CEO-AUTO-QA-LOOP.md](../../../docs/CEO-AUTO-QA-LOOP.md)）

## 失败摘要（Gate / evaluate / verify）

- 命令：
- 终端 excerpt：（粘贴关键 FAIL 行）

## Prompt Change 提案（GM/AI 必填 · 改稿前填写）

- 改什么：（文件路径 + 段落）
- 一句 diff：
- 依据（Gate / verify-logs）：
- 预期哪条 gate 变绿：
- 风险：

## GM Must 做

1. 读上表失败原因 + 完成 **提案** + 当前 `versions/vN.md`
2. 出 **v(N+1)**（或 Brief 补丁），**禁止**把同一 FAIL 稿再标「请 Owner 验证」
3. 重跑：

```bash
# CEO 指定（示例）
bash scripts/manager-ceo-owner-gate.sh --brief content/xiaohongshu/<file>.md
```

4. 更新 **GM-REPORT.md**，请求 CEO 复 gate

## CEO 备注（集成/Brief/Skill 倾向，不改 kernel 除非 05 专项）

-