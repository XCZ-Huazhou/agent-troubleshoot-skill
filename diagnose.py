#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Agent Troubleshooter - 诊断工具

使用方法:
    python diagnose.py "Codex 报 401 错误"
    python diagnose.py "Claude 429 rate limit"
"""

import json
import sys
from pathlib import Path

# 确保以任意工作目录运行时都能找到同目录下的 utils 包
sys.path.insert(0, str(Path(__file__).resolve().parent))

# 导入匹配工具
from utils.matcher import (
    extract_framework,
    extract_symptoms,
    match_issue,
    load_knowledge_base,
    normalize_keywords
)

# 知识库路径
KB_PATH = Path(__file__).parent / "knowledge-base.json"


def format_solution(match_result: dict, confidence: float) -> str:
    """
    格式化解决方案输出
    
    Args:
        match_result: 匹配结果字典
        confidence: 置信度分数
        
    Returns:
        格式化的解决方案文本
    """
    issue_type = match_result["type"]
    issue_data = match_result["data"]
    
    output = []
    output.append("## 🔍 诊断结果\n")
    output.append(f"**匹配案例**: `{issue_data.get('id', 'UNKNOWN')}`（置信度：{confidence:.0%}）\n")
    
    if issue_type == "common":
        output.append(f"**问题分类**: 共同问题 - {match_result.get('category', 'Unknown')}\n")
    else:
        output.append(f"**问题分类**: {match_result.get('framework', 'Unknown')} 独有问题\n")
    
    output.append(f"**根本原因**: {issue_data.get('rootCause', '未知')}\n")
    output.append("\n---\n\n### ✅ 解决方案\n")
    
    # 输出解决方案
    solutions = issue_data.get("solutions", {})
    if "all" in solutions:
        output.append(f"**通用方案**:\n{solutions['all']}\n")
    
    framework = match_result.get("framework")
    if framework and framework in solutions:
        output.append(f"\n**{framework} 特定建议**:\n{solutions[framework]}\n")
    
    # 输出诊断命令
    if "diagnosis" in issue_data:
        output.append(f"\n---\n\n### 🛠️ 诊断命令\n\n```bash\n{issue_data['diagnosis']}\n```\n")
    
    # 输出预防措施
    if "prevention" in issue_data:
        output.append(f"\n### 📚 预防措施\n\n{issue_data['prevention']}\n")
    
    # 输出错误方案（避坑）
    wrong = issue_data.get("wrongSolutions", [])
    if wrong:
        output.append("\n### ⚠️ 这些方法试过没用（避坑）\n")
        for w in wrong:
            output.append(f"- **{w.get('method', '?')}**：{w.get('whyItFailed', '没用')}\n")
    
    output.append("\n---\n\n> 问题解决了吗？回复「已解决」我将记录这个案例到知识库。")
    
    return "\n".join(output)


def diagnose(user_input: str) -> str:
    """
    诊断用户问题
    
    Args:
        user_input: 用户输入文本
        
    Returns:
        格式化的诊断报告
    """
    # 加载知识库
    try:
        kb = load_knowledge_base(KB_PATH)
    except FileNotFoundError:
        return "❌ 知识库文件未找到，请确认技能已正确安装"
    
    # 匹配问题
    match_result, confidence = match_issue(user_input, kb, threshold=0.3)
    
    if match_result and confidence >= 0.3:
        return format_solution(match_result, confidence)
    else:
        # 无匹配，启动交互式诊断
        framework = extract_framework(user_input)
        
        output = []
        output.append("## ⚠️ 未在知识库中找到完全匹配的案例\n")
        output.append("让我帮你逐步排查这个问题：\n")
        output.append("**步骤 1/3**: 请确认你使用的 Agent 框架是？\n")
        output.append("- [ ] Codex")
        output.append("- [ ] Claude")
        output.append("- [ ] ZCode")
        output.append("- [ ] Gemini")
        output.append("- [ ] Foundry")
        output.append("- [ ] 其他：____\n")
        
        if framework:
            output.append(f"\n检测到你可能在使用 **{framework}**，对吗？\n")
        
        output.append("**步骤 2/3**: 错误日志或截图是？（可直接粘贴）\n")
        output.append("**步骤 3/3**: 问题出现前你执行了什么操作？\n")
        
        return "\n".join(output)


def main():
    """主函数"""
    # Windows 控制台兼容：跟随终端编码，仅对无法编码的字符（如 emoji）做替换，
    # 避免 GBK 控制台下中文乱码或 UnicodeEncodeError 崩溃
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(errors="replace")
            except Exception:
                pass

    if len(sys.argv) < 2:
        print("使用方法：python diagnose.py \"问题描述\"")
        print("示例：python diagnose.py \"Codex 报 401 错误\"")
        sys.exit(1)
    
    user_input = " ".join(sys.argv[1:])
    result = diagnose(user_input)
    print(result)


if __name__ == "__main__":
    main()
