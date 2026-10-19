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
- Settings → MCP：授权 **Google Drive**、**Canva**

## 5. 验证

```bash
bash scripts/verify-handoff.sh        # L0 接手（Must 无 FAIL）
bash scripts/verify-integration.sh    # 6 case 集成（有 OAuth 时应 6/6 PASS）
```

- [ ] `verify-handoff.sh` 无 FAIL
- [ ] `verify-integration.sh` 无 FAIL（无 OAuth 时 SKIP 3–4–6 可接受）
- [ ] 需代理访问 Google：`export HTTPS_PROXY=…` 后再跑集成脚本

## 6. Hub 关系

总索引不在本仓 → [danying-apps INDEX](https://github.com/dymusiques/danying-apps/blob/main/INDEX.md)
