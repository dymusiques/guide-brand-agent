---
context_version: "2026-10-30-l012"
repo_path: "SETUP.md"
goal: "SETUP · Guide Brand Agent"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "1e4b62154b7e79db"
---

# SETUP · Guide Brand Agent

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** 新机 / 新 Agent clone 后执行（主 Agent 直接做，见 hub `rules/check/check.md`）。
- **Path:** `SETUP.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **1. Clone**: ```bash
- **2. Python**: ```bash
- **3. OAuth（一次性 · 不进 git）**: ```bash
- **4. Cursor**: - Open Folder → 新终端自动激活 `.venv`（`.vscode/settings.json`）
- **5. 验证**: ```bash
- **6. 后台目标链（新机 · 自动写入配置）**: **新机 / 新 Agent：** 跑 **`bash scripts/new-machine-bootstrap.sh`**（已含 `ensure-background-goal-evolution…
- **7. Hub 关系**: 总索引不在本仓 → [danying-apps INDEX](https://github.com/dymusiques/danying-apps/blob/main/INDEX.md)


---

## L2 正文

# SETUP · Guide Brand Agent

新机 / 新 Agent clone 后执行（主 Agent 直接做，见 hub `rules/check/check.md`）。

## 1. Clone

```bash
origin repo clone danying/guide-brand-agent ~/guide-brand-agent
cd ~/guide-brand-agent
git submodule update --init --recursive
# 若 submodule 拉取失败（无法直连 github.com），临时开代理后重跑上一行，例如：
# export HTTPS_PROXY=http://127.0.0.1:3213 HTTP_PROXY=http://127.0.0.1:3213
```

## 2. Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e vendor/gdocs-skill
pip install -e vendor/writing-skill
pip install -e vendor/docx-skill
pip install -e 'vendor/pptx.skill[dev]'
pip install -e 'vendor/process-launcher[dev]'   # Python ≥3.12 · 可选 API 见 integration/process-launcher-adoption.md
# ai-agent-cli-skill：仅 Markdown submodule，无 pip；headless 见 integration/ai-agent-cli-adoption.md

# IP 内容工具链（Owner 2026-10-22 已纳入 SETUP · 触发条件见 integration/ip-content-skills-adoption.md）：
pip install -e vendor/semantic-search-skill
pip install -e vendor/voice-lora
pip install -e vendor/bilibili-upload-skill
pip install -e vendor/asr-skill
pip install -e vendor/online-media-skill
pip install -e vendor/voice-memos-skill
pip install -e vendor/intake-skill
pip install -e vendor/ai_session_export
pip install -e vendor/vlog-skill
pip install -e vendor/playwright-test-skill
pip install -e vendor/typefully-twitter-skill
pip install -e vendor/dataforseo-skill
playwright install chromium   # bilibili-upload / pw-test 需要
# ASR / intake 转写：按需 pip install -e 'vendor/asr-skill[...]' / 'vendor/intake-skill[qwen-asr]'（MLX · 见 vendor README）
# opus-video-audio-skill：无 pyproject · 脚本仓，用时读 vendor skill

bash scripts/verify-ip-skills-env.sh   # Agent：换机/装完 pip 必跑 · 防 CLI/PATH/CDP 误读
```

## 3. OAuth（一次性 · 不进 git）

```bash
# 将 Desktop OAuth JSON 放到：
# vendor/gdocs-skill/secrets/credentials.json
chmod 600 vendor/gdocs-skill/secrets/credentials.json

# overlay（含 Drive folder ID）：
cp rules/skills/overlays/gdocs-skill.local.example.md \
   rules/skills/overlays/gdocs-skill.local.md
# 从安全备份恢复 token.json 或重新授权：
python -m gdocs --secrets-dir vendor/gdocs-skill/secrets create --title "Smoke test"
```

## 4. Cursor

- Open Folder → 新终端自动激活 `.venv`（`.vscode/settings.json`）
- **Google（推荐 · Owner 已授权 Agent）：** §3 的 **gdocs CLI + token.json** 即可；Agent **默认不用**反复 Connect MCP。见 [docs/OWNER-GOOGLE-GRANT-AGENT.md](docs/OWNER-GOOGLE-GRANT-AGENT.md)。
- **Customize → MCPs**（**可选** duplicate）：Drive / Gmail / Calendar / Canva — 未 Connect 时 Agent **仍走 CLI**，**不会**在 chat 请你确认。

## 5. 验证

```bash
bash scripts/verify-handoff.sh        # L0 接手（Must 无 FAIL）
bash scripts/verify-integration.sh    # 6 case 集成（有 OAuth 时应 6/6 PASS）
```

- [ ] `verify-handoff.sh` 无 FAIL
- [ ] `verify-integration.sh` 无 FAIL（无 OAuth 时 SKIP 3–4–6 可接受）
- [ ] 需代理访问 Google：`export HTTPS_PROXY=…` 后再跑集成脚本

## 6. 后台目标链（新机 · 自动写入配置）

**新机 / 新 Agent：** 跑 **`bash scripts/new-machine-bootstrap.sh`**（已含 `ensure-background-goal-evolution.sh`，**不必**单独记 setup 脚本名）。

仅补写 launcher 配置时：

```bash
bash scripts/ensure-background-goal-evolution.sh
```

**第一次在 Terminal.app 启动 daily 09:00 调度（Owner 或 Agent 提示下做一次）：**

```bash
cd vendor/process-launcher && ../../.venv/bin/process-launcher start --config config/dba-brand-agent.yaml
```

见 [docs/BACKGROUND-GOAL-EVOLUTION.md](docs/BACKGROUND-GOAL-EVOLUTION.md)。改频率见 [integration/BACKGROUND-CYCLE-INTERVAL-TRIGGER.md](integration/BACKGROUND-CYCLE-INTERVAL-TRIGGER.md)。

## 7. Hub 关系

总索引不在本仓 → [danying-apps INDEX](https://github.com/dymusiques/danying-apps/blob/main/INDEX.md)