# Cursor Automation · 分支真源（防旧分支）

真源：`integration/handoff/cursor-automation-branch-pin.json`

## Must（每个 Automation · Instructions 顶行）

```
仓库 guide-brand-agent / 分支 main only。禁止 checkout 其它分支；脚本路径以 main 为准。
```

Environment 必须显示：**`guide-brand-agent @ main`**（或 GitHub `dymusiques/guide-brand-agent` main）。

## 自验（本机 / Agent 改 Automation 前）

```bash
cd ~/Desktop/danying-brand-agent
python3 scripts/verify-cursor-automation-branch-pin.py
```

FAIL → 先 `git checkout main` · `git pull github main` · `git pull origin main` · push 后再跑 Automation。

## 远程分支 hygiene

- **只允许** `github/main` 与 `origin/main`（`cursor/*`、feature 分支易让云端 Agent 误以为要 checkout）。
- 已合并分支：`git push github --delete <branch>` · 同名删 `origin`。
- **不**用 `git push --force` 改历史去「盖掉」旧 commit；**以 main 最新 + 删多余远程分支** 为准。

## Cron 与时区（为何出现 18:30）

若自定义 **`30 10 * * *`** 但界面显示 **18:30 GMT+8**：

- 常见原因：Cron **按 UTC 解释**，10:30 UTC = **18:30 北京时间**。
- **要北京时间 10:30 日检**，任选其一：
  1. UI 选 **Every day at 10:30**，时区 **GMT+8**（不要手填 UTC cron）；
  2. 或 Custom cron **`30 2 * * *`**（02:30 UTC = 10:30 北京）；
  3. **10:00 日检也可接受**（你当前 Every day 10:00 = 正确本地时间则不必改）。

导表提醒 **20:30 周三/日**：若同样偏 8 小时，用 UI **20:30 + 周日/周三 + GMT+8**，或 UTC cron **`30 12 * * 0,3`**（12:30 UTC = 20:30 北京）。