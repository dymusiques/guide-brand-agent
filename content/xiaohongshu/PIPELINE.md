# content/xiaohongshu/ 管线

Git 真相源下的 **小红书选题 → Brief → Gemini 对齐 → 定稿 commit** 流程。Kernel / Skill 已就绪；本文件定义 **重复执行** 时的状态与命令。

## 在总顺序中的位置

```
Kernel (6 case) → Topic Manager Skill → 单篇 Brief 闭环 ✅
→ 【本管线】文档 + 批量 verify + 交班习惯
→ brand-visual（封面）→ 可选 Drive → P 层 KPI 复盘
```

## 文件约定

| 项 | 规则 |
|----|------|
| **命名** | `YYYY-MM-DD-<slug>-brief.md` |
| **模板** | [kernels/templates/xhs-content-brief.template.md](../../kernels/templates/xhs-content-brief.template.md) |
| **Classifier** | 必须含 `<!-- xhs-classifier -->` + JSON 的 `subject` / `body` |
| **Verify log** | Brief 末尾记录每次 `evaluate` 结果（日期、版本、aligned、exit code） |

### 状态（人工标记，写在 Brief「与品牌」或 Verify log）

| 状态 | 含义 | 允许的动作 |
|------|------|------------|
| **draft** | 文案或未 evaluate | 可改 JSON；不可称定稿、不可 sync Drive |
| **verified** | `evaluate --brief` → `aligned: true` | 可 commit；仍非最终发布稿 |
| **定稿** | Owner 确认 + **已 git commit** | 可交 `brand-visual`；Owner 要求时可 sync Drive |

## 单篇流程（必会）

1. 复制模板 → 填 Brief + **同步改 classifier JSON**  
2. 单条验收：  
   `python scripts/evaluate-xhs-topic.py --brief content/xiaohongshu/<file>.md`  
3. **`aligned: true`** → 更新 Verify log → **git commit**  
4. 封面需求 → `.cursor/skills/brand-visual/`  
5. **仅** Owner 说「同步 Drive」→ `05-xiaohongshu/`（overlay folder ID）

正式路径用 **`--brief`**，不用裸 `--subject/--body` 代替定稿。

## 批量流程（交班 / 发版前）

扫描目录内所有 `*-brief.md`：

```bash
bash scripts/verify-xhs-content-dir.sh
```

- 每篇调用与单条相同的 `evaluate-xhs-topic.py --brief`  
- 任一篇 **未 aligned** 或 **API/格式错误** → 脚本 exit 1  
- 需要 `Guide/0/.env` 中 `GEMINI_API_KEY`（与 kernel 6 case 相同）

## 与 kernel 6 case 的分工

| 命令 | 何时跑 |
|------|--------|
| `bash scripts/verify-xhs-topic.sh` | 修改 `kernels/xiaohongshu/line2/` 或 classifier 规则后 |
| `bash scripts/verify-xhs-content-dir.sh` | 新增/改 Brief 后、交班前、发版前 |
| `python scripts/evaluate-xhs-topic.py --brief …` | 单篇改稿循环 |

## 交班清单（Agent）

1. `bash scripts/verify-handoff.sh`  
2. 若有 `content/xiaohongshu/*-brief.md`：`bash scripts/verify-xhs-content-dir.sh`  
3. 改过 kernel：`bash scripts/verify-xhs-topic.sh`  
4. （有 OAuth 时）`bash scripts/verify-integration.sh`  

## 红线（勿提前做）

- 不要把粉丝数 **5000/10k** 写进 classifier 单测  
- **未 aligned** 不要 sync Drive  
- **不要** 只写 Drive 不 commit Git  

## 相关链接

- Skill：[.cursor/skills/xiaohongshu/topic-manager.md](../../.cursor/skills/xiaohongshu/topic-manager.md)  
- Kernel：[kernels/xiaohongshu/README.md](../../kernels/xiaohongshu/README.md)  
- 路由：[integrations/index.md](../../integrations/index.md)
