#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细测试微博技能的内容生成入参
"""

import sys
import os

# 添加技能路径
sys.path.append('/home/ubuntu/.openclaw/workspace/skills/weibo-publish-2/scripts')

# 修改导入以获取更多详细信息
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

def call_longcat_api_with_debug(topic, research_context=None):
    """调用LongCat大模型生成内容 - 带详细调试信息"""
    api_key = os.environ.get('LONGCAT_API_KEY')
    if not api_key:
        print("❌ LONGCAT_API_KEY 未配置")
        return None
    
    # 显示完整的prompt内容
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
    
    print("📝 完整的Prompt入参内容:")
    print("="*80)
    print(prompt)
    print("="*80)
    
    # 显示API请求参数
    api_request = {
        "model": "LongCat-Flash-Chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 800,
        "temperature": 0.8
    }
    
    print("\n🔧 API请求参数:")
    print("="*80)
    print(json.dumps(api_request, ensure_ascii=False, indent=2))
    print("="*80)
    
    try:
        session = requests.Session()
        session.mount('https://', CustomSSLAdapter())
        
        url = "https://api.longcat.chat/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        print(f"\n🌐 请求URL: {url}")
        print(f"📋 请求头: {headers}")
        
        response = session.post(
            url, 
            headers=headers, 
            json=api_request, 
            timeout=30,
            verify=False
        )
        
        print(f"\n📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n📋 完整API响应:")
            print("="*80)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            print("="*80)
            
            if 'choices' in result and result['choices']:
                content = result['choices'][0]['message']['content']
                return content.strip()
        else:
            print(f"❌ 请求失败: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return None

def main():
    """主测试函数"""
    if len(sys.argv) < 2:
        print("请提供测试话题作为参数")
        print("用法: python3 test_detailed_params.py <话题>")
        return
    
    topic = sys.argv[1]
    print(f"🚀 测试话题: {topic}")
    print("\n" + "="*80)
    
    result = call_longcat_api_with_debug(topic)
    
    if result:
        print("\n✅ 生成内容:")
        print("="*80)
        print(result)
        print("="*80)
    else:
        print("\n❌ 生成失败")

if __name__ == "__main__":
    main()
