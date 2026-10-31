---
context_version: "2026-10-30-l012"
repo_path: ".cursor/skills/personal-ip/SKILL.md"
goal: "Personal IP"
openwebui_route: "rag_l2"
cursor_route: "read"
content_sha256: "82bb569d51342032"
---

# Personal IP

## L1 任务（压缩 · Open WebUI / Cursor 顶栏）
- **Goal:** 1. `content/personal-ip/2026-10-18-key-person-of-influence-capstone-playbook.md`（KPI · CAPSTONE · Pitch/Publish/Product）
2. `content/personal-ip/ip-positioning-brief-2026-10-05.md`
- **Path:** `.cursor/skills/personal-ip/SKILL.md`
- **Open WebUI:** `rag_l2`
- **Cursor:** `read`

## 章节锚点
- **读什么**: 1. `content/personal-ip/2026-10-18-key-person-of-influence-capstone-playbook.md`（KPI · CAPSTONE · Pi…
- **存储默认规则**: 与 [docs/HANDOFF-COMPLETENESS.md](../../../docs/HANDOFF-COMPLETENESS.md) 一致：
- **产出**: - IP 定位陈述（一句话 + 三支柱 + 差异化）
- **验收**: - [ ] 与现有 Danying 品牌不冲突


---

## L2 正文

# Personal IP

## 读什么

1. `content/personal-ip/2026-10-18-key-person-of-influence-capstone-playbook.md`（KPI · CAPSTONE · Pitch/Publish/Product）
2. `content/personal-ip/ip-positioning-brief-2026-10-05.md` + `rules/USER.md`
3. `guide-core/soul.md` + `guide-core/user.md`
4. Git `content/personal-ip/` 其余定稿（真相源，优先）
5. Drive `02-personal-ip/`（仅 Owner 已同步定稿时查阅）
6. `kernels/templates/ip-positioning-brief.template.md`

## 存储默认规则

与 [docs/HANDOFF-COMPLETENESS.md](../../../docs/HANDOFF-COMPLETENESS.md) 一致：

1. **草稿** → 写 `content/personal-ip/`
2. **稳定 / 定稿** → git commit（Owner 说「定稿」或段落完成时）
3. **Drive** → 仅 Owner 说「同步 Drive」→ 写入 `02-personal-ip/`
4. **禁止** → 只写 Drive 不 commit；未 commit 就称交班完成

交班前：`bash scripts/verify-handoff.sh`

## 产出

- IP 定位陈述（一句话 + 三支柱 + 差异化）
- 目标受众画像
- 内容日历建议（与听见 Daily 协同）

## 验收

- [ ] 与现有 Danying 品牌不冲突
- [ ] 可执行（至少 2 周内容方向清晰）
- [ ] 已写入 `content/personal-ip/` 且稳定后 commit
- [ ] （可选）Owner 说「同步 Drive」时已写入 `02-personal-ip/`