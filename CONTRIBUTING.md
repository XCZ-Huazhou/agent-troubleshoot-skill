# Contributing · 贡献指南

感谢关注 agent-troubleshoot！欢迎以任何形式参与：提交新故障案例、修正现有案例、改进文档或代码。

Thanks for your interest! Contributions of all kinds are welcome — new troubleshooting cases above all.

## 提交新案例 · Submitting a new case

### 方式一：开 Issue（推荐，无需会写代码）

1. 打开 [Issues](https://github.com/XCZ-Huazhou/agent-troubleshoot-skill/issues) → 选择「新故障案例」模板
2. 按模板填写：平台、症状、根因（若已知）、解决方案、预防（可选）
3. 提交即可 —— 维护者会审核、脱敏并合并进 `knowledge-base.json`

> ⚠️ **隐私红线**：任何内容（包括报错原文）都不得包含 API 密钥、令牌、端口、内网地址、真实本地路径。
> **Privacy first**: never include API keys, tokens, ports, internal addresses or real local paths — even inside pasted error logs.

### 方式二：提交 Pull Request（PR）

1. Fork 本仓库并创建分支
2. 编辑 `knowledge-base.json`：在对应平台的 `unique-issues` 数组末尾追加一个对象（也可新建平台块）
3. **请省略 `id` 字段** —— 由维护者统一编号，避免冲突
4. 字段遵循现有格式：

```json
{
  "symptoms": ["error message / 报错关键词"],
  "rootCause": "why it happened / 成因",
  "solution": "verified fix steps / 已验证的解决步骤",
  "prevention": "optional / 可选"
}
```

5. 提交 PR 并简单说明案例来源

## 审核流程 · Review process

- 所有案例合并前会经过人工审核：确认可复现、已验证有效、不含敏感信息
- 相似度 > 0.8 的重复案例会被合并到现有条目
- 合并后会出现在下一个 Release 中

All cases are reviewed before merging: reproducible, verified, sanitized. Near-duplicates are merged; accepted cases ship with the next release.

## 其它 · Other contributions

文档纠错、翻译、`diagnose.py` 改进同样欢迎，直接开 Issue 或 PR 即可。

Docs, translations and improvements to `diagnose.py` are equally welcome.
