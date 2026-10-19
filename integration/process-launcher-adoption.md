# Process Launcher · 本仓采纳说明

> **真相源分工：** 能力 API 与 TCC 规则 → `vendor/process-launcher/skills/skill_process_launcher.md`；本文件只写 **danying-brand-agent 里用它做什么、不做什么**，防新 Agent 与 Manager 工作流打架。

## 0. 运行策略（Owner 确认 · 2026-10）

| 项 | 选择 |
|----|------|
| 主路径 | **Cursor + 00 Manager**；需要时 **`bash scripts/manager-autopilot.sh`** |
| Process Launcher | **工具箱已安装**（submodule + pip + 路由）；**默认不** `start` 常驻 |
| 预留 | 定时 autopilot / analytics / TCC 任务 → [templates/process-launcher-reserved-jobs.example.yaml](./templates/process-launcher-reserved-jobs.example.yaml)（`enabled: false`） |
| 以后加能力改哪 | [EXTENSION-POINTS.md](./EXTENSION-POINTS.md) |

新机/新 Agent：**不依赖** launcher 进程即可写 Brief、跑 verify、跑 autopilot。

## 1. 从上游提炼、对本仓有用的部分

### 1.1 框架：localhost 进程控制面

| 能力 | 典型用途 |
|------|----------|
| `POST /run` | 一次性或 **延时/定点** 跑 shell 命令；`command` 用 **数组** 更安全 |
| `GET /processes` + `/output` | 看子进程是否还在跑、读 stdout/stderr |
| `GET/POST/PATCH /scheduled` | SQLite 持久化定时任务；launcher 重启后可按 `misfire_policy` 恢复 |
| YAML `services:` | 常开守护（声明式，**不能** HTTP 动态创建） |
| YAML `periodic_jobs:` | daily/weekly/interval/cron；只读 HTTP + `POST /periodic/reload` |
| `/logs/heartbeat` · `/logs/output` | 审计与排错（**没有** bare `/logs`） |

**调度前习惯：** 目标 CLI 有 dry-run 就先 dry-run；409 `schedule_conflict` 表示同一 `run_at` 已有任务，需 `confirm_conflict` 或先 cancel。

### 1.2 框架：macOS TCC 权限桥

- 从 **Terminal.app / iTerm2** 交互启动的 launcher，其子进程可继承麦克风、屏幕录制、本地网络等 TCC 链。
- **无效链：** cron、launchd、PM2、无 GUI 祖先的 tmux server、Agent/SSH 后台自启 launcher。
- **Agent 禁止：** 调 `POST /shutdown`、自行重启 launcher；要重启 **找 Owner 在 GUI 终端操作**。

对本仓：**Playwright 反爬、将来 TCC 敏感自动化** 可考虑经 launcher 调度；**普通 verify / Brief evaluate** 仍直接在 `.venv` 里跑脚本即可。

### 1.3 框架：Agentic Patrol（可选）

`vendor/process-launcher/skills/skill_agentic_patrol.md` 定义 **Inspect → Stop 或 Schedule 一次 follow-up** 的长任务巡检契约：

- 看 **真实证据**（日志、exit code、产物文件），不靠 wall-clock 猜进度。
- 每次只 schedule **一个** 下次检查；终止条件写在 **稳定 prompt 文件** 里。
- **不保证** watchdog SLA：`completed` 只表示子进程 exit 0，不表示 LLM 一定完成了巡检。

**本仓映射：** 长时 `verify-all`、大批量渲染、外部下载等 **Owner 显式授权** 时可参考；**不**用来替代 00 Manager 会话内逐步派活。Cursor 没有 OpenCode append；用 **脚本 + 定点 `/run`** 或 YAML periodic 更贴切。

## 2. 与本仓已有机制的分工（接手必读）

| 机制 | 负责什么 | Process Launcher 是否替代 |
|------|----------|---------------------------|
| `scripts/manager-autopilot.sh` | Goal 验收 → 仪表盘 → CEO 派活块 | **否** — 仍是一键 CEO 工作流 |
| `scripts/manager-workflow-verify.sh` | 单篇 Brief aligned | **否** |
| `content/xiaohongshu/PIPELINE.md` | Brief 三阶段 · Owner 发帖 | **否** — launcher 不代发 |
| `integration/IMPORTANT.md` Dry Run | 禁止未授权破坏性/发布 | **是** — scheduled 命令也须遵守 |
| Owner CSV → `analytics-pipeline.sh` | 数据复盘 | **可选** — CSV 落地后可用 periodic 提醒跑 pipeline |

**结论：** Process Launcher 是 **本机自动化基础设施（可选）**，不是 danying-brand-agent 的「第二个 CEO」。

## 3. 文件与路径（防 clone 后混乱）

| 类型 | 路径 | Git |
|------|------|-----|
| 上游代码 | `vendor/process-launcher/` | submodule |
| Discovery 唯一入口 | `rules/skills/skill_process_launcher.md` | ✅ |
| 本仓边界（本文） | `integration/process-launcher-adoption.md` | ✅ |
| 私有配方 | `rules/skills/overlays/process-launcher.local.md` | ❌ gitignore |
| 本地 launcher 配置 | `vendor/process-launcher/config/launcher.yaml` | ❌ vendor .gitignore |
| 运行时日志/DB | `vendor/process-launcher/logs/`、`state/` | ❌ |

**不要** 在 `rules/skills/` 再复制一份 upstream skill 全文；**不要** 把 `launcher.yaml` commit 进本仓根目录。

## 4. 新机 / 新 Agent 安装顺序

1. `git submodule update --init --recursive`（含 `vendor/process-launcher`）
2. `pip install -e 'vendor/process-launcher[dev]'`（见 [SETUP.md](../SETUP.md)）
3. 读本文 + router → 按需 `cp config/launcher.example.yaml` → `config/launcher.yaml`
4. **Owner** 在 GUI 终端启动 launcher（若要用 API）
5. 品牌/Brief 任务仍走 [AGENT-TAKEOVER.md](../docs/AGENT-TAKEOVER.md) 与 00 Manager — **不依赖** launcher 是否在跑

## 5. 验收

- Submodule：`[[ -f vendor/process-launcher/pyproject.toml ]]`
- Router：`rules/skills/skill_process_launcher.md`
- 扩展登记：`integration/EXTENSION-POINTS.md` · 预留 YAML 模板存在即可
- 可选 smoke：`curl -sf http://127.0.0.1:7997/health`（**仅当** Owner 已启动服务；未启动 **不是** FAIL）

## 6. 变更接口（摘要）

| 要改什么 | 接哪里 |
|----------|--------|
| 新 periodic / service | 本地 `launcher.yaml` + 可选从 `templates/process-launcher-reserved-jobs.example.yaml` 合并 |
| 新 label 约定 | `overlays/process-launcher.local.md` |
| 新 vendor 能力 | `EXTENSION-POINTS.md` §4 |
| CEO 逻辑本身 | **只**改 `manager-autopilot.sh` 或其调用的脚本，不在 launcher 里复制第二套 |
