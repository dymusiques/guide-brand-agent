---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/skill_docx.md"
goal: "Skill Router: DOCX (Word)"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "1010c2e348a14d3a"
---

# Skill Router: DOCX (Word)

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **唯一 discovery 入口。**
- **Path:** `rules/skills/skill_docx.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **激活顺序**: 1. **Overlay（可选）:** `rules/skills/overlays/docx-skill.local.example.md`
- **When to Use**: Word 表单/文档 **inspect、填表、轻量编辑**；须保留版式。触发词："DOCX"、"Word 表单"、"填 Word"。
- **Quick Activation**: ```bash


---

## L2 正文

# Skill Router: DOCX (Word)

> **唯一 discovery 入口。**

## 激活顺序

1. **Overlay（可选）:** `rules/skills/overlays/docx-skill.local.example.md`
2. **Root skill:** `vendor/docx-skill/docs/skill.md`

## When to Use

Word 表单/文档 **inspect、填表、轻量编辑**；须保留版式。触发词："DOCX"、"Word 表单"、"填 Word"。

## Quick Activation

```bash
source .venv/bin/activate
pip install -e 'vendor/docx-skill[dev]'   # 首次；CLI 仍为 scaffold 时以 skill 文档为准
```

**红线：** 不原地覆盖 Owner 原件；私密表格不进 commit（见 skill 内 Non-Goals）。