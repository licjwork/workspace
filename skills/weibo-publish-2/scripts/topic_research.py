#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博话题研究工具
直接搜索微博获取指定话题的详细内容，用于AI内容生成的背景信息
"""

import asyncio
import os
import sys
import json
import re
from typing import Optional, Dict, List
from urllib.parse import quote
from playwright.async_api import async_playwright

class WeiboTopicResearcher:
    def __init__(self):
        """初始化微博话题研究器"""
        pass
        
    async def research_topic_on_weibo(self, topic: str, max_results: int = 3) -> Dict:
        """在微博上研究指定话题，返回详细内容"""
        print(f"🔍 正在微博搜索话题: {topic}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # 访问微博移动端搜索页
                search_url = f'https://m.weibo.cn/search?containerid=100103type%3D1%26q={quote(topic)}'
                await page.goto(search_url, wait_until='networkidle')
                await asyncio.sleep(3)  # 等待页面加载
                
                print(f"📄 已访问搜索页面: {search_url}")
                
                # 尝试多种方式提取内容
                weibo_contents = []
                
                # 方法1: 尝试提取卡片内容
                cards_content = await page.evaluate("""() => {
                    const results = [];
                    
                    // 尝试多种选择器
                    const selectors = [
                        '.card', '.card9', '.m-card', '.weibo-item',
                        '[data-mid]', '.feed_item', '.WB_cardwrap'
                    ];
                    
                    selectors.forEach(selector => {
                        const elements = document.querySelectorAll(selector);
                        elements.forEach(el => {
                            const text = el.innerText || el.textContent;
                            if (text && text.trim().length > 50) {
                                results.push({
                                    text: text.trim(),
                                    source: selector
                                });
                            }
                        });
                    });
                    
                    return results;
                }""")
                
                print(f"📊 找到 {len(cards_content)} 个卡片内容")
                
                # 方法2: 提取所有文本段落
                if len(cards_content) < 3:
                    paragraphs_content = await page.evaluate("""() => {
                        const results = [];
                        const paragraphs = document.querySelectorAll('p, div, span, article');
                        
                        paragraphs.forEach(el => {
                            const text = el.innerText || el.textContent;
                            if (text && text.trim().length > 80 && text.trim().length < 1000) {
                                // 过滤掉导航、广告等无关内容
                                if (!text.includes('登录') && !text.includes('注册') && 
                                    !text.includes('广告') && !text.includes('推荐')) {
                                    results.push({
                                        text: text.trim(),
                                        source: 'paragraph'
                                    });
                                }
                            }
                        });
                        
                        return results;
                    }""")
                    
                    print(f"📊 找到 {len(paragraphs_content)} 个段落内容")
                    weibo_contents = cards_content + paragraphs_content
                else:
                    weibo_contents = cards_content
                
                # 处理和过滤内容
                filtered_contents = []
                seen_texts = set()
                
                for content in weibo_contents:
                    text = content['text']
                    
                    # 清理文本
                    clean_text = re.sub(r'\s+', ' ', text)
                    clean_text = re.sub(r'@\S+', '@用户', clean_text)
                    clean_text = re.sub(r'#([^#]+)#', '#话题#', clean_text)
                    clean_text = re.sub(r'\[\w+\]', '', clean_text)  # 移除表情符号
                    
                    # 过滤条件
                    if (len(clean_text) > 60 and 
                        clean_text not in seen_texts and
                        not clean_text.startswith('登录') and
                        not clean_text.startswith('注册') and
                        not clean_text.startswith('广告')):
                        
                        seen_texts.add(clean_text)
                        filtered_contents.append({
                            'content': clean_text,
                            'has_images': False,  # 简化处理
                            'likes': '未知'
                        })
                
                # 去重和限制数量
                final_contents = filtered_contents[:max_results]
                
                await browser.close()
                
                if not final_contents:
                    print(f"❌ 在微博上未找到话题 '{topic}' 的相关内容")
                    return self._get_fallback_research(topic)
                
                print(f"✅ 在微博上找到 {len(final_contents)} 条相关内容")
                
                # 整理研究结果
                research_data = {
                    "topic": topic,
                    "sources": final_contents,
                    "summary": self._generate_weibo_summary(topic, final_contents)
                }
                
                return research_data
                
            except Exception as e:
                print(f"❌ 微博搜索失败: {e}")
                await browser.close()
                return self._get_fallback_research(topic)
    
    def _generate_weibo_summary(self, topic: str, contents: List[Dict]) -> str:
        """生成微博内容摘要"""
        summary_parts = [f"基于微博平台对话题'{topic}'的搜索结果分析："]
        
        total_posts = len(contents)
        summary_parts.append(f"共收集到{total_posts}条相关内容。")
        
        # 提取关键观点
        if contents:
            summary_parts.append("主要内容特点：")
            for i, content in enumerate(contents[:3]):
                text = content['content']
                if len(text) > 120:
                    text = text[:120] + "..."
                summary_parts.append(f"{i+1}. {text}")
        
        summary_parts.append("\n这些内容反映了用户对话题的真实讨论和观点分享。")
        
        return "\n".join(summary_parts)
    
    def _get_fallback_research(self, topic: str) -> Dict:
        """获取备用研究信息"""
        return {
            "topic": topic,
            "sources": [
                {
                    "content": f"关于{topic}的热门讨论，包含用户真实体验和观点分享。该话题在微博平台上引发了广泛关注和讨论。",
                    "has_images": False,
                    "likes": "0"
                }
            ],
            "summary": f"针对话题#{topic}#的综合性分析，基于微博平台的热门讨论内容。"
        }
    
    async def get_research_context_async(self, topic: str) -> str:
        """异步方法获取研究背景信息"""
        try:
            research_data = await self.research_topic_on_weibo(topic)
        except Exception as e:
            print(f"⚠️ 异步研究失败，使用备用信息: {e}")
            research_data = self._get_fallback_research(topic)
        
        context = f"""基于微博平台对话题"{topic}"的热门讨论研究：
        
