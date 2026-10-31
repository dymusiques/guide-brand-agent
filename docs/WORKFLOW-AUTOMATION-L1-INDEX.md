# Workflow 自动化 · L1 索引（机器 + 人）

> 生成 UTC：`2026-10-31T16:11:07.929653+00:00` · JSON：`integration/handoff/workflow-automation-catalog-l1.json`

## 一键执行

```bash
python3 scripts/run-workflow-from-manifest.py --list-layers
python3 scripts/run-workflow-from-manifest.py --layer L2_CEO_START --goal "<Owner 原话>"
python3 scripts/run-workflow-from-manifest.py --phrase "CEO 开始执行" --goal "<Owner 原话>"
bash scripts/run-context-reorg-pipeline.sh   # Open WebUI 上下文全量同步
```

## 层级（L0_BOOT → L4_CAMPAIGN）

### `L0_BOOT` — Clone / new machine / new Agent
- **Owner 触发：** 「全部克隆」 · 「danying-brand-agent」 · 「新机接手」

### `L1_BACKGROUND` — Daily machine cycle (no Owner utterance)
- **命令：** `scripts/background-goal-evolution-cycle.sh`

### `L2_CEO_START` — Owner says work
- **Owner 触发：** 「CEO 开始执行」 · 「请 CEO 开始工作」 · 「CEO 开始」 · 「CEO 干活」
- **命令：** `bash scripts/ceo-full-execution-pipeline.sh --goal "<owner goal>"`
- **Open WebUI 步 −1：** `bash scripts/run-openwebui-router-pipeline.sh --goal "<owner goal>"`

### `L3_BRIEF_GATE` — Brief quality gate + evolution until READY

### `L4_CAMPAIGN` — 01-12 campaign / deep delivery
- **命令：** `bash scripts/run-ceo-deep-delivery-cycle.sh`

## Open WebUI Knowledge

- 聊天：`# workflow-automation-pack` — 问「L3 brief gate  exit 42 怎么办」
- 与 `# cursor-brand-corpus` · `# agent-prompt-pack` 并用

## 验收

```bash
bash scripts/verify-workflow-automation.sh
```
