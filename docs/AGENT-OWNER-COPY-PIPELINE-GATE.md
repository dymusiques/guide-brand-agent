# Drive 备份 + 三平台大V · 硬门槛

机械真源（monorepo）：`~/Desktop/未命名/docs/agent/AGENT-OWNER-COPY-PIPELINE-GATE.json`

## 一条命令

```bash
python3 scripts/agent-owner-copy-pipeline-gate.py --goal "<Owner 原话>"
```

handoff：`integration/handoff/owner-copy-pipeline-gate-latest.json`

## 必须通过什么

1. **Drive**：`owner-drive-hydrate-latest.json` 中 screen `direct_hit` + manifest 钉选文件 · 非 `BLOCKED`/`FAIL`，且 `read_complete` 或 OCR `PARTIAL`（≥200 字）
2. **大V**：`owner-platform-voice-benchmark-latest.json` **PASS** + roster 每平台 ≥2 账号

已编入 `agent-owner-research-gate.py` 层 `owner_copy_pipeline_gate`；C1/C3 在文案/口播类 goal 上同样要求 research-gate PASS。