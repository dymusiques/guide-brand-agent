---
context_version: "2026-11-01-agent-drive"
repo_path: "docs/AGENT-DRIVE-CONTEXT-EXTERNALIZATION.md"
goal: "新 Agent Must：Drive 与上下文外置 · 动机 + 三层管理"
openwebui_route: "rag_l1"
cursor_route: "read"
---

# 新 Agent Must · Drive 与上下文外置

> **动机（保留 · 全仓 Must）：**  
> **不能让越来越长的 chat，或整片 Google Drive，直接变成定稿 prompt。**  
> 必须先 **压缩、分层、外置到 Git 文件**，再让 CEO / 新 Agent 接手。  
> Chat 与 RAG 都是**辅助**；**真相与约束在仓库里的 MD / JSON / intake。**

---

## 1. 你为什么会在 Cursor 里「丢重点、犯懒」

- 单会话 context 有限；越长越容易概括过度、漏 Owner 约束。  
- **Open WebUI 里的模型也会同样犯懒**——「先 WebUI 提炼再喂 Cursor」**不保证**更准，除非提炼结果是**可验收的文件**。  
- **海量 Drive** 不能指望「读完再懂」；必须 **搜索 → 精读少量 → 写进 intake**。

新 Agent：**默认 chat 要短**；材料用 **`@file` / 路径** 读 L1 与 intake，不复制整段历史对话。

---

## 2. Google Drive 三层（管理规则）

| 层 | 名称 | 放什么 | Agent 怎么用 | 是否全量 sync 到 Open WebUI |
|----|------|--------|--------------|----------------------------|
| **T0** | **Git 定稿** | IP/Brief/SOP/handoff（已在 `content/`、`docs/`、`agents/`） | **Must 优先读**；改完 commit | 否（走 `cursor-brand-corpus` 镜像，有界） |
| **T1** | **Drive 精选包** | 当前 campaign 常用文件夹（见 manifest） | 可 sync 到 `brand-ip-knowledge`；RAG **短答 + Sources** | **仅 manifest 内文件夹** |
| **T2** | **Drive 书海** | 海量书籍、归档、全库 | **Must：搜索 / 按 file id 读片段** → 写入 `content/personal-ip/intake/` 或 Brief 块 | **禁止**全量 embedding |

**配置：** `integration/handoff/drive-context-manifest.json`（Owner 维护 folder id / 名称；无文件时用 `.example` 复制）。

---

## 3. 标准工序（达到「精准 prompt」）

```
Owner 目标（原话短）
  → CEO 读 L1：AGENT-TAKEOVER · PROMPT-CONTEXT-STANDARD · 本文
  → 需要 Drive 事实？
       T2：gdocs / Drive MCP 搜索 → 打开 ≤N 个文件 → 摘录带 drive_file_id
       T1：可选 RAG 短问（要 Sources）交叉核对
  → 外置：写 content/personal-ip/intake/<slug>.md（或 Brief 一节）
  → L1 摘要：Goal + 约束 + 指向 intake 路径（≤400 字级，见 L012）
  → CEO gate / evolution（chat 仍短）
  → Open WebUI（可选）：仅长文 Pipe / 有界 RAG；产出进 outbox → 再回 Git 改
```

**禁止：** 把整段 WebUI 聊天记录当 Brief；禁止「搜完书海仍不写 intake 就定稿」。

---

## 4. intake 文件最低结构（Must）

```markdown
# intake · <slug>
- source: google drive | openwebui outbox | owner paste
- drive_files: [{ "name": "...", "id": "..." }]   # 有则填
- goal_one_line: <Owner 原话>
## 摘录（仅任务相关）
...
## 未解决 / 待 verify
...
```

路径范例：[content/personal-ip/intake/2026-10-29-ngv-flute-curation-theme.md](../content/personal-ip/intake/2026-10-29-ngv-flute-curation-theme.md)

---

## 5. Open WebUI 在本动机下的位置

| 用途 | 允许 |
|------|------|
| `# workflow-automation-pack` / `# agent-prompt-pack` | 问 **命令与 SOP**（有界） |
| `# brand-ip-knowledge` | **T1 精选包**事实；必须 Sources |
| Pipe 长文 | 草稿 → **outbox → intake 文件** |
| 代替 Drive 搜索 T2 | **不允许** |
| 代替 Git 定稿 | **不允许** |

---

## 6. 新 Agent 接手读序（Drive 相关）

1. 本文（动机 + 三层）  
2. [PROMPT-CONTEXT-STANDARD.md](./PROMPT-CONTEXT-STANDARD.md)  
3. [CONTEXT-WINDOW-AND-DATA-ROUTING.md](./CONTEXT-WINDOW-AND-DATA-ROUTING.md)  
4. [integration/openwebui-rag/README.md](../integration/openwebui-rag/README.md)  
5. `integration/handoff/drive-context-manifest.json`（若存在）

验收：`bash scripts/verify-handoff.sh`（handoff 含 drive manifest example 时一并检查）。

---

## 7. Owner / Agent 维护 Drive「精选包」（T1）

1. 在 Drive 建或指定 **当前 program 文件夹**（不必搬书海）。  
2. 把 folder id 写入 `drive-context-manifest.json` → `tier1_sync_folders`。  
3. 跑：`python3 integration/openwebui-rag/scripts/sync_brand_drive_to_openwebui.py`（仅 sync 配置范围内）。  
4. **书海（T2）不加入 sync**；用时再搜，结果进 intake。

这样：**动机保留**（外置、分层），**Open WebUI 仍管有界 RAG**，**Cursor + Google 搜 T2**，新 Agent 不依赖长 chat。
