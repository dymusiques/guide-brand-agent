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
