#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
纯净版LongCat API调用 - 无模板，完全交给大模型
生成真实客观的内容，避免虚假信息
"""

import os
import requests
import json
import urllib3
import ssl
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CustomSSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

def call_longcat_api(topic, research_context=None):
    """调用LongCat大模型生成内容 - 完全无模板"""
    api_key = os.environ.get('LONGCAT_API_KEY')
    if not api_key:
        print("❌ LONGCAT_API_KEY 未配置，请在环境变量中设置或在 .env 文件中添加")
        return None
    
    # 强调真实客观的提示词
    prompt = f"""请为微博生成一段关于"{topic}"的有趣内容！
要求：
- 开头添加相关话题标签，格式为#标签内容1##标签内容2#, 标题要足够亮眼
- 语气轻松自然，有青春活力
- 网络用语和表情符号可用使用2-3个
- 200-400字，有信息量有观点
- 基于事实和数据，但要生动有趣
- 用轻松幽默的方式表达观点
- 避免说教感，保持客观中立的立场
- 严禁捏造不存在的数据与内容，只使用真实可靠的信息
- 如不确定性别，不要随意添加性别描述
- 不要使用"姐妹们"、"家人们"等群体称呼
- 你要知道现在是2026年，不强制要求内容里有2026年字眼
- 使用更普遍和中性的表达方式

背景信息：{research_context or '无具体背景信息'}

请直接生成内容，不要包含其他说明。"""
    
    try:
        # 创建自定义Session
        session = requests.Session()
        session.mount('https://', CustomSSLAdapter())
        
        # 使用文档中的正确API端点和模型名称
        api_configs = [
            {
                "url": "https://api.longcat.chat/openai/v1/chat/completions",
                "headers": {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                "data": {
                    "model": "LongCat-Flash-Chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 800,
                    "temperature": 0.8
                }
            },
            {
                "url": "https://api.longcat.chat/openai/v1/chat/completions",
                "headers": {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                "data": {
                    "model": "LongCat-Flash-Chat-2602-Exp",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 800,
                    "temperature": 0.8
                }
            }
        ]
        
        for config in api_configs:
            try:
                print(f"🔄 尝试连接到: {config['url']} (模型: {config['data']['model']})")
                response = session.post(
                    config["url"], 
                    headers=config["headers"], 
                    json=config["data"], 
                    timeout=30,
                    verify=False
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # 处理不同的响应格式
                    if 'choices' in result and result['choices']:
                        if 'message' in result['choices'][0]:
                            content = result['choices'][0]['message']['content']
                        elif 'text' in result['choices'][0]:
                            content = result['choices'][0]['text']
                        else:
                            content = str(result['choices'][0])
                    elif 'response' in result:
                        content = result['response']
                    elif 'content' in result:
                        content = result['content']
                    else:
                        print(f"❌ API返回异常格式: {result}")
                        return None
                    
                    if content.strip() and len(content.strip()) > 50:  # 确保内容有意义
                        print(f"✅ 成功连接到 {config['url']} (模型: {config['data']['model']})")
                        return content.strip()
                    else:
                        print(f"❌ API返回内容无效")
                        return None
                else:
                    print(f"❌ {config['url']} 返回错误: {response.status_code} - {response.text}")
                    
            except Exception as e:
                print(f"❌ {config['url']} 连接失败: {e}")
                continue
        
        print("❌ 所有API连接尝试失败")
        return None
            
    except Exception as e:
        print(f"❌ LongCat API 调用异常: {e}")
        return None

def call_dogegg_ai(topic, research_context=None):
    """完全交给LongCat大模型处理 - 无模板版本"""
    print(f"🤖 正在调用LongCat大模型生成内容: {topic}")
    
    # 100%依赖LongCat API，无本地备选方案
    content = call_longcat_api(topic, research_context)
    
    if content:
        print("✅ LongCat大模型内容生成成功")
        return content
    else:
        print("❌ LongCat生成失败，无法继续")
        return None

if __name__ == "__main__":
    import sys
    test_topic = sys.argv[1] if len(sys.argv) > 1 else "测试话题"
    result = call_dogegg_ai(test_topic)
    if result:
        print("\n" + "="*50)
        print(result)
