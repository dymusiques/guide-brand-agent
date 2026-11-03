# intake · 上下文由谁管

- source: owner chat 2026-11-03（重开 Agent，避免旧对话过长）
- drive_files: [{ "name": "小红书 IP 资料文件夹", "id": "1SrD2n_zXN2HjhH_YPbQa-_54YakKXbzZ" }]
- goal_one_line: 上下文要短，资料不丢；Cursor 管资料库记忆，Open WebUI 只防长文输出丢段
- entry: content/personal-ip/intake/2026-11-03-xhs-drive-corpus-L1.md

## 两件不同的事

1. **输入太长**（旧聊天、215 份长资料）：不要塞进一个 prompt。聊天只留 L1；每份资料用清单里的文件名和 Drive id 当地址；要用时打开那一份原件。
2. **输出太长**（一篇长文写到一半被模型跳过）：用分而治之。先说明全局任务，再声明「下面只处理这一段」，合并后抽查开头、中间、结尾。这是 Open WebUI 的 CoT / Diligent 该做的事。

## 裁定

- 小红书 IP 资料库的记忆、调度、背书引用：**Cursor + Git 卡片 + Drive 原件**。
- Open WebUI：只在单篇长输出时使用；RAG 若用来查一句事实，必须带回 Sources，再打开原件核对。
- 禁止把整库 embedding 或一份 MASTER 总摘录当作「已经读完」。

## 复核（2026-11-03）

- 2026-11-03 再次从 Drive 拉全：380 个文件，约 1.77 GiB，无子文件夹。旧清单 215 全部仍在，新增 165，删除 0。
- 本地 mirror 仍远少于 380。清单更新不等于正文已读。
- 已有种子摘录只覆盖 2 个文件，不能代表其余文件。

## 新资料怎么加

Owner 说文件名 → 在 manifest / L1 补一行地址。全文留在 Drive。不要把全文贴进聊天。

## 未解决

- [ ] 镜像 19/215，按任务单份下载，不为「读完」而全库灌进对话
- [ ] 真正要写某一篇时，只打开 1–3 个相关原件，引用写文件名
