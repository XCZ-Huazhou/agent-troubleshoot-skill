"""
Agent Troubleshooter - 语义匹配和去重工具

功能：
1. 症状关键词提取和标准化
2. Jaccard 相似度计算
3. 框架名识别
4. 案例去重判断
"""

import json
import re
import sys
from datetime import date
from typing import List, Dict, Any, Tuple, Optional
from pathlib import Path

# 错误码标准化映射
ERROR_CODE_NORMALIZATION = {
    # 认证错误
    "401": "AUTH_ERROR",
    "403": "AUTH_ERROR",
    "unauthorized": "AUTH_ERROR",
    "authentication failed": "AUTH_ERROR",
    "认证失败": "AUTH_ERROR",
    "token 过期": "AUTH_ERROR",
    "凭证过期": "AUTH_ERROR",
    
    # 限流错误
    "429": "RATE_LIMIT",
    "too many requests": "RATE_LIMIT",
    "rate limit": "RATE_LIMIT",
    "速率限制": "RATE_LIMIT",
    "配额耗尽": "RATE_LIMIT",
    "quota exceeded": "RATE_LIMIT",
    
    # 上下文错误
    "context limit": "CONTEXT_OVERFLOW",
    "token overflow": "CONTEXT_OVERFLOW",
    "maximum context length": "CONTEXT_OVERFLOW",
    "上下文溢出": "CONTEXT_OVERFLOW",
    "token 超限": "CONTEXT_OVERFLOW",
    
    # 网络错误
    "timeout": "NETWORK_ERROR",
    "connection timed out": "NETWORK_ERROR",
    "network error": "NETWORK_ERROR",
    "连接超时": "NETWORK_ERROR",
    "网络错误": "NETWORK_ERROR",
    
    # 模型错误
    "model not found": "MODEL_ERROR",
    "unsupported model": "MODEL_ERROR",
    "模型不存在": "MODEL_ERROR",
    "不支持的模型": "MODEL_ERROR",
}

# 框架名识别关键词
FRAMEWORK_KEYWORDS = {
    "Codex": ["codex", "openai codex", "/model", "mcp", "code review"],
    "Claude": ["claude", "anthropic", "artifact", "claude code"],
    "ZCode": ["zcode", "skill", "hook", "mcp server", "插件"],
    "Gemini": ["gemini", "google ai", "thinking budget", "google studio"],
    "Foundry": ["foundry", "azure", "azd", "application insights", "azure ai"],
    "Reasonix": ["reasonix", "reasoning chain"],
    "AntiGravity": ["antigravity", "anti-gravity"],
    "OpenCode": ["opencode", "open-code"],
}


def normalize_keywords(keywords: List[str]) -> List[str]:
    """
    标准化关键词（将具体错误码映射到通用类别）
    
    Args:
        keywords: 原始关键词列表
        
    Returns:
        标准化后的关键词列表
    """
    normalized = []
    for kw in keywords:
        kw_lower = kw.lower().strip()
        if kw_lower in ERROR_CODE_NORMALIZATION:
            normalized.append(ERROR_CODE_NORMALIZATION[kw_lower])
        else:
            normalized.append(kw_lower)
    return list(set(normalized))


def extract_framework(user_input: str) -> Optional[str]:
    """
    从用户输入中提取 Agent 框架名
    
    Args:
        user_input: 用户输入文本
        
    Returns:
        识别到的框架名，如果未识别返回 None
    """
    user_input_lower = user_input.lower()
    
    for framework, keywords in FRAMEWORK_KEYWORDS.items():
        for kw in keywords:
            if kw in user_input_lower:
                return framework
    
    return None


def extract_symptoms(user_input: str) -> List[str]:
    """
    从用户输入中提取症状关键词
    
    Args:
        user_input: 用户输入文本
        
    Returns:
        症状关键词列表
    """
    symptoms = []
    
    # 提取错误码（数字）
    error_codes = re.findall(r'\b\d{3}\b', user_input)
    symptoms.extend(error_codes)
    
    # 提取英文关键词
    english_words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9_-]*\b', user_input)
    symptoms.extend([w.lower() for w in english_words if len(w) > 3])
    
    # 提取中文短语（2-8 个字符）
    chinese_phrases = re.findall(r'[\u4e00-\u9fa5]{2,8}', user_input)
    symptoms.extend(chinese_phrases)
    
    # 去重
    return list(set(symptoms))


def jaccard_similarity(set_a: set, set_b: set) -> float:
    """
    计算 Jaccard 相似度
    
    Args:
        set_a: 集合 A
        set_b: 集合 B
        
    Returns:
        相似度分数 (0-1)
    """
    if not set_a and not set_b:
        return 0.0
    
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    
    return intersection / union if union > 0 else 0.0


def calculate_similarity(keywords_a: List[str], keywords_b: List[str]) -> float:
    """
    计算两组关键词的语义相似度
    
    Args:
        keywords_a: 关键词列表 A
        keywords_b: 关键词列表 B
        
    Returns:
        相似度分数 (0-1)
    """
    # 标准化
    normalized_a = set(normalize_keywords(keywords_a))
    normalized_b = set(normalize_keywords(keywords_b))
    
    return jaccard_similarity(normalized_a, normalized_b)


