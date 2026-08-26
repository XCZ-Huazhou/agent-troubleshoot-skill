# agent-troubleshoot-skill

Agent 故障排查知识库技能 —— 一个**可学习的 Agent 故障诊断知识库**，适用于 Codex / Claude Code / opencode 等支持 Agent Skills 规范的 CLI 工具。

## 功能

1. **故障诊断**：根据错误症状（错误码、框架名、关键词）匹配历史案例，输出带置信度的解决方案
2. **自动学习**：问题解决后自动归档新案例到知识库（Jaccard 语义去重、多解法合并）
3. **分类检索**：「共同问题」（跨框架）与「框架独有问题」两个维度

预置 24 个案例：401 鉴权、429 限流、上下文溢出、网络超时、模型不存在等共同问题，以及 Codex MCP、单模型上游慢、ZCode 技能不触发、Gemini 思考预算、Foundry 配额等独有问题。

## 安装

将本目录复制（或 symlink/junction）到 Agent 的技能目录：

```
~/.agents/skills/agent-troubleshoot/
├── SKILL.md              # 技能定义与工作流
├── knowledge-base.json   # 知识库（案例会持续积累）
├── diagnose.py           # 命令行诊断入口
└── utils/matcher.py      # 关键词提取 / Jaccard 匹配 / 去重
```

## 使用

```bash
# 命令行直接诊断
python diagnose.py "Codex 报 401 错误"
python diagnose.py "Claude 429 rate limit"

# 运行自检
python utils/matcher.py
```

或在支持 skills 的 Agent 中自动触发：对话中提到「Agent 报错 / 排查 / 401 / timeout / MCP server not found」等关键词即可。

## 知识库结构

```json
{
  "common-issues": { "auth-errors": { "symptoms": [], "rootCause": "", "solutions": {} } },
  "frameworks": {
    "Codex": { "unique-issues": [ { "id": "CODEX-001", ... } ] }
  },
  "metadata": { "totalCases": 24 }
}
```

- 每次更新知识库前自动备份 `knowledge-base.json.bak`
- 新案例入库前做语义去重（相似度 > 0.8 合并进现有案例）

## 兼容性说明

- 所有文件为 UTF-8 编码；Windows GBK 控制台下已做 emoji/中文输出兼容处理
- Python 3.7+，无第三方依赖

## License

MIT
