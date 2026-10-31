---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/skill_google_docs.md"
goal: "Skill Router: Google Workspace"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "1aea672e655dc645"
---

# Skill Router: Google Workspace

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **唯一 discovery 入口。** 不要直接暴露 `vendor/gdocs-skill/` 内多个文件给全局 skill 链。
- **Path:** `rules/skills/skill_google_docs.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **激活顺序**: 1. **Read local overlay first:** `rules/skills/overlays/gdocs-skill.local.md`
- **When to Use**: User asks for Google Docs, Gmail, Calendar, or Drive download operations.
- **Quick Activation (this workspace)**: ```bash


---

## L2 正文

# Skill Router: Google Workspace

> **唯一 discovery 入口。** 不要直接暴露 `vendor/gdocs-skill/` 内多个文件给全局 skill 链。

## 激活顺序

1. **Read local overlay first:** `rules/skills/overlays/gdocs-skill.local.md`  
   Workspace paths, secrets dir, OAuth account aliases live here only.
2. **Read full CLI reference:** `vendor/gdocs-skill/docs/skill_google_docs.md`  
   Complete command reference, error handling, and pitfalls.
3. **OAuth setup (one-time):** `vendor/gdocs-skill/README.md`

## When to Use

User asks for Google Docs, Gmail, Calendar, or Drive download operations.  
**Default to `sync` over `publish`** when Markdown will be edited repeatedly.

## Quick Activation (this workspace)

```bash
source .venv/bin/activate
python -m gdocs --secrets-dir vendor/gdocs-skill/secrets <command>
```

See overlay for canonical paths. Never commit `vendor/gdocs-skill/secrets/credentials.json` or `token.json`.