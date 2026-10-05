# SETUP · Guide Brand Agent

新机 / 新 Agent clone 后执行（主 Agent 直接做，见 hub `rules/check/check.md`）。

## 1. Clone

```bash
origin repo clone danying/guide-brand-agent ~/guide-brand-agent
cd ~/guide-brand-agent
git submodule update --init --recursive
```

## 2. Python

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e vendor/gdocs-skill
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
bash scripts/verify-handoff.sh   # 接手完整性（Must PASS 或 PASS with warnings）
```

- [ ] `verify-handoff.sh` 无 FAIL
- [ ] （可选）`python -m gdocs ... gmail profile`（需代理时先 export HTTP_PROXY）
- [ ] （可选）Drive MCP `search` 能找到 `AI-Agent-Knowledge-Bank`

## 6. Hub 关系

总索引不在本仓 → [danying-apps INDEX](https://github.com/dymusiques/danying-apps/blob/main/INDEX.md)
