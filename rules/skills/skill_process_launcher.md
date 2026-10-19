# Skill Router: Process Launcher

> **唯一 discovery 入口。** 长任务巡检模式见 vendor 内 `skills/skill_agentic_patrol.md`（第二份 skill，**不**单独占 INDEX 路由）。

## 激活顺序

1. **Overlay（Must 读本仓边界）:** [integration/process-launcher-adoption.md](../../integration/process-launcher-adoption.md)
2. **私有路径/定时任务配方（可选）:** `rules/skills/overlays/process-launcher.local.example.md` → 复制为 `process-launcher.local.md`（gitignored）
3. **Root skill（API 与 TCC）:** `vendor/process-launcher/skills/skill_process_launcher.md`
4. **可选 · Agentic Patrol:** `vendor/process-launcher/skills/skill_agentic_patrol.md`

## When to Use

本机 **localhost HTTP** 启停命令、读日志、** durable 延时/定点任务**、YAML 声明的常开服务与周期任务。触发词：延时执行、定时任务、周期任务、background job、process launcher、run in N minutes、`POST /run`。

**本仓默认不用它替代：** `bash scripts/manager-autopilot.sh`、Brief verify、小红书发帖（见 adoption 文档分工表）。

## Quick Activation

```bash
source .venv/bin/activate
pip install -e 'vendor/process-launcher[dev]'   # 首次；需 Python ≥3.12
cp vendor/process-launcher/config/launcher.example.yaml vendor/process-launcher/config/launcher.yaml  # 本地编辑，不进 git
# Owner：在 Terminal.app / iTerm2 交互会话中启动（TCC 链）
process-launcher start --config vendor/process-launcher/config/launcher.yaml
curl -sf http://127.0.0.1:7997/health
```

**红线（来自 upstream skill）：** Agent **不得** `POST /shutdown` 或自行用 launchd/cron/PM2 重启 launcher；需重启时 **请求 Owner 在 GUI 终端手动操作**。
