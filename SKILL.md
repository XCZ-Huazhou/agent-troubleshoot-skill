---
name: agent-troubleshoot
description: >-
  Agent 故障排查知识库，支持 Codex/Claude/ZCode/Gemini/Foundry/Reasonix/Antigravity/OpenCode 等框架的常见问题诊断。
  自动学习用户遇到的 bug，形成可检索的知识库，下次遇到相似问题时快速匹配解决方案。
  触发关键词：Agent 报错、故障排查、诊断、401、429、timeout、rate limit、context limit、MCP server、skill not triggering 等。
  A learnable troubleshooting knowledge base for AI coding agents (Codex, Claude Code,
  ZCode, Gemini, Foundry, Reasonix, Antigravity, OpenCode): diagnoses common failures
  from error symptoms and auto-archives resolved cases for future matching.
  Triggers: agent error, troubleshoot, diagnose, 401, 403, 429, timeout, rate limit,
  context limit, MCP server not found.
---

# Agent Troubleshoot Skill - 可学习的故障排查知识库

> **⚠️ 首次安装必读**：为了更好地让该技能处理本机遇到的各种 agent bug，安装完成后请让您的
> AI Agent 完成以下初始化：
> 1. **全盘智能扫描 Python 解释器**：运行技能自带的 `pick_python.py --deep`（限时深度扫描，
>    自动跳过 Windows、回收站、node_modules 等无关目录），发现所有可用环境后**弹出点击式
>    选择框**，用户鼠标点选一个作为默认——结果自动保存到 `.python_default.json`；
> 2. **自动读取**本机各 Agent 的配置与日志位置（如 ~/.codex/config.toml、~/.claude/ 等），
>    无需用户手动指定；
> 3. **自动读取**本机网络 / 代理端口设置，无需用户提供。
>
> **💡 扩展提示**：若您使用的 Agent 平台不在支持列表中，可让您的 AI 大模型参照知识库
> 现有案例格式（symptoms / rootCause / solution / prevention）自行补充新平台条目，
> 并在 frameworks 与 metadata 中登记。

## 技能定位

本技能是一个**可学习的 Agent 故障排查知识库**，核心功能：

1. **故障诊断**：根据用户描述的错误症状，匹配知识库中的历史案例，输出解决方案
2. **自动学习**：问题解决后，自动将新案例归档到知识库（去重检查）
3. **分类检索**：支持按「问题类型」（共同问题/独有问题）和「Agent 框架」两个维度检索

---

## 触发条件

### 语义触发（满足任一条件即激活）

1. **错误码出现**：对话中包含 `401`、`403`、`429`、`500` 等 HTTP 错误码
2. **框架名 + 故障词**：
   - 「Codex/Claude/ZCode/Gemini/Foundry」+ 「报错/失败/error/failed/不 work」
   - 「Agent」+ 「诊断/排查/怎么修/怎么办」
3. **典型症状关键词**：
   - 认证类：`Authentication failed`、`Unauthorized`、`登录失败`、`token 过期`
   - 限流类：`429`、`rate limit`、`quota exceeded`、`速率限制`
   - 上下文类：`context limit`、`token overflow`、`上下文溢出`
   - 网络类：`timeout`、`connection failed`、`连接超时`
   - 特定框架：`MCP server not found`、`skill not triggering`、`artifact render failed`
4. **命令式触发**：用户使用 `/agent-fix`、`/diagnose`、` 排查 Agent 问题`

### 文件触发

- 当用户上传包含错误日志的 `.log` 文件、traceback 截图、或错误信息文本时

---

## 核心工作流

```
用户报告故障
  ↓
【步骤 1】提取关键词（错误码、框架名、症状描述）
  ↓
【步骤 2】优先匹配「common-issues」共同问题分类
  ↓
【步骤 3】如果无匹配，在对应框架的「unique-issues」中查找
  ↓
【步骤 4】输出解决方案（带置信度）
  ↓
【步骤 5】用户确认解决 → 自动归档到知识库（去重检查）
```

---

## 诊断逻辑

### 问题分类规则

| 问题类型 | 判断标准 | 存储位置 |
|---------|---------|---------|
| **共同问题** | 3 个以上框架共有（如 401 鉴权、429 限流） | `common-issues` 分类 |
| **独有问题** | 特定框架特有（如 Codex MCP、ZCode skill trigger） | `frameworks.{Agent}.unique-issues` |

### 匹配算法

```python
def match_issue(user_input, knowledge_base):
    # 1. 提取框架名（Codex/Claude/ZCode/Gemini/Foundry）
    framework = extract_framework(user_input)
    
    # 2. 提取症状关键词
    symptoms = extract_symptoms(user_input)
    
    # 3. 优先匹配共同问题（计算症状相似度）
    for issue_id, issue in knowledge_base["common-issues"].items():
        if similarity(symptoms, issue["symptoms"]) > 0.7:
            return format_solution(issue, framework)
    
    # 4. 匹配框架独有问题
    if framework in knowledge_base["frameworks"]:
        for issue in knowledge_base["frameworks"][framework]["unique-issues"]:
            if similarity(symptoms, issue["symptoms"]) > 0.7:
                return format_solution(issue, framework)
    
    # 5. 无匹配 → 启动交互式诊断
    return start_interactive_diagnosis(user_input)
```