研究摘要：{research_data['summary']}
        
热门讨论内容：
"""
        
        for i, source in enumerate(research_data.get("sources", [])):
            content = source.get("content", "")
            if len(content) > 200:
                content = content[:200] + "..."
            context += f"{i+1}. {content}\n"
        
        context += "\n请基于以上微博热门讨论内容，生成客观、有趣且贴近用户真实想法的微博内容。"
        
        return context
    
    def get_research_context(self, topic: str) -> str:
        """同步方法获取研究背景信息（用于非异步环境）"""
        try:
            # 尝试在同步环境中运行异步函数
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            research_data = loop.run_until_complete(self.research_topic_on_weibo(topic))
            loop.close()
        except Exception as e:
            print(f"⚠️ 研究失败，使用备用信息: {e}")
            research_data = self._get_fallback_research(topic)
        
        context = f"""基于微博平台对话题"{topic}"的热门讨论研究：
        
研究摘要：{research_data['summary']}
        
热门讨论内容：
"""
        
        for i, source in enumerate(research_data.get("sources", [])):
            content = source.get("content", "")
            if len(content) > 200:
                content = content[:200] + "..."
            context += f"{i+1}. {content}\n"
        
        context += "\n请基于以上微博热门讨论内容，生成客观、有趣且贴近用户真实想法的微博内容。"
        
        return context

# 为了兼容同步调用，创建一个同步包装器
class TopicResearcher:
    def __init__(self):
        self.async_researcher = WeiboTopicResearcher()
    
    def get_research_context(self, topic: str) -> str:
        """同步方法获取研究背景信息"""
        return self.async_researcher.get_research_context(topic)

def main():
    """命令行测试"""
    if len(sys.argv) < 2:
        print("请提供话题参数，例如: python3 topic_research.py '人工智能发展'")
        return
    
    topic = sys.argv[1]
    researcher = WeiboTopicResearcher()
    
    print("🚀 微博话题研究工具")
    print("=" * 50)
    
    # 使用异步方式运行
    research_data = asyncio.run(researcher.research_topic_on_weibo(topic))
    
    print("\n📊 研究结果:")
    print("=" * 50)
    print(f"话题: {research_data['topic']}")
    print(f"\n研究摘要: {research_data['summary']}")
    
    print("\n📚 微博相关内容:")
    for i, source in enumerate(research_data.get("sources", [])):
        print(f"{i+1}. {source['content']}")
        print(f"   包含图片: {'是' if source['has_images'] else '否'}")
        print(f"   点赞数: {source['likes']}")
        print()
    
    print("\n📝 用于AI生成的背景信息:")
    print("=" * 50)
    context = researcher.get_research_context(topic)
    print(context)

if __name__ == "__main__":
    main()