def match_issue(
    user_input: str, 
    knowledge_base: Dict[str, Any],
    threshold: float = 0.5
) -> Tuple[Optional[Dict[str, Any]], float]:
    """
    匹配用户问题到知识库中的案例
    
    Args:
        user_input: 用户输入
        knowledge_base: 知识库字典
        threshold: 匹配置信度阈值
        
    Returns:
        (匹配的案例，置信度)，如果无匹配返回 (None, 0.0)
    """
    # 提取框架名
    framework = extract_framework(user_input)
    
    # 提取症状
    user_symptoms = extract_symptoms(user_input)
    
    best_match = None
    best_score = 0.0
    
    # 1. 优先匹配共同问题
    common_issues = knowledge_base.get("common-issues", {})
    for issue_id, issue in common_issues.items():
        issue_symptoms = issue.get("symptoms", [])
        score = calculate_similarity(user_symptoms, issue_symptoms)
        
        if score > best_score and score >= threshold:
            best_score = score
            best_match = {
                "type": "common",
                "category": issue_id,
                "data": issue
            }
    
    # 2. 匹配框架独有问题
    if framework and framework in knowledge_base.get("frameworks", {}):
        unique_issues = knowledge_base["frameworks"][framework].get("unique-issues", [])
        for issue in unique_issues:
            issue_symptoms = issue.get("symptoms", [])
            score = calculate_similarity(user_symptoms, issue_symptoms)
            
            if score > best_score and score >= threshold:
                best_score = score
                best_match = {
                    "type": "unique",
                    "framework": framework,
                    "data": issue
                }
    
    return best_match, best_score


def check_duplicate(
    new_case: Dict[str, Any],
    knowledge_base: Dict[str, Any],
    similarity_threshold: float = 0.8
) -> Optional[Dict[str, Any]]:
    """
    检查新案例是否与知识库中已有案例重复
    
    Args:
        new_case: 新案例字典
        knowledge_base: 知识库
        similarity_threshold: 相似度阈值
        
    Returns:
        如果重复，返回已有案例；否则返回 None
    """
    new_symptoms = new_case.get("symptoms", [])
    
    # 检查共同问题
    for issue_id, issue in knowledge_base.get("common-issues", {}).items():
        existing_symptoms = issue.get("symptoms", [])
        score = calculate_similarity(new_symptoms, existing_symptoms)
        
        if score >= similarity_threshold:
            return {"type": "common", "id": issue_id, "data": issue}
    
    # 检查框架独有问题
    framework = new_case.get("framework")
    if framework and framework in knowledge_base.get("frameworks", {}):
        for issue in knowledge_base["frameworks"][framework].get("unique-issues", []):
            existing_symptoms = issue.get("symptoms", [])
            score = calculate_similarity(new_symptoms, existing_symptoms)
            
            if score >= similarity_threshold:
                return {"type": "unique", "id": issue.get("id"), "data": issue}
    
    return None


def load_knowledge_base(kb_path: str) -> Dict[str, Any]:
    """
    加载知识库文件
    
    Args:
        kb_path: 知识库 JSON 文件路径
        
    Returns:
        知识库字典
    """
    kb_file = Path(kb_path)
    if not kb_file.exists():
        raise FileNotFoundError(f"知识库文件不存在：{kb_path}")
    
    with open(kb_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_knowledge_base(knowledge_base: Dict[str, Any], kb_path: str) -> None:
    """
    保存知识库文件（自动备份旧版本）
    
    Args:
        knowledge_base: 知识库字典
        kb_path: 知识库 JSON 文件路径
    """
    kb_file = Path(kb_path)
    
    # 备份旧版本
    if kb_file.exists():
        backup_path = kb_file.with_suffix('.json.bak')
        kb_file.rename(backup_path)
    
    # 写入新版本
    with open(kb_file, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, ensure_ascii=False, indent=2)


def add_new_case(
    knowledge_base: Dict[str, Any],
    new_case: Dict[str, Any]
) -> Tuple[bool, str]:
    """
    添加新案例到知识库
    
    Args:
        knowledge_base: 知识库字典
        new_case: 新案例，包含 framework, symptoms, rootCause, solution 等字段
        
    Returns:
        (是否添加成功，消息)
    """
    framework = new_case.get("framework")
    
    if not framework:
        return False, "未指定框架名"
    
    # 检查框架是否存在
    if framework not in knowledge_base.get("frameworks", {}):
        # 创建新框架分类
        knowledge_base["frameworks"][framework] = {
            "description": f"{framework} Agent Framework",
            "unique-issues": []
        }
    
    # 添加到框架的 unique-issues
    issue_id = f"{framework.upper()}-{len(knowledge_base['frameworks'][framework]['unique-issues']) + 1:03d}"
    new_case["id"] = issue_id
    
    knowledge_base["frameworks"][framework]["unique-issues"].append(new_case)
    
    # 更新 metadata
    knowledge_base["metadata"]["totalCases"] += 1
    knowledge_base["metadata"]["lastUpdated"] = date.today().isoformat()
    
    return True, f"案例 {issue_id} 已添加到知识库"


# 测试函数
def run_tests():
    """运行单元测试"""
    print("测试关键词标准化...")
    assert normalize_keywords(["401", "Unauthorized"]) == ["AUTH_ERROR"]
    print("✓ 关键词标准化通过")
    
    print("测试框架识别...")
    assert extract_framework("Codex 报 401 错误") == "Codex"
    assert extract_framework("Claude artifact 无法加载") == "Claude"
    print("✓ 框架识别通过")
    
    print("测试相似度计算...")
    score = calculate_similarity(["401", "unauthorized"], ["401", "auth failed"])
    assert score >= 0.5
    print("✓ 相似度计算通过")
    
    print("\n所有测试通过！✅")


if __name__ == "__main__":
    # Windows 控制台兼容：避免 GBK 控制台下 emoji 导致 UnicodeEncodeError
    for _stream in (sys.stdout, sys.stderr):
        if hasattr(_stream, "reconfigure"):
            try:
                _stream.reconfigure(errors="replace")
            except Exception:
                pass
    run_tests()
