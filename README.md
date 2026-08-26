# agent-troubleshoot-skill

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platforms](https://img.shields.io/badge/platforms-8-blue)
![Cases](https://img.shields.io/badge/cases-30-green)

**A learnable troubleshooting knowledge-base skill for AI coding agents | 可学习的 Agent 故障排查知识库技能**

Works with any agent that supports the Agent Skills spec (Codex, Claude Code, opencode, etc.).
适用于 Codex / Claude Code / opencode 等支持 Agent Skills 规范的 AI Agent。

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

Works with any skills-capable agent (Codex / Claude Code / opencode, etc.). **Copy & send just this line to your AI:**

> 帮我安装 agent-troubleshoot 技能，项目地址：https://github.com/cjc505/agent-troubleshoot-skill ，下载放入我的技能目录并完成本机配置。

---

**⚠️ Post-install checklist** *(reference only — do NOT copy-paste this part)*
To help the skill debug local agent issues effectively, have your AI assistant confirm each item after install:

- **Python interpreter path** (pixi / conda / system): required to run `diagnose.py` and self-tests
- **Local config & log locations of your agents** (e.g. `~/.codex/config.toml`, `~/.claude/`): required for framework-specific diagnosis
- **Network / proxy ports**: required when debugging network-type failures

**💡 Using an agent not listed?** No need to wait for updates — ask your own AI to append cases for the new platform to `knowledge-base.json`, following the existing case format (symptoms / rootCause / solution / prevention), then register it under `frameworks`.

### Usage

Once the skill is enabled, it triggers automatically when keywords like "Agent error / troubleshoot / 401 / timeout" appear in the conversation.

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

适用于任何支持技能机制的 Agent（Codex / Claude Code / opencode 等）。**复制下面这一行发送给您的 AI 即可：**

> 帮我安装 agent-troubleshoot 技能，项目地址：https://github.com/cjc505/agent-troubleshoot-skill ，下载放入我的技能目录并完成本机配置。

---

**⚠️ 安装后配置清单** *（以下是说明文字，无需复制发送）*
为了更好地让该技能处理本机遇到的各种 agent bug，安装完成后请让 AI 助手逐项确认：

- **Python 解释器路径**（pixi / conda / 系统环境均可）：运行 `diagnose.py` 与自检所必需
- **本机各 Agent 的配置与日志位置**（如 `~/.codex/config.toml`、`~/.claude/`）：排查框架专属故障时必需
- **本机网络 / 代理端口**：诊断网络类故障时必需

**💡 列表里没有你的 Agent？** 无需等待更新——直接让您的 AI 大模型参照知识库现有案例格式（symptoms / rootCause / solution / prevention）自行补充新平台的故障案例，并在 `frameworks` 中登记即可。

### 使用

启用本技能后，若对话中提到「Agent 报错 / 排查 / 401 / timeout」等关键词即可自动触发技能。

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

Issues and pull requests are welcome — especially new troubleshooting cases.
欢迎提交 Issue 与 PR，尤其是补充新的故障案例。

**What to provide · 提交新案例请提供以下信息：**

| Item 项目 | Description 说明 |
|---|---|
| Platform 平台 | Which agent framework it belongs to（属于哪个框架，如 Codex / Claude / 其他新平台）|
| Symptoms 症状 | Exact error messages, error codes, keywords — both English & Chinese welcome（报错原文、错误码、关键词，中英文均可）|
| Root cause 根因 | Why it happened, if known（成因，若已知）|
| Solution 解决方案 | The steps that actually fixed it（实际验证有效的解决步骤）|
| Prevention 预防 | Optional · 可选 |

**File types / formats · 文件类型与格式：**

- **Easiest 最简单**: open an **Issue** and write the info above in plain text — the case will be formatted and merged into `knowledge-base.json` for you
  （直接开一个 Issue 用纯文本写清楚上表内容即可，会有人/AI 帮你格式化入库）
- **Via PR 走 PR**: edit `knowledge-base.json` directly, appending a new object under the matching platform's `unique-issues` (or create a new platform block), following the existing schema — `id` is auto-numbered, so leave it out or use the next number:
  （直接编辑 `knowledge-base.json`，在对应平台的 `unique-issues` 里按现有字段追加一个对象即可，`id` 会自动编号）

```json
{
  "symptoms": ["error message / 报错关键词"],
  "rootCause": "why it happened / 成因",
  "solution": "verified fix steps / 已验证的解决步骤",
  "prevention": "optional / 可选"
}
```

## Disclaimer · 免责声明

> 本技能由 opencode 平台的 OX Alpha 模型整理、发布，技能跟内容描述可能存在不完善之处，敬请见谅！
>
> This skill was curated and published by **OX Alpha**, an AI model on the **opencode** platform. The skill and its content description may be imperfect in places — thank you for your understanding!

## License

MIT
