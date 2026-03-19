#!/usr/bin/env python3
"""
Enhanced News Search - Get detailed news content with minimum length requirement
"""

import json
import sys
import os
from typing import List, Dict
from tavily_search import search


def get_detailed_news(query: str, api_key: str, min_content_length: int = 200) -> Dict:
    """
    Get detailed news with minimum content length requirement
    """
    # Use advanced search for comprehensive results
    result = search(
        query=query,
        api_key=api_key,
        search_depth="advanced",
        topic="news",
        max_results=10,
        include_answer=True,
        include_raw_content=True
    )
    
    if "error" in result:
        return result
    
    # Filter results to ensure minimum content length
    detailed_results = []
    for item in result.get("results", []):
        content = item.get("content", "")
        if len(content) >= min_content_length:
            detailed_results.append(item)
    
    # If we don't have enough detailed results, try to supplement
    if len(detailed_results) < 10:
        # Get more results to supplement
        supplement_result = search(
            query=query,
            api_key=api_key,
            search_depth="advanced",
            topic="news",
            max_results=15,
            include_answer=False,
            include_raw_content=True
        )
        
        if "error" not in supplement_result:
            for item in supplement_result.get("results", []):
                content = item.get("content", "")
                if len(content) >= min_content_length and item not in detailed_results:
                    detailed_results.append(item)
                    if len(detailed_results) >= 10:
                        break
    
    result["results"] = detailed_results[:10]  # Keep top 10
    result["total_detailed_results"] = len(detailed_results)
    result["min_content_length"] = min_content_length
    
    return result


def format_news_for_display(result: Dict) -> str:
    """
    Format news results for display with detailed content
    """
    output = []
    
    if "error" in result:
        output.append(f"错误: {result['error']}")
        return "\n".join(output)
    
    output.append(f"=== 新闻搜索: {result['query']} ===")
    output.append(f"搜索深度: 高级")
    output.append(f"详细新闻数量: {result.get('total_detailed_results', 0)}/10")
    output.append(f"最小内容长度: {result.get('min_content_length', 0)}字")
    output.append("\n")
    
    if result.get("answer"):
        output.append("=== AI摘要 ===")
        output.append(result["answer"])
        output.append("\n")
    
    if result.get("results"):
        output.append("=== 详细新闻内容 ===")
        for i, item in enumerate(result["results"], 1):
            output.append(f"\n{i}. {item.get('title', '无标题')}")
            output.append(f"   来源: {item.get('url', '未知来源')}")
            output.append(f"   相关性: {item.get('score', 0):.3f}")
            
            content = item.get("content", "")
            # Ensure content is detailed enough
            if len(content) < 200:
                content += " [内容较短，建议查看原文获取详细信息]"
            
            output.append(f"   内容: {content}")
            output.append("-" * 50)
    else:
        output.append("未找到符合条件的详细新闻内容")
    
    return "\n".join(output)


def main():
    """
    Enhanced news search with detailed content
    """
    if len(sys.argv) < 2:
        print("用法: python enhanced_news.py '搜索关键词' [--min-length 200]")
        sys.exit(1)
    
    query = sys.argv[1]
    min_length = 200  # Default minimum content length
    
    # Parse optional arguments
    for i, arg in enumerate(sys.argv[2:], 2):
        if arg == "--min-length" and i + 1 < len(sys.argv):
            try:
                min_length = int(sys.argv[i + 1])
            except ValueError:
                print("错误: --min-length 参数必须是整数")
                sys.exit(1)
    
    api_key = os.getenv("TAVILY_API_KEY") or "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"
    
    result = get_detailed_news(query, api_key, min_length)
    
    formatted_output = format_news_for_display(result)
    print(formatted_output)


if __name__ == "__main__":
    main()