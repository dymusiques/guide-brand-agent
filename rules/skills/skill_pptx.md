---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/skill_pptx.md"
goal: "Skill Router: PPTX"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "87be875089c8ea7f"
---

# Skill Router: PPTX

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **唯一 discovery 入口。** 小红书 **封面** 仍优先 `.cursor/skills/brand-visual/` + Canva。
- **Path:** `rules/skills/skill_pptx.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **激活顺序**: 1. **Overlay（可选）:** `rules/skills/overlays/pptx-skill.local.example.md`
- **When to Use**: 读/改 **PPTX**、结构化 dump、LibreOffice 渲染 PNG 自检。触发词："pptx"、"改 slide"、"投资人 deck"（**非** Canva 小红书封面）。
- **Quick Activation**: ```bash


---

## L2 正文

# Skill Router: PPTX

> **唯一 discovery 入口。** 小红书 **封面** 仍优先 `.cursor/skills/brand-visual/` + Canva。

## 激活顺序

1. **Overlay（可选）:** `rules/skills/overlays/pptx-skill.local.example.md`
2. **Root skill:** `vendor/pptx.skill/docs/skill.md`
3. **环境:** `pptx-skill doctor`（LibreOffice 渲染需 Owner 同意安装，见 vendor README）

## When to Use

读/改 **PPTX**、结构化 dump、LibreOffice 渲染 PNG 自检。触发词："pptx"、"改 slide"、"投资人 deck"（**非** Canva 小红书封面）。

## Quick Activation

```bash
source .venv/bin/activate
pip install -e 'vendor/pptx.skill[dev]'   # 首次
pptx-skill doctor
```