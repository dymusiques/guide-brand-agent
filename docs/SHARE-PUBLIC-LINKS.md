# 分享给鸭哥 · 公开链接（Private 仓 404 时用）

主仓库 **Private** 时，`github.com/dymusiques/guide-brand-agent/...` 对无权限的人会显示 **404**。

## 可转发（公开 · 无需登录）

| 内容 | 链接 |
|------|------|
| 导读 + 导图（同一 Gist） | https://gist.github.com/dymusiques/1efd20ba040828b8e9def78de9e56672 |
| 交互思维导图 HTML | https://htmlpreview.github.io/?https://gist.githubusercontent.com/dymusiques/1efd20ba040828b8e9def78de9e56672/raw/owner-stack-openwebui-mindmap.html |

## 若希望 GitHub 仓链接也可直接打开

任选其一：

1. **邀请鸭哥** 为仓库 collaborator（Settings → Collaborators，需他的 GitHub 账号）
2. **改为 Public 仓**（整仓对外可见；确认无密钥后再做）

```bash
# 仅 Owner 在 Terminal 确认后执行
gh repo edit dymusiques/guide-brand-agent --visibility public --accept-visibility-change-consequences
```
