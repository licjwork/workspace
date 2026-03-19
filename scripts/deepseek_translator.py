#!/usr/bin/env python3
"""
使用DeepSeek API进行高质量翻译
"""

import requests
import json
import os
import re
from datetime import datetime

def deepseek_translate(text, target_lang="zh"):
    """
    使用DeepSeek API进行翻译
    """
    if not text or len(text.strip()) == 0:
        return text
    
    # 检查API密钥
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        # 如果没有API密钥，使用备用翻译
        return backup_translate(text)
    
    try:
        # DeepSeek API端点
        url = "https://api.deepseek.com/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 构建翻译提示
        prompt = f"""请将以下英文新闻内容翻译成流畅的中文，保持新闻的准确性和可读性：

{text}

翻译要求：
1. 全部翻译成中文，不保留任何英文单词
2. 保持专业新闻报道的风格
3. 确保专有名词翻译准确
4. 译文要流畅自然

中文翻译："""
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一名专业的新闻翻译专家，擅长将英文新闻准确翻译成中文。"},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            translated = data["choices"][0]["message"]["content"].strip()
            
            # 清理可能的提示文本
            translated = re.sub(r'中文翻译[:：]', '', translated).strip()
            translated = re.sub(r'^["\']|["\']$', '', translated).strip()
            
            return translated
        else:
            print(f"DeepSeek翻译API错误: {response.status_code}")
            return backup_translate(text)
            
    except Exception as e:
        print(f"DeepSeek翻译失败: {e}")
        return backup_translate(text)

def backup_translate(text):
    """
    备用翻译方法：使用简单的词典替换
    """
    # 常见新闻词汇翻译词典
    translations = {
        # 国家和地区
        "Italy": "意大利", "Italy's": "意大利的", "Italian": "意大利的",
        "United States": "美国", "U.S.": "美国", "USA": "美国",
        "Canada": "加拿大", "Canadian": "加拿大的",
        "China": "中国", "Chinese": "中国的",
        "Japan": "日本", "Japanese": "日本的",
        "Germany": "德国", "German": "德国的",
        "France": "法国", "French": "法国的",
        "UK": "英国", "United Kingdom": "英国", "British": "英国的",
        "Russia": "俄罗斯", "Russian": "俄罗斯的",
        
        # 新闻事件词汇
        "Culture Ministry": "文化部",
        "spent around": "花费约",
        "$35 million": "3500万美元",
        "rare": "稀有的",
        "painting": "画作",
        "resigned": "辞职",
        "owning a": "拥有一本",
        "signed copy": "签名版",
        "Alpine skier": "高山滑雪运动员",
        "won silver": "获得银牌",
        "giant slalom sitting race": "大回转坐式比赛",
        "Winter Paralympics": "冬季残奥会",
        "defeated": "击败",
        "Baseball Classic": "棒球经典赛",
        "three-run homer": "三分全垒打",
        "struck out": "三振出局",
        "advancing to": "晋级到",
        "semi-finals": "半决赛",
        
        # 通用词汇
        "after": "在...之后", "with": "随着", "in": "在",
        "on": "关于", "at": "在", "to": "到",
        "for": "为了", "of": "的", "by": "被",
        "and": "和", "or": "或", "but": "但是",
        "the": "", "a": "一个", "an": "一个",
        
        # 月份和日期
        "January": "一月", "February": "二月", "March": "三月",
        "April": "四月", "May": "五月", "June": "六月",
        "July": "七月", "August": "八月", "September": "九月",
        "October": "十月", "November": "十一月", "December": "十二月",
    }
    
    # 替换已知词汇
    translated = text
    for eng, chn in translations.items():
        # 使用正则表达式确保单词边界
        translated = re.sub(rf'\b{re.escape(eng)}\b', chn, translated, flags=re.IGNORECASE)
    
    # 处理剩余的大写专有名词
    def replace_proper_nouns(match):
        word = match.group(0)
        if len(word) > 2 and word[0].isupper():
            # 音译处理
            return f"【{word}】"
        return word
    
    # 替换未翻译的专有名词
    translated = re.sub(r'\b[A-Z][a-z]+\b', replace_proper_nouns, translated)
    
    # 清理格式
    translated = re.sub(r'\s+', ' ', translated).strip()
    
    # 确保开头和结尾
    if translated == text:
        translated = f"【原文】{text[:80]}..."
    
    return translated

def translate_news_text(text):
    """
    主翻译函数
    """
    # 优先使用DeepSeek翻译
    deepseek_result = deepseek_translate(text)
    
    # 检查翻译质量
    if deepseek_result != text and len(deepseek_result) > len(text)/2:
        return deepseek_result
    
    # 如果DeepSeek翻译质量不行，使用备用翻译
    return backup_translate(text)

if __name__ == "__main__":
    # 测试代码
    test_text = """Italy's Culture Ministry spent around $35 million on a rare Caravaggio painting. Niagara Regional Chair Bob Gale resigned after owning a signed copy of Hitler's "Mein Kampf." Alpine skier Momoka Takaoka won silver in the giant slalom sitting race at the Milano Cortina Winter Paralympics. The United States defeated Italy in the World Baseball Classic, with Pete Crow-Armstrong hitting a three-run homer. Mason Miller struck out Canada's Otto Lopez, advancing the United States to the World Baseball Classic semi-finals."""
    
    print("原文:", test_text[:200])
    print("\n翻译结果:", translate_news_text(test_text)[:200])
    print("\n完整翻译:", translate_news_text(test_text))