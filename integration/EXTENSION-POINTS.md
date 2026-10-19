# 扩展接口 · 预留能力（不改 kernel）

> **当前运行策略（Owner 2026-10）：** **Cursor + 00 Manager + 按需 `manager-autopilot`**；Process Launcher **已 vendor、默认不常驻**。  
> 本文定义 **以后加能力时改哪里**，避免新 Agent 另起炉灶或破坏接手链。

## 1. 分层（谁接什么改动）

```
Owner 目标 / 红线     → integration/goals/registry.json · IMPORTANT.md · content/personal-ip/
指挥与派活           → agents/00-manager/AUTO-WORKFLOW.md · scripts/manager-autopilot.sh
内容定稿             → content/<domain>/ · PIPELINE.md · evaluate 脚本
对外工具能力         → vendor/<repo>/ + rules/skills/skill_*.md（唯一 discovery 入口）
本机调度 / TCC 桥    → vendor/process-launcher/ + overlay + launcher.yaml（可选）
私有路径与配方       → rules/skills/overlays/*.local.md · gitignored
并行调研中间工件     → tmp/parallel/<session_slug>/ · gitignored（见 workflow-parallel-subagents overlay）
```

**原则：** 新能力优先 **接在已有层**；只有跨层时才新增 `integration/*.md` 说明 + INDEX/WORKSPACE 一行路由。

## 2. Process Launcher · 预留接口（工具箱模式）

| 接口 | 路径 | 用途 | 默认 |
|------|------|------|------|
| Discovery | `rules/skills/skill_process_launcher.md` | Agent 命中「定时/延时/launcher」 | 已注册 |
| 本仓边界 | `integration/process-launcher-adoption.md` | 与 CEO/autopilot 分工 | 必读 |
| 私有配方 | `overlays/process-launcher.local.md` | label、路径、启用说明 | 可选 |
| 预留 job 片段 | `integration/templates/process-launcher-reserved-jobs.example.yaml` | 复制进 `launcher.yaml` 的 `periodic_jobs` / `services` | **全部 `enabled: false`** |
| Patrol 契约 | `vendor/.../skills/skill_agentic_patrol.md` | 长任务巡检 | 按需读 |
| HTTP 契约 | `http://127.0.0.1:7997` | `/run`、`/scheduled`、`/periodic` | 服务未启时不阻塞本仓 |

**启用步骤（以后 Owner 决定开时）：**

1. `cp vendor/process-launcher/config/launcher.example.yaml` → `config/launcher.yaml`
2. 从 `integration/templates/process-launcher-reserved-jobs.example.yaml` **合并**需要的块，改 `cwd`/`command`，**单条** `enabled: true`
3. GUI 终端：`process-launcher start --config vendor/process-launcher/config/launcher.yaml`
4. 更新 `process-launcher.local.md` 记录「已启用哪些 label」（仍不进 git）

**禁止：** Agent 自行 shutdown/restart launcher；scheduled 命令违反 IMPORTANT Dry Run。

## 3. CEO / 数据轨 · 预留接口

| 接口 | 扩展方式 |
|------|----------|
| CEO 一键流 | 改 `scripts/manager-autopilot.sh` 或在其 **末尾** 调用新脚本（保持单入口） |
| 新 Goal | `integration/goals/registry.json` + `GOALS-REGISTRY.md` + `verify-goals.sh` 可测项 |
| 新平台 CSV | `content/analytics/inbox/<platform>-*.csv` + `scripts/analytics/fetch/` 新 fetch 脚本 |
| 09→04 派活 | 仍输出 `content/analytics/derived/ceo-dispatch-latest.md`（勿平行第二派活文件） |

定时 autopilot **若将来启用**：只通过 Launcher 调 **`manager-autopilot.sh`**，不 fork 第二套 CEO 逻辑。

## 4. Skills / Vendor · 预留接口

| 动作 | 接口 |
|------|------|
| 新 public repo | `git submodule add` → `vendor/<name>/` |
| 注册 discovery | **一个** `rules/skills/skill_<name>.md` → vendor root skill |
| 索引 | `rules/skills/INDEX.md` · `rules/WORKSPACE.md` · `integrations/index.md` |
| 本仓特殊边界 | `integration/<name>-adoption.md`（可选但推荐） |
| 暂缓清单 | INDEX Tier 3 · WORKSPACE「暂缓」表 |

## 5. 改完后的最小验收（防接手乱）

```bash
bash scripts/verify-handoff.sh
bash scripts/manager-autopilot.sh    # 若动 CEO 链
# 若启用 launcher：curl -sf http://127.0.0.1:7997/health
```

新 Agent 仍以 [HANDOFF-MD-MANIFEST.md](../docs/HANDOFF-MD-MANIFEST.md) 为准；**扩展本文或 adoption 时** 同步 manifest「Should」表一行。
