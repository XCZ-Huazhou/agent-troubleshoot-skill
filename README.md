# agent-troubleshoot-skill

**可学习的 Agent 故障排查知识库技能 | A learnable troubleshooting knowledge-base skill for AI coding agents**

适用于 Codex / Claude Code / opencode 等支持 Agent Skills 规范的 CLI 工具。
Works with any agent that supports the Agent Skills spec (Codex, Claude Code, opencode, etc.).

[中文](#简介中文) | [English](#overview-english)

---

## 简介（中文）

一个**可学习的 Agent 故障排查知识库**，核心功能：

1. **故障诊断**：根据错误症状（错误码、框架名、关键词）匹配历史案例，输出带置信度的解决方案
2. **自动学习**：问题解决后自动归档新案例到知识库（Jaccard 语义去重、多解法合并）
3. **分类检索**：「共同问题」（跨框架）与「框架独有问题」两个维度

预置 24 个案例：

| 类别 | 示例 |
|---|---|
| 共同问题 | 401 鉴权失败、429 限流、上下文溢出、网络超时、模型不存在 |
| Codex 独有 | MCP server 缺失、单模型上游慢导致超时、/model 切换失败 |
| Claude 独有 | artifact 渲染崩溃、shell 命令找不到、权限拒绝 |
| ZCode 独有 | 技能不触发、hook 失效、MCP 断连、插件缺失 |
| Gemini 独有 | 思考预算耗尽、图片上传失败、日配额用尽 |
| Foundry 独有 | 部署失败、trace 导出失败、agent.yaml 缺失 |

### 安装

将本目录复制（或 symlink/junction）到 Agent 的技能目录：

```
~/.agents/skills/agent-troubleshoot/
├── SKILL.md              # 技能定义与工作流
├── knowledge-base.json   # 知识库（案例会持续积累）
├── diagnose.py           # 命令行诊断入口
└── utils/matcher.py      # 关键词提取 / Jaccard 匹配 / 去重
```

### 使用

```bash
# 命令行直接诊断
python diagnose.py "Codex 报 401 错误"
python diagnose.py "Claude 429 rate limit"

# 运行自检
python utils/matcher.py
```

在支持 skills 的 Agent 中可自动触发：对话中提到「Agent 报错 / 排查 / 401 / timeout」等关键词即可。

---

## Overview (English)

A **learnable troubleshooting knowledge base** for AI coding agents:

1. **Diagnose**: matches error symptoms (error codes, framework names, keywords) against archived cases and returns ranked solutions with confidence scores
2. **Self-learning**: resolved cases are auto-archived with Jaccard-based deduplication and multi-solution merging
3. **Two-level taxonomy**: cross-framework *common issues* + per-framework *unique issues*

Ships with 24 pre-loaded cases covering auth failures (401), rate limits (429), context overflow, network timeouts, missing models, MCP server issues, and more.

### Install

Copy (or symlink) this directory into your agent's skills directory:

```
~/.agents/skills/agent-troubleshoot/
```

### Usage

```bash
python diagnose.py "Codex 401 error"
python diagnose.py "Claude 429 rate limit"
python utils/matcher.py   # run self-tests
```

In skill-capable agents it triggers automatically on keywords like "agent error", "troubleshoot", "401", "timeout".

### Knowledge base format

```json
{
  "common-issues": { "auth-errors": { "symptoms": [], "rootCause": "", "solutions": {} } },
  "frameworks": {
    "Codex": { "unique-issues": [ { "id": "CODEX-001" } ] }
  },
  "metadata": { "totalCases": 24 }
}
```

- The knowledge base is backed up automatically (`knowledge-base.json.bak`) before every update
- New cases with similarity > 0.8 are merged into existing ones

---

## Compatibility

- All files are UTF-8; output is safe on Windows GBK consoles (emoji/Chinese fallback)
- Python 3.7+ standard library only — **any interpreter works** (pixi / conda / system Python), just specify the path explicitly at runtime

## License

MIT
