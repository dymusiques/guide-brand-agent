# Double-Check Subagent · CEO 轨（13-QC）

> **岗位：** 派活完成后、交付 Owner 前的 **专职复核**（Cursor Task，非 01–12 编制内干活 GM）。  
> **作业仓通用：** 见宿主仓 `docs/agent/DOUBLE-CHECK-AGENT.md`（若存在）。

---

## 1. 在指挥链中的位置

```text
Owner 目标
  → 00 CEO 写 dispatch / 派 01–12（顺序扮演）
  → 各步 terminal 验收脚本
  → 【13-QC · Task Double-Check】← 本文件
  → triple-eval / 6-case（若 brief）· HTML 弹出
```

**QC 插在：** GM 步与 **CEO 宣称交 Owner** 之间；**不**插在 04 写稿中途。

---

## 2. Must 核对（品牌专用 + 通用）

- dispatch 表每行 **验收命令是否已跑**、输出是否附在 GM-REPORT  
- `CEO-RUN-MANIFEST-latest.json` roster **invoked/skipped** 是否诚实（机械：`python3 scripts/verify-ceo-run-manifest.py --contract <monorepo>/docs/agent/AGENT-BRAND-CEO-ROSTER.json`）  
- Brief aligned / kernel / integration verify **无假 PASS**  
- 红队 / adversarial **不**被 QC 省略（已有则查文件存在）  
- Owner 交付格式 [`OWNER-CHAT-DELIVERY-FORMAT.md`](../../docs/OWNER-CHAT-DELIVERY-FORMAT.md)

---

## 3. 启动命令（主 Agent）

```text
Task · generalPurpose · run_in_background: false
prompt: 见 rules/skills/workflow_double_check_subagent.md（填入 slug、paths、verify 日志）
```

落盘：`tmp/double-check/<slug>/report.md` · 状态 **PASS | FAIL**

---

## 4. 与 B 类并行 Task 的区别

| | 调研 Task（可选） | 13-QC（Must） |
|--|-------------------|---------------|
| 时机 | 写 Brief **前** | 派活验收 **后** |
| 目的 | 搜集材料 | **否定/确认** 可交付 |
| 能否不写 | 可以 | **不可**（有交付时） |

---

*更新 AUTO-WORKFLOW 步 **3d**；名册见 `IP-SUBAGENT-ROSTER.md` 13-QC 行。*
