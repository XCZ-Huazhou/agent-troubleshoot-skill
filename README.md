# agent-troubleshoot-skill

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platforms](https://img.shields.io/badge/platforms-8-blue)
![Cases](https://img.shields.io/badge/cases-30-green)

**A learnable troubleshooting knowledge-base skill for AI coding agents | 可学习的 Agent 故障排查知识库技能**

Works with any agent that supports the Agent Skills spec (Codex, Claude Code, opencode, etc.).
适用于 Codex / Claude Code / opencode 等支持 Agent Skills 规范的 CLI 工具。

[English](#overview-english) | [中文](#简介中文)

---

## Overview (English)

A **learnable troubleshooting knowledge base** for AI coding agents:

1. **Diagnose**: matches error symptoms (error codes, framework names, keywords) against archived cases and returns ranked solutions with confidence scores
2. **Self-learning**: resolved cases are auto-archived with Jaccard-based deduplication and multi-solution merging
3. **Two-level taxonomy**: cross-framework *common issues* (e.g. 401 auth, 429 rate limit — any agent can hit them) vs per-framework *unique issues* (failures that only exist inside one framework's own toolchain, e.g. an `azd` deployment error can only happen on Microsoft Foundry)

Ships with 30 pre-loaded cases across 8 platforms:

| Category | Examples |
|---|---|
| Common | 401 auth failed, 429 rate limit, context overflow, network timeout, model not found |
| AntiGravity-specific | browser control failure (Chrome/extension), artifact & task-list sync failure |
| Claude-specific | artifact render crash, shell command not found, permission denied |
| Codex-specific | MCP server missing, single slow upstream model causing timeout, /model switch failure |
| Foundry-specific（Microsoft Azure AI） | azd deployment failure, trace export failure, missing agent.yaml |
| Gemini-specific | thinking budget exceeded, image upload failed, daily quota exhausted |
| OpenCode-specific | custom provider config not applied, session restore failure after crash |
| Reasonix-specific | reasoning chain broken (max depth exceeded), tool loop / repeated tool calls |
| ZCode-specific | skill not triggering, hook not firing, MCP disconnected, plugin missing |

### Install

Copy (or symlink) this directory into your agent's skills directory:

```
~/.agents/skills/agent-troubleshoot/
├── SKILL.md              # skill definition & workflow
├── knowledge-base.json   # knowledge base (keeps growing)
├── diagnose.py           # CLI diagnosis entry
└── utils/matcher.py      # keyword extraction / Jaccard matching / dedup
```

> **⚠️ Post-install setup (required)**: After installing, ask **your own AI assistant** to
> adapt this skill to your machine — Python interpreter path (pixi / conda / system),
> network proxy ports, local knowledge-base storage path, etc. These differ on every machine;
> using the skill unadapted may prevent it from working correctly.

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
  "metadata": { "totalCases": 30 }
}
```

- The knowledge base is backed up automatically (`knowledge-base.json.bak`) before every update
- New cases with similarity > 0.8 are merged into existing ones

---

## 简介（中文）

一个**可学习的 Agent 故障排查知识库**，核心功能：

1. **故障诊断**：根据错误症状（错误码、框架名、关键词）匹配历史案例，输出带置信度的解决方案
2. **自动学习**：问题解决后自动归档新案例到知识库（Jaccard 语义去重、多解法合并）
3. **两级分类**：「共同问题」是任何框架都可能遇到的（如 401 认证失败、429 限流）；「独有问题」是只在某个框架自身工具链里才存在的故障（例如 `azd` 部署错误只可能发生在微软 Foundry 上）

预置 8 个平台共 30 个案例：

| 类别 | 示例 |
|---|---|
| 共同问题 | 401 鉴权失败、429 限流、上下文溢出、网络超时、模型不存在 |
| AntiGravity 独有 | 浏览器控制失败（Chrome/扩展）、工件与任务列表同步失败 |
| Claude 独有 | artifact 渲染崩溃、shell 命令找不到、权限拒绝 |
| Codex 独有 | MCP server 缺失、单模型上游慢导致超时、/model 切换失败 |
| Foundry 独有（微软 Azure AI 平台） | azd 部署失败、trace 导出失败、missing agent.yaml |
| Gemini 独有 | 思考预算耗尽、图片上传失败、日配额用尽 |
| OpenCode 独有 | 自定义 provider 配置不生效、崩溃后会话恢复失败 |
| Reasonix 独有 | 推理链断裂（深度超限）、工具循环调用 |
| ZCode 独有 | 技能不触发、hook 失效、MCP 断连、插件缺失 |

### 安装

将本目录复制（或 symlink/junction）到 Agent 的技能目录 `~/.agents/skills/agent-troubleshoot/` 即可。

> **⚠️ 安装后配置（必读）**：安装完成后，请让**您自己的 AI 助手**根据本机实际环境完成适配——
> 包括 Python 解释器路径（pixi / conda / 系统环境自选）、网络代理端口、知识库本地存储路径等。
> 每台机器的端口与环境各不相同，未经适配直接使用可能无法正常工作。

### 使用

```bash
# 命令行直接诊断
python diagnose.py "Codex 报 401 错误"
python diagnose.py "Claude 429 rate limit"

# 运行自检
python utils/matcher.py
```

在支持 skills 的 Agent 中可自动触发：对话中提到「Agent 报错 / 排查 / 401 / timeout」等关键词即可。

### 知识库格式

```json
{
  "common-issues": { "auth-errors": { "symptoms": [], "rootCause": "", "solutions": {} } },
  "frameworks": {
    "Codex": { "unique-issues": [ { "id": "CODEX-001" } ] }
  },
  "metadata": { "totalCases": 30 }
}
```

- 每次更新知识库前自动备份 `knowledge-base.json.bak`
- 新案例相似度 > 0.8 时自动合并进已有案例

---

## Compatibility

- All files are UTF-8; output is safe on Windows GBK consoles (emoji/Chinese fallback)
- Python 3.7+ standard library only — **any interpreter works** (pixi / conda / system Python), just specify the path explicitly at runtime

## Contributing · 贡献

Issues and pull requests are welcome — especially new troubleshooting cases for the knowledge base.
欢迎提交 Issue 与 PR，尤其是补充新的故障案例到知识库。

## Disclaimer · 免责声明

> 本技能由 opencode 平台的 OX Alpha 模型整理、发布，技能可能存在不完善之处，敬请见谅！
>
> This skill was curated and published by **OX Alpha**, an AI model on the **opencode** platform. It may be imperfect in places — thank you for your understanding!

## License

MIT
