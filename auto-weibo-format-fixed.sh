#!/bin/bash

# 自动微博格式脚本 - 改进版
# 确保生成高质量的news_list数据

cd /home/ubuntu/.openclaw/workspace/web-navigation-system

echo "=== 开始生成国际新闻数据 ==="

# 1. 搜索国际新闻
echo "正在搜索国际新闻..."
python3 /home/ubuntu/.openclaw/workspace/skills/tavily/scripts/tavily_search.py "国际最新新闻" \
  --api-key "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" \
  --topic news \
  --max-results 10

# 2. 使用改进的Prompt解析数据
echo "正在解析和结构化数据..."
python3 << 'PYTHON_PARSE'
import requests
import json
from datetime import datetime
import subprocess
import re

# 获取Tavily搜索结果
result = subprocess.run(
    ['python3', '/home/ubuntu/.openclaw/workspace/skills/tavily/scripts/tavily_search.py', 
     '国际最新新闻', '--api-key', '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',
     '--topic', 'news', '--max-results', '10'],
    capture_output=True, text=True
)

tavily_output = result.stdout

# 使用改进的Prompt解析
prompt = f'''你是一个专业的新闻编辑。请从以下搜索结果中提取最新新闻，生成JSON格式。

严格要求：
1. 提取5条最新、最重要的国际新闻
2. 完全忽略包含旧日期（如"3月17日"、"March 17"）的内容
3. 每条新闻格式：
   - index: 序号（必须从1开始连续编号：1, 2, 3, 4, 5）
   - title: 标题（15-25字，简洁明了）
   - summary: 摘要（40-80字，概括关键事实，不要空话）
4. 清理所有无关标记和符号
5. 返回纯JSON，不要任何Markdown标记

搜索结果：
{tavily_output}

返回格式：
{{"news_list": [{{"index": 1, "title": "标题", "summary": "摘要"}}, ...]}}
'''

response = requests.post(
    'https://api.longcat.chat/openai/v1/chat/completions',
    headers={
        'Authorization': 'Bearer ak_2Yu4dw9LQ9lu6v63Dh42J3Oo6aE50',
        'Content-Type': 'application/json'
    },
    json={
        'model': 'LongCat-Flash-Chat',
        'messages': [{'role': 'user', 'content': prompt}]
    },
    timeout=30
)

if response.status_code == 200:
    result = response.json()
    content = result['choices'][0]['message']['content'].strip()
    
    # 清理Markdown标记
    if '```' in content:
        lines = content.split('\n')
        content = '\n'.join([line for line in lines if not line.strip().startswith('```')])
    
    try:
        news_data = json.loads(content)
        
        # 验证和修复数据
        validated_news = []
        for i, news in enumerate(news_data.get('news_list', []), 1):
            if all(key in news for key in ['title', 'summary']):
                # 检查是否包含旧日期
                if '3月17日' in news.get('title', '') or '3月17日' in news.get('summary', ''):
                    continue
                if 'March 17' in news.get('title', '') or 'March 17' in news.get('summary', ''):
                    continue
                
                # 清理摘要中的无关内容
                summary = news['summary']
                summary = re.sub(r'#.*', '', summary).strip()
                summary = re.sub(r'网站分类.*', '', summary).strip()
                
                validated_news.append({
                    'index': len(validated_news) + 1,
                    'title': news['title'],
                    'summary': summary
                })
                
                # 最多保留5条
                if len(validated_news) >= 5:
                    break
        
        news_data['news_list'] = validated_news
        news_data['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 生成摘要
        if validated_news:
            titles = [news['title'] for news in validated_news[:3]]
            news_data['content'] = '国际新闻摘要：' + '；'.join(titles) + '。'
        
        # 保存
        with open('/home/ubuntu/.openclaw/workspace/web-navigation-system/database/news.json', 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        
        print('✅ 数据生成成功')
        print(f'更新时间: {news_data["last_update"]}')
        print(f'新闻条数: {len(validated_news)}')
    except Exception as e:
        print(f'❌ 解析失败: {e}')
else:
    print(f'❌ API失败: {response.status_code}')
PYTHON_PARSE

echo "=== 数据生成完成 ==="
