---
context_version: "2026-10-30-l012"
repo_path: "content/evolution/_template/README.md"
goal: "Evolution artifact 模板"
openwebui_route: "intake_l2"
cursor_route: "read"
content_sha256: "73572729da0e7a3b"
---

# Evolution artifact 模板

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** 复制本目录结构到新 slug：
- **Path:** `content/evolution/_template/README.md`
- **Open WebUI:** `intake_l2`
- **Cursor:** `read`


---

## L2 正文

# Evolution artifact 模板

复制本目录结构到新 slug：

```text
content/evolution/<agent-slot>/<your-slug>/
  intake/              ← collector-intake.py 写入
  manifest.json
  versions/v0.md       ← 首版产出
  reference/gold.md    ← Owner 标准答案
  metrics.jsonl        ← evaluate-edit-distance.py --append
```

命令示例见 [docs/COLLECTOR-EVALUATOR-PIPELINE.md](../../docs/COLLECTOR-EVALUATOR-PIPELINE.md)