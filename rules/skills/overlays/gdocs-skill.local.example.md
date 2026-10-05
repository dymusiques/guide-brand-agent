# gdocs-skill — Local Overlay (example)

Copy to `gdocs-skill.local.md` in this directory and adjust paths for your machine.

```bash
cp rules/skills/overlays/gdocs-skill.local.example.md rules/skills/overlays/gdocs-skill.local.md
```

The `.local.md` file is gitignored. Never put credential JSON contents in markdown — only paths.

## Workspace Paths

| Key | Value |
|-----|-------|
| Workspace root | `<YOUR_CLONE_PATH>/guide-brand-agent` |
| Vendored repo | `vendor/gdocs-skill/` |
| Secrets dir | `vendor/gdocs-skill/secrets/` |
| Gmail cache | `vendor/gdocs-skill/data/mail/` |
| Python venv | `.venv/` (workspace root) |

## Activation

```bash
cd <YOUR_CLONE_PATH>/guide-brand-agent
source .venv/bin/activate
python -m gdocs --secrets-dir vendor/gdocs-skill/secrets <subcommand> ...
```

## OAuth (one-time)

1. Save Desktop OAuth JSON as `vendor/gdocs-skill/secrets/credentials.json` (`chmod 600`)
2. Smoke test: `python -m gdocs --secrets-dir vendor/gdocs-skill/secrets create --title "Smoke test"`
3. Browser opens once; `token.json` is written beside credentials

## Knowledge Bank (Drive folder IDs)

Root: `1jLcbbr0WkmEI8mJlsf5R4Y1NtSGEP8_c`

| Folder | ID |
|--------|-----|
| `AI-Agent-Knowledge-Bank/` (root) | `1jLcbbr0WkmEI8mJlsf5R4Y1NtSGEP8_c` |
| `00-soul/` | `1dUI7qgJ2AO_Hhums5rYuquRXNqjHcrcz` |
| `01-owner/` | `1egKSUCZ1rZQdWx31fSEkM9Ca4G5FZA0n` |
| `02-personal-ip/` | `1mHUIRTHVQ7yXym5Yk-AajfpMdxBq65P1` |
| `03-business-brand/` | `1LNCj-rzkUQDqyosryTtbxW_YidNO9kWa` |
| `04-marketing/` | `1e6ZoJNtMUT_7O3gipFWhsSYnZsPkXyQb` |
| `05-xiaohongshu/` | `13pC9qFVGaHsvOHrnTwXeX65-MCCeIV3p` |
| `06-visual/` | `11RbVjxMWBaCDPasamt8jYH6IQu3uR5br` |
| `07-templates/` | `1UX7FGQPZfRpM6ebe1pv0RVoQ9TUF6zVj` |
| `99-examples/` | `1ph0_9P8iYEDFkda7rYmjwNXkemLaK4Hv` |
