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
