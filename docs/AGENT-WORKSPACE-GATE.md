# 工作区门禁（品牌仓 · Agent 必读）

> **brand-ceo 任务**：git 顶目录 **必须** 为本仓 `danying-brand-agent`。  
> **机械校验**（在**本仓根**执行）：

```bash
python3 "/Users/danying/Desktop/未命名/scripts/assert-task-workspace.py" -t brand-ceo
```

- **PASS** → 继续 CEO MANDATE / pipeline / 3d QC  
- **FAIL** → Cursor **Open Folder** 本仓，勿在作业仓改 CEO 真源  

真源文档：作业仓 `docs/agent/WORKSPACE-GATE.md` · 表 `AGENT-STEP-01-WORKSPACE-REGISTRY.json`（旧名 `TASK-WORKSPACE-REGISTRY.json` 已废弃）
