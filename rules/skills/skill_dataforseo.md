---
context_version: "2026-10-30-l012"
repo_path: "rules/skills/skill_dataforseo.md"
goal: "Skill Router: DataForSEO"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "92961de136cee524"
---

# Skill Router: DataForSEO

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **边界：** 关键词/SERP **补充** Drive 选题 PDF；不替代 Owner Excel 队列。
- **Path:** `rules/skills/skill_dataforseo.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`


---

## L2 正文

# Skill Router: DataForSEO

> **边界：** 关键词/SERP **补充** Drive 选题 PDF；不替代 Owner Excel 队列。

1. **Root skill:** `vendor/dataforseo-skill/skills/dataforseo.md`
2. **Adoption:** [ip-content-skills-adoption.md](../../integration/ip-content-skills-adoption.md)

触发词："DataForSEO"、"关键词 API"、"SERP"。

```bash
pip install -e vendor/dataforseo-skill   # 首次 · 凭证进 overlay
```