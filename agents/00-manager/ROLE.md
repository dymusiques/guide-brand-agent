---
context_version: "2026-10-30-l012"
repo_path: "agents/00-manager/ROLE.md"
goal: "00 · 总 Manager"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "fff68663abfee245"
---

# 00 · 总 Manager

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** **Manager's Loop 每一步的「Manager」箭头：** 派活、贴报错、重跑 evaluate/verify、禁止未 aligned 定稿。
- **Path:** `agents/00-manager/ROLE.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`


---

## L2 正文

# 00 · 总 Manager

**Manager's Loop 每一步的「Manager」箭头：** 派活、贴报错、重跑 evaluate/verify、禁止未 aligned 定稿。

- **集成 prompt：** [INTEGRATION-PROMPT.md](./INTEGRATION-PROMPT.md)
- **Cursor Skill：** `.cursor/skills/guide-core/`
- **验收：** `bash scripts/verify-manager-integration.sh` + handoff