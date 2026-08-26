# agent-troubleshoot-skill

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platforms](https://img.shields.io/badge/platforms-8-blue)
![Cases](https://img.shields.io/badge/cases-30-green)

**一个会不断成长的故障排查知识库技能 | A constantly-growing troubleshooting knowledge-base skill for AI coding agents**

适用于 Codex、Claude Code、OpenCode 等常用的 Agent 工具。
Works with any agent that supports the Agent Skills spec (Codex, Claude Code, OpenCode, etc.).

[中文](#简介中文) | [English](#overview-english)

---

## 简介（中文）

> 把踩过的坑都记下来，让AI遇到问题先翻笔记本，再动手修。

一个**会不断成长的 Agent 故障排查知识库**——基于确认过的排查经验持续积累，遇到历史同类故障时能快速识别并复用解决方案，显著缩短修复时间。

它的作用体现在三层：

| 层次 | 作用 | 说明 |
|---|---|---|
| **即时匹配** | 减少重复排查 | 遇到报错时自动检索知识库中相似的历史案例，直接给出解决方案和预防措施 |
| **统一入口** | 覆盖主流平台 | 一个技能覆盖 Codex、Claude、Gemini、ZCode、Foundry、OpenCode 等 8 大平台，不用针对每个平台单独找方案 |
| **持续积累** | 越用越强 | 每确认一个新案例，知识库就更扎实，形成正向循环 |

> **🔒 隐私与质量保障**
> - **你的敏感信息不会被收录**：API 密钥、令牌、端口、本机路径等，入库前都会自动删掉或替换掉
> - **错误方案不会被收录**：只有你确认问题真正解决后，案例才会写入知识库

核心功能：

1. **故障诊断**：根据错误症状（错误码、框架名、关键词）匹配历史案例，输出带置信度的解决方案
2. **智能学习**：问题解决后由用户确认，新案例归档到知识库（Jaccard 语义去重、多解法合并）
3. **两级分类**：「共同问题」是任何框架都可能遇到的（如 401 认证失败、429 限流）；「独有问题」是只在某个框架自身工具链里才存在的故障

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

**⚠️ 安装后初始化** *（以下是说明文字，无需复制发送）*
为了更好地让该技能处理本机遇到的各种 agent bug，安装完成后，它会自动做两件事：

- **确认Python的运行环境**：自动全盘智能扫描所有可用环境（pixi / conda / 系统等），**弹出点击式选择框**让你挑一个作为默认——运行`diagnose.py`与自检所必需
- **摸清你的Agent配置**：自动读取各Agent的设置与日志位置（如 `~/.codex/config.toml`、`~/.claude/`），以及上网代理端口，供后续排查使用，供后续排查使用

**💡 列表里没有你的 Agent？** 无需等待更新——直接让您的 AI 大模型参照知识库现有案例的四个字段（症状 symptoms、根因 rootCause、解决方案 solution、预防 prevention）自行补充新平台的故障案例，并在 `frameworks` 中登记即可。

### 使用

启用本技能后，若对话中提到「Agent 报错 / 排查 / 401 / timeout」等关键词即可自动触发诊断。每次修完，它都会先问一句「问题解决了吗」，等你确认后，才会把这条经验收进知识库。

### 知识库格式

```json
{
  "common-issues": {
    "auth-errors": {
      "id": "COMMON-AUTH-001",
      "symptoms": ["401", "认证失败"],
      "rootCause": "密钥过期或未配置",
      "solutions": { "通用": "重新登录或更换密钥" }
    }
  },
  "frameworks": {
    "Codex": {
      "unique-issues": [
        {
          "symptoms": ["报错关键词"],
          "rootCause": "问题成因",
          "solution": "已验证的解决步骤",
          "prevention": "预防措施（可选）"
        }
      ]
    }
  },
  "metadata": { "totalCases": 30 }
}
```

- 「共同问题」用 `solutions`（可按平台分别给方案）；「独有问题」用单个 `solution`
- 通过 Issue 或 PR 提交的新案例**无需填写 `id`**，收录时自动编号
- 每次更新知识库前自动备份 `knowledge-base.json.bak`
- 新案例相似度 > 0.8 时自动合并进已有案例

---

## Overview (English)

> Every pitfall you've hit gets written down. When AI sees a problem, it checks the notebook first, then fixes it.

A **constantly-growing troubleshooting knowledge base** for AI coding agents — it accumulates confirmed fixes over time, recognizes similar issues when they recur, and reuses proven solutions to dramatically cut repair time.

How it helps — three layers:

| Layer | What it does | How |
|---|---|---|
| **Instant match** | Skip repeated diagnosis | When an error hits, the KB is searched for similar past cases; solutions and prevention tips surface immediately |
| **Unified entry** | One skill, all platforms | Covers Codex, Claude, Gemini, ZCode, Foundry, OpenCode and more — 8 major frameworks under one roof |
| **Continuous growth** | Gets stronger with use | Every confirmed case makes the KB more complete; the more you use it, the faster it resolves |

> **🔒 Privacy & quality guarantees**
> - **Your secrets are never recorded**: API keys, tokens, ports and local paths are always removed or replaced before anything enters the knowledge base
> - **Wrong fixes are never recorded**: cases are archived only after you confirm the issue is truly resolved

Core features:

1. **Diagnose**: matches error symptoms (error codes, framework names, keywords) against archived cases and returns ranked solutions with confidence scores
2. **Smart learning**: resolved cases are archived only after user confirmation (Jaccard-based deduplication, multi-solution merging)
3. **Two-level taxonomy**: cross-framework *common issues* (e.g. 401 auth, 429 rate limit — any agent can hit them) vs per-framework *unique issues* (failures that only exist inside one framework's own toolchain)

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

**⚠️ Post-install init** *(reference only — do NOT copy-paste this part)*
To help the skill debug local agent issues effectively, after install it will automatically do two things:

- **Confirm the Python runtime**: full smart scan of every available environment (pixi / conda / system), then a **click-to-pick dialog** pops up for you to choose the default — needed to run `diagnose.py` and self-tests
- **Learn your agent setup**: automatically reads each agent's config/log locations (e.g. `~/.codex/config.toml`, `~/.claude/`) and your proxy ports for later troubleshooting

**💡 Using an agent not listed?** No need to wait for updates — ask your own AI to append cases for the new platform to `knowledge-base.json`, following the existing case format (symptoms / rootCause / solution / prevention), then register it under `frameworks`.

### Usage

Once the skill is enabled, it triggers automatically when keywords like "Agent error / troubleshoot / 401 / timeout" appear in the conversation. After each fix, it asks "Is the problem resolved?" — only after your confirmation will the case be added to the knowledge base.

### Knowledge base format

```json
{
  "common-issues": {
    "auth-errors": {
      "id": "COMMON-AUTH-001",
      "symptoms": ["401", "auth failed"],
      "rootCause": "expired or missing credentials",
      "solutions": { "general": "re-login or replace the key" }
    }
  },
  "frameworks": {
    "Codex": {
      "unique-issues": [
        {
          "symptoms": ["error keywords"],
          "rootCause": "why it happened",
          "solution": "verified fix steps",
          "prevention": "optional"
        }
      ]
    }
  },
  "metadata": { "totalCases": 30 }
}
```

- *Common issues* use `solutions` (per-platform fixes allowed); *unique issues* use a single `solution`
- New cases submitted via Issue or PR should **omit the `id` field** — it is assigned automatically
- The knowledge base is backed up automatically (`knowledge-base.json.bak`) before every update
- Near-duplicates (similarity > 0.8) are merged into existing cases

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

---

# ⚠️ 注明出处 · ATTRIBUTION REQUIRED

> ## 🔴 二次修改或引用，必须注明出处！
>
> ### 出处 / Source
>
> **[XCZ-Huazhou / agent-troubleshoot-skill](https://github.com/XCZ-Huazhou/agent-troubleshoot-skill)**
>
> When modifying or citing this skill, you **MUST** attribute the source:
>
> **XCZ-Huazhou / agent-troubleshoot-skill**
> https://github.com/XCZ-Huazhou/agent-troubleshoot-skill
