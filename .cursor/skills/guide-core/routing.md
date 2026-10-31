---
context_version: "2026-10-30-l012"
repo_path: ".cursor/skills/guide-core/routing.md"
goal: "Task Routing"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "6ec61f03dfca32ce"
---

# Task Routing

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** ```
用户消息
  → guide-core（识别主领域，可读多领域）
  → 读对应 .cursor/skills/<domain>/SKILL.md
  → 查 rules/WORKSPACE.md 定位文件
  → 读 Git content/<domain>/（真相源，优先）
  → 查 Drive Knowledge Bank（仅 Owner 已
- **Path:** `.cursor/skills/guide-core/routing.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **文件落点**: | 产出类型 | Git（Must commit） | Drive（仅 Owner 说「同步 Drive」） |


---

## L2 正文

# Task Routing

```
用户消息
  → guide-core（识别主领域，可读多领域）
  → 读对应 .cursor/skills/<domain>/SKILL.md
  → 查 rules/WORKSPACE.md 定位文件
  → 读 Git content/<domain>/（真相源，优先）
  → 查 Drive Knowledge Bank（仅 Owner 已同步定稿时）
  → 需要 Doc/Gmail → rules/skills/skill_google_docs.md
  → 需要设计 → Canva MCP（需 Cursor 内授权）
  → 产出 → content/ → 稳定后 commit → （可选）Owner 说「同步 Drive」
  → 交班前 → bash scripts/verify-handoff.sh
```

## 文件落点

| 产出类型 | Git（Must commit） | Drive（仅 Owner 说「同步 Drive」） |
|---------|-------------------|-------------------------------------|
| IP 定位稿 | `content/personal-ip/` | `02-personal-ip/` |
| 品牌/商业策划 | `content/business-brand/` | `03-business-brand/` |
| 营销 Brief | `content/marketing/` | `04-marketing/` |
| 小红书文案 / 选题 Brief | `content/xiaohongshu/` | `05-xiaohongshu/` |

小红书 **选题 / Topic Manager**：`.cursor/skills/xiaohongshu/topic-manager.md` → `scripts/evaluate-xhs-topic.py`
| 视觉 Brief | `content/visual/` | `06-visual/` |