### 相似度计算（简化版）

```python
def similarity(keywords_a, keywords_b):
    """
    计算两组关键词的 Jaccard 相似度
    支持数字归一化（401 → "AUTH_ERROR"）
    """
    # 标准化：401/403 → "AUTH_ERROR", 429 → "RATE_LIMIT"
    normalized_a = normalize_keywords(keywords_a)
    normalized_b = normalize_keywords(keywords_b)
    
    # Jaccard 相似度 = 交集 / 并集
    intersection = len(set(normalized_a) & set(normalized_b))
    union = len(set(normalized_a) | set(normalized_b))
    
    return intersection / union if union > 0 else 0
```

---

## 学习逻辑

### 🚫 入库守门规则（硬性约束，优先级最高）

**在用户明确确认「问题已解决」之前，严禁将任何案例写入知识库。**

- ✅ 可以入库：用户明确回复「已解决」「解决了」「有效」「好使」等肯定表述
- ❌ 禁止入库：
  - 用户仅回复「谢谢」「好的」等致谢/敷衍语（不构成解决确认）
  - 用户表示「还是不行」「没解决」「报别的错了」
  - 用户未回应确认询问就结束了对话
- 🔁 用户反馈未解决时：不得入库；应追问新报错信息、更新诊断思路后重新给出方案
- 📋 入库前建议：先向用户复述将要收录的条目内容（症状/根因/方案），请其过目后再写入

### 🔐 入库隐私保护规则（硬性约束）

**知识库可能随项目被公开分享（如上传 GitHub）。收录案例时，任何人的敏感信息一律不得写入。**

- ❌ 禁止收录：
  - API 密钥 / 令牌 / 密码（**任何格式**，不限 `sk-` 前缀；混合大小写长串同样视为疑似密钥）
  - 内网地址、真实端口号、服务商内部域名
  - 真实用户名、机器路径（如 `C:\Users\<用户名>\...`、`D:\某盘\...`）
  - 可识别个人或组织身份的信息
- ✅ 替代写法：泛化描述或占位符，如「第三方 API 中转服务」「本地转发端口」「`<your-config-path>`」
- 📌 报错原文若包含上述敏感片段，须先截断或打码再收录
- 🧭 判断标准：假设这份知识库明天就会公开到互联网——任何你不想出现在公网的内容都不应写入

### 新案例入库规则

```
IF 问题类型已存在（语义相似度 > 0.8）:
  → 合并到现有案例（更新解决方案列表，保留多种解法）
  
ELSE IF 框架已存在但问题为新类型:
  → 添加到该框架的 unique-issues 数组
  
ELSE:
  → 创建新框架分类 + 新问题条目
```

### 去重策略

- **语义去重**：避免重复记录「401 错误」「Authentication failed」「Unauthorized」这类重复问题
- **自动合并**：同一问题有多个解法时，合并到同一案例的 `solutions` 数组
- **版本控制**：每次更新知识库前备份 `knowledge-base.json.bak`

---

## 输出格式

### 诊断报告模板

```markdown
## 🔍 诊断结果

**匹配案例**: `{issue_id}`（置信度：{confidence}%）

**问题分类**: {共同问题 / 框架独有问题}

**根本原因**: {rootCause}

---

### ✅ 解决方案

**通用方案**:
{solution["all"]}

**{framework} 特定建议**:
{solution[framework]}

---

### 🛠️ 诊断命令

```bash
{diagnosis_command}
```

---

### 📚 预防措施

{prevention}

---

> 问题解决了吗？回复「已解决」我将记录这个案例到知识库。
```

### 新问题交互式诊断模板

```markdown
## ⚠️ 未在知识库中找到完全匹配的案例

让我帮你逐步排查这个问题：

**步骤 1/3**: 请确认你使用的 Agent 框架是？
- [ ] Codex
- [ ] Claude
- [ ] ZCode
- [ ] Gemini
- [ ] Foundry
- [ ] 其他：____

**步骤 2/3**: 错误日志或截图是？（可直接粘贴）

**步骤 3/3**: 问题出现前你执行了什么操作？

---

我根据你的回答逐步诊断...
```

---

## 知识库结构

知识库文件路径：`~/.agents/skills/agent-troubleshoot/knowledge-base.json`

### JSON 结构

```json
{
  "common-issues": {
    "类别名": {
      "id": "问题 ID",
      "symptoms": ["症状关键词 1", "症状关键词 2"],
      "rootCause": "根本原因",
      "solutions": {
        "all": "通用方案",
        "框架名": "特定框架方案"
      },
      "diagnosis": "诊断命令",
      "prevention": "预防措施"
    }
  },
  "frameworks": {
    "框架名": {
      "description": "框架简介",
      "unique-issues": [
        {
          "id": "问题 ID",
          "symptoms": ["症状关键词"],
          "rootCause": "根本原因",
          "solution": "解决方案",
          "prevention": "预防措施"
        }
      ]
    }
  },
  "metadata": {
    "version": "版本号",
    "lastUpdated": "最后更新时间",
    "totalCases": "案例总数",
    "frameworks": ["支持的框架列表"]
  }
}
```

