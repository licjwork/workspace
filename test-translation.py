#!/usr/bin/env python3
# 测试翻译功能

import os
import sys
import requests

# 加载环境变量
def load_env():
    """从.env文件加载环境变量"""
    env_path = "/home/ubuntu/.openclaw/.env"
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value.strip('"')

load_env()

# 测试翻译
def translate(text):
    api_key = os.getenv('LONGCAT_API_KEY')
    if not api_key:
        print("错误：未找到LONGCAT_API_KEY")
        return text
    
    url = "https://api.longcat.chat/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "LongCat-Flash-Chat",
        "messages": [
            {"role": "system", "content": "你是一个专业的科技新闻翻译助手，擅长将英文科技新闻准确翻译成中文。"},
            {"role": "user", "content": f"请原文翻译：{text}"}
        ],
        "max_tokens": 2000,
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"翻译失败，状态码：{response.status_code}")
            return text
    except Exception as e:
        print(f"翻译错误：{e}")
        return text

# 测试新的新闻内容
text = """China's 2026-2030 development plan emphasizes innovation and technological self-reliance, aiming to transform the manufacturing-driven economy into a global innovation powerhouse. The plan includes significant investments in original innovation, basic research, and major science and technology infrastructure projects. Additionally, China has allocated 200 billion yuan in 2026 for large-scale equipment upgrades to promote industrial transformation and strengthen the manufacturing sector."""

translated = translate(text)
print("原文：")
print(text)
print("\n译文：")
print(translated)