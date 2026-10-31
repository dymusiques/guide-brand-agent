---
context_version: "2026-10-30-l012"
repo_path: "docs/BACKGROUND-GOAL-EVOLUTION.md"
goal: "后台目标链 · Baseline + Evaluator + 验收（Owner 只 setup 一次）"
openwebui_route: "rag_l1"
cursor_route: "read"
content_sha256: "1c2f570477cc6100"
---

# 后台目标链 · Baseline + Evaluator + 验收（Owner 只 setup 一次）

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** > **Owner（2026-10-27）：** 一条 CLI setup 后后台自转；**不要**日常「一键 autopilot」。  
> **频率：** **每天 1 次** · **09:00** · `Asia/Shanghai`（含 Gemini 6 case）。  
> **改频率：** Agent 见 [BACKGROUND-CYCLE-IN
- **Path:** `docs/BACKGROUND-GOAL-EVOLUTION.md`
- **Open WebUI:** `rag_l1`
- **Cursor:** `read`

## 章节锚点
- **Owner 只做一次（改 schedule 后需重启 Launcher）**: ```bash
- **环境**: - [GEMINI-NETWORK-AUTO.md](./GEMINI-NETWORK-AUTO.md)
- **TRIGGER（改间隔 / 改验收强度）**: **Must 问 Owner：** [integration/BACKGROUND-CYCLE-INTERVAL-TRIGGER.md](../integration/BACKGROUND-CYCLE…


---

## L2 正文

# 后台目标链 · Baseline + Evaluator + 验收（Owner 只 setup 一次）

> **Owner（2026-10-27）：** 一条 CLI setup 后后台自转；**不要**日常「一键 autopilot」。  
> **频率：** **每天 1 次** · **09:00** · `Asia/Shanghai`（含 Gemini 6 case）。  
> **改频率：** Agent 见 [BACKGROUND-CYCLE-INTERVAL-TRIGGER.md](../integration/BACKGROUND-CYCLE-INTERVAL-TRIGGER.md) — **须先问 Owner**。


## Owner 只做一次（改 schedule 后需重启 Launcher）

```bash
cd /path/to/danying-brand-agent
bash scripts/setup-background-goal-evolution.sh
```

**Terminal.app / iTerm2** 启动（或 **改 yaml 后重启**）：

```bash
cd vendor/process-launcher
../../.venv/bin/process-launcher start --config config/dba-brand-agent.yaml
# 或：cd 到 repo 根 && source .venv/bin/activate && cd vendor/process-launcher && process-launcher start ...
# 若已在跑：Owner 在 GUI 终端 Ctrl+C 停掉再 start
```


## 环境

- [GEMINI-NETWORK-AUTO.md](./GEMINI-NETWORK-AUTO.md)  
- [integration/process-launcher-adoption.md](../integration/process-launcher-adoption.md)  
- [OWNER-INPUT-PRINCIPLES.md](./OWNER-INPUT-PRINCIPLES.md)


## TRIGGER（改间隔 / 改验收强度）

**Must 问 Owner：** [integration/BACKGROUND-CYCLE-INTERVAL-TRIGGER.md](../integration/BACKGROUND-CYCLE-INTERVAL-TRIGGER.md)