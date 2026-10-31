---
context_version: "2026-10-30-l012"
repo_path: "content/xiaohongshu/README.md"
goal: "小红书 Brief（Git 真相源）"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "633b32cbb9c33cd9"
---

# 小红书 Brief（Git 真相源）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** 小红书 Brief（Git 真相源）
- **Path:** `content/xiaohongshu/README.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`


---

## L2 正文

# 小红书 Brief（Git 真相源）

**管线全文：** [PIPELINE.md](./PIPELINE.md)（状态、交班、批量 verify）

Topic Manager 产出目录。命名建议：

`YYYY-MM-DD-<slug>-brief.md`

每个 Brief 须含 `<!-- xhs-classifier -->` JSON 块（见 `kernels/templates/xhs-content-brief.template.md`）。

验收：

```bash
python scripts/evaluate-xhs-topic.py --brief content/xiaohongshu/<file>.md
bash scripts/verify-xhs-content-dir.sh   # 目录内全部 *-brief.md
bash scripts/verify-xhs-topic.sh         # kernel 改动的交班前
```

Skill：`.cursor/skills/xiaohongshu/topic-manager.md`