---

## 使用示例

### 示例 1：共同问题（401 鉴权错误）

**用户**：「Codex 一直报 401 错误」

**技能响应**：
```markdown
## 🔍 诊断结果

**匹配案例**: `COMMON-AUTH-001`（置信度：95%）

**问题分类**: 共同问题 - API 鉴权失败

**根本原因**: API 凭证过期或未配置

---

### ✅ 解决方案

**Codex 特定建议**:
执行 `codex login` 重新认证，或设置环境变量 `OPENAI_API_KEY`

---

### 🛠️ 诊断命令

```bash
codex auth status
```

---

问题解决了吗？回复「已解决」我将记录这个案例到知识库。
```

### 示例 2：独有问题（ZCode skill 未触发）

**用户**：「skill not triggering，技能未自动激活」

**技能响应**：
```markdown
## 🔍 诊断结果

**匹配案例**: `ZCODE-001`（置信度：90%）

**问题分类**: ZCode 独有问题

**根本原因**: 技能触发词匹配度不足

---

### ✅ 解决方案

手动调用 `/skill-name` 或调整 SKILL.md 的 description 字段增强匹配。

---

### 🛠️ 诊断命令

```bash
zcode skill list --verbose
```

---

### 📚 预防措施

使用 `skill-trigger-check` 技能验证触发条件。

---

问题解决了吗？回复「已解决」我将记录这个案例到知识库。
```

### 示例 3：新问题学习

**用户**：「Foundry 部署时报 subscription quota exceeded」

**技能响应**（未匹配到现有案例）：
```markdown
## ⚠️ 未在知识库中找到完全匹配的案例

让我帮你逐步排查这个问题：

**步骤 1/3**: 请确认具体报错信息是？（粘贴完整错误日志）

**用户**：「The request exceeded your subscription quota.」

**技能响应**：
```markdown
明白了，这是 Azure 订阅配额超限问题。

**解决方案**:
1. 运行 `azd auth login` 重新认证
2. 访问 Azure Portal 检查订阅配额使用情况
3. 使用 `azd quota request` 申请配额提升

---

问题解决了吗？如果已解决，我将记录这个案例到知识库：
- 框架：Foundry
- 症状：subscription quota exceeded
- 原因：Azure 订阅配额不足
- 方案：升级订阅或使用 azd quota request
```

---

## 维护指南

### 手动更新知识库

1. 编辑 `knowledge-base.json` 文件
2. 运行 `zcode skill reload agent-troubleshoot` 重新加载
3. 使用 `zcode skill test agent-troubleshoot` 验证触发

### 自动学习开关

在 `.zcode/config.json` 中配置：

```json
{
  "skills": {
    "agent-troubleshoot": {
      "autoLearn": true,  // 开启自动学习（默认）
      "requireConfirmation": true  // 入库前需要用户确认
    }
  }
}
```

---

## 扩展指南

### 添加新框架支持

1. 在 `knowledge-base.json` 的 `frameworks` 分类中添加新框架：

```json
"Reasonix": {
  "description": "Reasonix AI Agent Framework",
  "unique-issues": [
    {
      "id": "REASONIX-001",
      "symptoms": ["reasoning failed", "推理链断裂"],
      "rootCause": "推理步骤超过最大深度",
      "solution": "增加 max_reasoning_depth 配置或简化问题"
    }
  ]
}
```

2. 在 `common-issues` 中更新框架特定方案

### 添加新共同问题

如果某个问题在 3 个以上框架中出现，应添加到 `common-issues` 分类：

```json
"ssl-errors": {
  "id": "COMMON-SSL-001",
  "symptoms": ["SSL certificate verify failed", "证书验证失败"],
  "rootCause": "SSL 证书过期或 CA 证书路径未配置",
  "solutions": {
    "all": "更新 certifi 包，或设置 SSL_CERT_FILE 环境变量"
  }
}
```

---

## 运行环境（Python）

- `diagnose.py` 与 `utils/matcher.py` 仅依赖 **Python 3.7+ 标准库**，无第三方依赖；
- **解释器由用户自行选择**：pixi / conda / 系统 Python 均可，运行时显式指定路径即可；
- 默认解释器遵循本机配置（如 pixi / conda 管理），可自行指定

```bash
# 示例（替换为你自己的解释器）
python diagnose.py "Codex 报 401 错误"
```

---

## 版本历史

- **v1.0.0** (2026-08-26): 支持 8 个平台（Antigravity/Claude/Codex/Foundry/Gemini/OpenCode/Reasonix/ZCode）共 30 个案例；匹配器支持多词症状双向拆词与框架命中加成；提供中英文文档；内置「安装后需按本机环境自行适配」提示

- **v1.0.0** (2026-08-25): 初始版本，支持 Codex/Claude/ZCode/Gemini/Foundry 五大框架，预置 23 个常见案例

---

## 免责声明

本技能由 OpenCode 平台的 OX Alpha 模型整理、发布，技能跟内容描述可能存在不完善之处，敬请见谅！
