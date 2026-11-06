# Cursor 聊天与工作区整理约定

**Owner 确认：2026-11-03**

## 唯一工作区（Must）

- **打开文件夹：** `~/Desktop/danying-brand-agent`（仅此一个 Git 仓作为 Brand Agent 产线）
- **不在 Desktop** 为 Personal IP、Weekly Review、Content Manager 等主题再建平行目录
- **Chat 分组** 只在 Cursor Agents 侧（标题、归档、少开重复 New Chat），不对应磁盘子文件夹

## Chat 标题 → 仓内真相源

| Cursor 里常见 Chat 名 | 仓内去哪找 / 放哪 | Agent 编号 |
|----------------------|-------------------|------------|
| **Content Manager** | `content/xiaohongshu/` · `content/xiaohongshu/PIPELINE.md` · `agents/06-xhs-content-pipeline/` | 06 内容管线 |
| **Personal IP location** | `content/personal-ip/` · `agents/01-personal-ip/` · `.cursor/skills/personal-ip/` | 01 |
| **Automated weekly business review** | `docs/DAILY-GM-TRIO-SOP.md` · `agents/12-owner-daily-brief/` · `content/daily-brief/` · `kernels/daily-gm/` | 12 + daily-gm |
| **Context management strategies** | `docs/PROMPT-CONTEXT-STANDARD.md` · `docs/CONTEXT-WINDOW-AND-DATA-ROUTING.md` · CEO 上下文重组 HTML 在 `content/evolution/00-manager/ceo-inbox/` | 00 / 文档轨 |
| **Open WebUI configuration overview** | `integration/openwebui-rag/` · `integration/handoff/openwebui-jobs/` | 08 集成 |
| **问题解决**（通用 Q&A） | 仍用 **同一 Folder** `danying-brand-agent`；杂项笔记可放 `docs/owner-notes/`（按需建），**不要**再开 `Guide/0/问题解决` 路径 |

## 建议归档的重复 Chat（保留较新一条即可）

| 标题 | 建议保留 | 建议不再打开 |
|------|----------|--------------|
| Automated weekly business review | `fcbd2e3c-c672-4465-8fdc-b91426ecb262`（2026-11-03） | `91ee8863-cfb4-4730-a29d-1865aaa47322` |
| Personal IP location | `2f261ec4-01f8-49cf-a211-c7536e5c5c01`（2026-11-03） | `da247c32-d0c1-4590-ad6b-f91b7e73fd81` |

（在 Agents 窗口对旧 Chat 使用归档/删除，按 Cursor 当前 UI 为准。）

## 桌面其它项（不归进本仓）

| 路径 | 说明 |
|------|------|
| `~/Desktop/Open WebUI Personal IP` | Open WebUI 侧配置/知识库，与 Git 仓分开 |
| `~/Desktop/Project1/Guide` | 历史空壳；可删或只留 README 指针到本仓 |
| `~/Desktop/飞书-*` | 飞书导出/下载区，非 Brand Agent 代码 |

## 新开 Chat 习惯

1. **File → Open Folder** 始终选 `danying-brand-agent`
2. 按 **任务类型** 开 Chat，标题建议：`Brand · Content Manager · 2026-11-03` 这类带前缀
3. 换 Agent / 新一天续作：先说 **`danying-brand-agent`** 或让读 `docs/AGENT-TAKEOVER.md`
4. 不必为整理去建 Cursor **Project（Cloud 协调）**；跨周大迁移再考虑
