# Skill Router: B 站投稿填表（bilibili-upload）

> **边界：** 填表至 **「立即投稿」前**；**Owner 扫码登录 + 手点发布**。见 [bilibili-inst360-channel-adoption.md](../../integration/bilibili-inst360-channel-adoption.md)。

1. **Overlay:** `rules/skills/overlays/bilibili-upload.local.example.md`
2. **Root skill:** `vendor/bilibili-upload-skill/skills/bilibili-upload/SKILL.md`
3. **Adoption:** [ip-content-skills-adoption.md](../../integration/ip-content-skills-adoption.md)

触发词："B 站投稿"、"bili-upload"、"哔哩哔哩 fill"。

```bash
source scripts/ensure-workspace-venv.sh
pip install -e vendor/bilibili-upload-skill   # 首次
playwright install chromium                  # 首次 · verify-ip-skills-env 会查
# 首次只 dry-run fill；完整 execute 需 Owner 在场 · 可见 Chrome + Owner 扫码
```
