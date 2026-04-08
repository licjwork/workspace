#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def parse_news_with_ai(tavily_results):
    """使用LongCat AI解析Tavily搜索结果，生成高质量的结构化新闻数据"""
    
    prompt = f'''你是一个专业的新闻编辑。请从以下搜索结果中提取最新新闻，生成JSON格式的新闻列表。

要求：
1. 提取5-10条最新、最重要的国际新闻
2. 忽略任何包含旧日期（如"3月17日"）的内容
3. 每条新闻必须包含：
   - index: 序号（从1开始连续编号）
   - title: 标题（15-25字，简洁明了）
   - summary: 摘要（40-80字，概括关键信息）
4. 清理摘要中的无关内容（如"# 网站分类"、标记符号等）
5. 确保新闻内容真实、有价值
6. 返回纯JSON格式，不要任何Markdown标记

搜索结果：
{tavily_results}

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
        
        # 移除可能的Markdown代码块标记
        if '```' in content:
            lines = content.split('\n')
            content = '\n'.join([line for line in lines if not line.strip().startswith('```')])
        
        try:
            news_data = json.loads(content)
            
            # 验证数据质量
            validated_news = []
            for news in news_data.get('news_list', []):
                # 验证必需字段
                if all(key in news for key in ['index', 'title', 'summary']):
                    # 确保序号连续
                    if news['index'] == len(validated_news) + 1:
                        # 清理摘要中的无关内容
                        summary = news['summary']
                        summary = summary.replace('# 网站分类', '').strip()
                        summary = summary.replace('#', '').strip()
                        
                        validated_news.append({
                            'index': news['index'],
                            'title': news['title'],
                            'summary': summary
                        })
            
            return {'news_list': validated_news}
        except Exception as e:
            print(f"解析JSON失败: {e}")
            return None
    else:
        print(f"API调用失败: {response.status_code}")
        return None

if __name__ == "__main__":
    # 测试
    test_results = "伊朗能源设施遭袭后油价飙升，美国国防部申请2000亿美元军费"
    result = parse_news_with_ai(test_results)
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
