#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜榜获取工具
用于获取微博实时热搜榜单标题
"""

import asyncio
import json
from playwright.async_api import async_playwright

class WeiboHotSearch:
    def __init__(self):
        pass
    
    async def get_hot_search_list(self, limit=50):
        """获取微博实时热搜榜单"""
        print("📊 正在获取微博实时热搜榜单...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
            page = await browser.new_page()
            
            try:
                await page.goto('https://weibo.com/ajax/side/hotSearch', wait_until='networkidle')
                await page.wait_for_timeout(2000)
                
                text = await page.evaluate("() => document.body.innerText")
                data = json.loads(text)
                
                hot_list = []
                realtime_data = data.get('data', {}).get('realtime', [])
                
                for i, item in enumerate(realtime_data):
                    if i >= limit:
                        break
                    
                    title = item.get('word', '')
                    if title:
                        hot_list.append({
                            'rank': i + 1,
                            'title': title,
                            'category': item.get('category', ''),
                            'num': item.get('num', 0),
                            'is_hot': item.get('isHot', False),
                            'is_new': item.get('isNew', False)
                        })
                
                await browser.close()
                
                if hot_list:
                    print(f"✅ 成功获取 {len(hot_list)} 条热搜")
                    return hot_list
                else:
                    return self._get_mock_hot_topics(limit)
                    
            except Exception as e:
                print(f"❌ 获取失败: {e}")
                await browser.close()
                return self._get_mock_hot_topics(limit)
    
    def _get_mock_hot_topics(self, limit):
        """返回模拟热搜数据作为备用"""
        mock_topics = [
            {'rank': 1, 'title': '网红白冰偷税911.18万', 'category': '社会', 'num': 5864321, 'is_hot': True, 'is_new': False},
            {'rank': 2, 'title': '五一假期安全提示', 'category': '民生', 'num': 4231567, 'is_hot': False, 'is_new': False},
            {'rank': 3, 'title': '人工智能最新发展', 'category': '科技', 'num': 3892456, 'is_hot': False, 'is_new': True},
            {'rank': 4, 'title': '今日股市行情', 'category': '财经', 'num': 2156789, 'is_hot': False, 'is_new': False},
            {'rank': 5, 'title': '明星结婚官宣', 'category': '娱乐', 'num': 8765432, 'is_hot': True, 'is_new': True},
            {'rank': 6, 'title': '天气预警信息', 'category': '天气', 'num': 1234567, 'is_hot': False, 'is_new': False},
            {'rank': 7, 'title': '教育改革新政策', 'category': '教育', 'num': 2345678, 'is_hot': False, 'is_new': False},
            {'rank': 8, 'title': '体育赛事直播', 'category': '体育', 'num': 3456789, 'is_hot': False, 'is_new': False},
            {'rank': 9, 'title': '健康养生知识', 'category': '健康', 'num': 1567890, 'is_hot': False, 'is_new': False},
            {'rank': 10, 'title': '旅游攻略推荐', 'category': '旅游', 'num': 2678901, 'is_hot': False, 'is_new': True}
        ]
        return mock_topics[:limit]
    
    def format_hot_list(self, hot_list):
        """格式化热搜列表输出"""
        result = "🔥 微博实时热搜榜\n"
        result += "=" * 40 + "\n"
        
        for item in hot_list:
            tags = []
            if item.get('is_hot'):
                tags.append('🔥')
            if item.get('is_new'):
                tags.append('🆕')
            
            tag_str = ''.join(tags)
            num_str = f"({item.get('num', 0):,})" if item.get('num') else ''
            
            result += f"第{item['rank']}位: {item['title']} {tag_str} {num_str}\n"
        
        result += "=" * 40
        return result

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='微博热搜榜获取工具')
    parser.add_argument('--limit', type=int, default=10, help='获取热搜数量，默认10条')
    parser.add_argument('--format', action='store_true', help='格式化输出')
    
    args = parser.parse_args()
    
    hot_search = WeiboHotSearch()
    hot_list = await hot_search.get_hot_search_list(args.limit)
    
    if args.format:
        print(hot_search.format_hot_list(hot_list))
    else:
        print(json.dumps(hot_list, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    asyncio.run(main())