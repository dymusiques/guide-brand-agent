---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/skill_writing.md"
goal: "Skill Router: Writing (long-form)"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "95c3b0e131ac5da7"
---

# Skill Router: Writing (long-form)

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **唯一 discovery 入口。** 不暴露 `vendor/writing-skill/skills/` 下全部文件。
- **Path:** `rules/skills/skill_writing.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **边界（Owner · 1-A）**: - **小红书 Brief / Pitch / aligned 定稿** → **不走**本 skill；用 `.cursor/skills/xiaohongshu/`、`content/xiaoho…
- **激活顺序**: 1. **Overlay（可选）:** `rules/skills/overlays/writing-skill.local.example.md`
- **When to Use**: 触发词："外部长文"、"internal memo"、"写深度稿"、"survey report"、"prose lint"（**非** "小红书 Brief")。
- **Quick Activation**: ```bash


---

## L2 正文

# Skill Router: Writing (long-form)

> **唯一 discovery 入口。** 不暴露 `vendor/writing-skill/skills/` 下全部文件。

## 边界（Owner · 1-A）

- **小红书 Brief / Pitch / aligned 定稿** → **不走**本 skill；用 `.cursor/skills/xiaohongshu/`、`content/xiaohongshu/PIPELINE.md`、`evaluate-xhs-topic.py`。
- **本 skill** → 内部 memo、决策简报、**外部长文**（专栏/深度稿）、听见 Daily **长文版**（非 Brief 模板）。

## 激活顺序

1. **Overlay（可选）:** `rules/skills/overlays/writing-skill.local.example.md`
2. **Root skill:** `vendor/writing-skill/skills/writing_workflows.md`
3. **CLI（external 中文 lint）:** `python -m writing_skill.external_prose_lint_cli <file.md>`

## When to Use

触发词："外部长文"、"internal memo"、"写深度稿"、"survey report"、"prose lint"（**非** "小红书 Brief")。

## Quick Activation

```bash
source .venv/bin/activate
pip install -e vendor/writing-skill   # 首次
python -m writing_skill.external_prose_lint_cli content/…/article.md
```