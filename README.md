# agent-troubleshoot-skill

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platforms](https://img.shields.io/badge/platforms-8-blue)
![Cases](https://img.shields.io/badge/cases-30-green)

**可学习的 Agent 故障排查知识库技能 | A learnable troubleshooting knowledge-base skill for AI coding agents**

适用于 Codex、Claude Code、OpenCode 等常用的 AI 助手（Agent）工具。
Works with any agent that supports the Agent Skills spec (Codex, Claude Code, OpenCode, etc.).

[中文](#简介中文) | [English](#overview-english)

---

## 简介（中文）

一个**可学习的 Agent 故障排查知识库**，核心功能：

1. **故障诊断**：根据错误症状（错误码、框架名、关键词）匹配历史案例，输出带置信度的解决方案
2. **自动学习**：问题解决后自动归档新案例到知识库（Jaccard 语义去重、多解法合并）
3. **两级分类**：「共同问题」是任何框架都可能遇到的（如 401 认证失败、429 限流）；「独有问题」是只在某个框架自身工具链里才存在的故障（例如 `azd` 部署错误只可能发生在微软 Foundry 上）
4. **收录有门槛**：用户确认问题解决后才允许入库；应用程序接口（API）密钥、端口、路径等敏感信息一律不收录

> **🔒 两句安心话**
> - **你的敏感信息不会被收录**：API 密钥、令牌、端口、本机路径等，入库前都会自动删掉或替换掉
> - **错误方案不会被收录**：只有你确认问题真正解决后，案例才会写入知识库

预置 8 个平台共 30 个案例：

| 类别 | 示例 |
|---|---|
| 共同问题 | 401 鉴权失败、429 限流、上下文溢出、网络超时、模型不存在 |
| Antigravity 独有 | 浏览器控制失败（Chrome/扩展）、工件与任务列表同步失败 |
| Claude 独有 | artifact 渲染崩溃、shell 命令找不到、权限拒绝 |
| Codex 独有 | 模型上下文协议（MCP）服务器缺失、单模型上游慢导致超时、切换模型失败 |
| Foundry 独有（微软 Azure AI 平台） | azd 部署失败、trace 导出失败、missing agent.yaml |
| Gemini 独有 | 思考预算耗尽、图片上传失败、日配额用尽 |
| OpenCode 独有 | 自定义 provider 配置不生效、崩溃后会话恢复失败 |
| Reasonix 独有 | 推理链断裂（深度超限）、工具循环调用 |
| ZCode 独有 | 技能不触发、hook 失效、MCP 断连、插件缺失 |

### 安装

适用于任何支持技能机制的 Agent（Codex / Claude Code / OpenCode 等）。**复制下面这一行发送给您的 AI 即可：**

> 帮我安装 agent-troubleshoot 技能，项目地址：https://github.com/XCZ-Huazhou/agent-troubleshoot-skill ，下载放入我的技能目录并完成本机配置。

---

**⚠️ 安装后配置清单** *（以下是说明文字，无需复制发送）*
为了更好地让该技能处理本机遇到的各种 agent bug，安装完成后请让 AI 助手逐项确认：

- **Python 解释器路径**（pixi / conda / 系统环境均可）：运行 `diagnose.py` 与自检所必需
- **本机各 Agent 的配置与日志位置**（如 `~/.codex/config.toml`、`~/.claude/`）：排查框架专属故障时必需
- **本机网络 / 代理端口**：诊断网络类故障时必需

**💡 列表里没有你的 Agent？** 无需等待更新——直接让您的 AI 大模型参照知识库现有案例的四个字段（症状 symptoms、根因 rootCause、解决方案 solution、预防 prevention）自行补充新平台的故障案例，并在 `frameworks` 中登记即可。

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

## Overview (English)

A **learnable troubleshooting knowledge base** for AI coding agents:

1. **Diagnose**: matches error symptoms (error codes, framework names, keywords) against archived cases and returns ranked solutions with confidence scores
2. **Self-learning**: resolved cases are auto-archived with Jaccard-based deduplication and multi-solution merging
3. **Two-level taxonomy**: cross-framework *common issues* (e.g. 401 auth, 429 rate limit — any agent can hit them) vs per-framework *unique issues* (failures that only exist inside one framework's own toolchain, e.g. an `azd` deployment error can only happen on Microsoft Foundry)
4. **Gated archiving**: cases enter the knowledge base only after you confirm the issue is actually resolved; sensitive info (API keys, ports, local paths) is never written in — safe to share publicly

> **🔒 Two promises**
> - **Your secrets are never recorded**: API keys, tokens, ports and local paths are always removed or replaced before anything enters the knowledge base
> - **Wrong fixes are never recorded**: cases are archived only after you confirm the issue is truly resolved

Ships with 30 pre-loaded cases across 8 platforms:

| Category | Examples |
|---|---|
| Common | 401 auth failed, 429 rate limit, context overflow, network timeout, model not found |
| Antigravity-specific | browser control failure (Chrome/extension), artifact & task-list sync failure |
| Claude-specific | artifact render crash, shell command not found, permission denied |
| Codex-specific | Model Context Protocol (MCP) server missing, single slow upstream model causing timeout, model switching failure |
| Foundry-specific（Microsoft Azure AI） | azd deployment failure, trace export failure, missing agent.yaml |
| Gemini-specific | thinking budget exceeded, image upload failed, daily quota exhausted |
| OpenCode-specific | custom provider config not applied, session restore failure after crash |
| Reasonix-specific | reasoning chain broken (max depth exceeded), tool loop / repeated tool calls |
| ZCode-specific | skill not triggering, hook not firing, MCP disconnected, plugin missing |

### Install

Works with any skills-capable agent (Codex / Claude Code / OpenCode, etc.). **Copy & send just this line to your AI:**

> 帮我安装 agent-troubleshoot 技能，项目地址：https://github.com/XCZ-Huazhou/agent-troubleshoot-skill ，下载放入我的技能目录并完成本机配置。

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

## Compatibility

- All files are UTF-8; output is safe on Windows GBK consoles (emoji/Chinese fallback)
- Python 3.7+ standard library only — **any interpreter works** (pixi / conda / system Python), just specify the path explicitly at runtime

## Contributing · 贡献

欢迎补充新故障案例，两种方式任选：

- **提交 Issue（问题反馈，推荐，无需会写代码）**：Issues 页选择「新故障案例」模板，按提示填写平台 / 症状 / 根因 / 解决方案即可，会由维护者审核后入库
- **提交拉取请求（Pull Request，简称 PR）**：直接编辑 `knowledge-base.json` 追加案例（请省略 `id` 字段，由维护者统一编号）

> ⚠️ **隐私红线**：任何内容（包括粘贴的报错日志）都不得包含 API 密钥、令牌、端口、内网地址、真实本地路径。

字段说明、审核流程等详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## Disclaimer · 免责声明

> 本技能由 OpenCode 平台的 OX Alpha 模型整理、发布，技能跟内容描述可能存在不完善之处，敬请见谅！
>
> This skill was curated and published by **OX Alpha**, an AI model on the **OpenCode** platform. The skill and its content description may be imperfect in places — thank you for your understanding!

## License

MIT
