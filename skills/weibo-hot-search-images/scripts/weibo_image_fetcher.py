#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜图片获取工具 - 增强版 (基于 Playwright)
用于从微博热搜话题中提取和下载相关图片，支持自动转换 PNG。
"""

import asyncio
import re
import io
import time
import requests
from pathlib import Path
import argparse
from urllib.parse import quote
from PIL import Image
from playwright.async_api import async_playwright

class WeiboImageFetcher:
    def __init__(self, uploads_dir=None):
        # 使用项目下的 uploads 目录
        self.uploads_dir = Path(uploads_dir) if uploads_dir else Path('/home/ubuntu/.openclaw/workspace/uploads')
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        print(f"📂 图片将保存至: {self.uploads_dir}")
        
    async def get_hot_search_list(self, limit=10):
        """获取微博热搜榜单"""
        print("📊 正在获取微博热搜榜单...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # 使用 AJAX 接口获取热搜数据
                await page.goto('https://weibo.com/ajax/side/hotSearch', wait_until='networkidle')
                content = await page.content()
                
                # 尝试解析 JSON (因为直接访问 AJAX URL 浏览器会渲染成预览)
                import json
                text = await page.evaluate("() => document.body.innerText")
                data = json.loads(text)
                
                topics = []
                realtime_data = data.get('data', {}).get('realtime', [])
                
                for i, item in enumerate(realtime_data):
                    if i >= limit: break
                    title = item.get('word', '')
                    if title:
                        topics.append({
                            'title': title,
                            'rank': i + 1
                        })
                
                await browser.close()
                if topics:
                    print(f"✅ 成功获取 {len(topics)} 个实时热搜话题")
                    return topics
            except Exception as e:
                print(f"❌ 自动获取失败: {e}")
                await browser.close()
                return self._get_mock_hot_topics(limit)

    def _get_mock_hot_topics(self, limit):
        mock_topics = [
            {"title": "网红白冰偷税911.18万", "rank": 1},
            {"title": "五一假期安全", "rank": 2},
            {"title": "人工智能发展", "rank": 3}
        ]
        return mock_topics[:limit]

    async def search_topic_images(self, topic, max_images=5):
        """搜索并下载话题图片"""
        print(f"🖼️ 正在搜索话题 '{topic}' 的图片...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                # 访问移动端搜索页，对图片展示更友好
                search_url = f'https://m.weibo.cn/search?containerid=100103type%3D1%26q={quote(topic)}'
                await page.goto(search_url, wait_until='networkidle')
                await asyncio.sleep(2) # 等待渲染
                
                # 滚动一下页面以加载更多图片
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight/2)")
                await asyncio.sleep(1)
                
                # 提取所有图片 URL
                image_urls = await page.evaluate("""() => {
                    const imgs = Array.from(document.querySelectorAll('img'));
                    return imgs.map(img => img.src || img.dataset.src)
                        .filter(src => src && (src.includes('sinaimg.cn/large') || src.includes('sinaimg.cn/mw690') || src.includes('sinaimg.cn/orj360')));
                }""")
                
                # 去重
                image_urls = list(dict.fromkeys(image_urls))[:max_images]
                
                if not image_urls:
                    print(f"❌ 未找到话题 '{topic}' 的有效图片")
                    await browser.close()
                    return []
                
                print(f"✅ 找到 {len(image_urls)} 个有效图片链接")
                
                downloaded_files = []
                for i, url in enumerate(image_urls):
                    file_path = self._download_image(url, f"{topic}_{i+1}")
                    if file_path:
                        downloaded_files.append(file_path)
                        print(f"  ✅ 下载并转换成功: {file_path}")
                
                await browser.close()
                return downloaded_files
                
            except Exception as e:
                print(f"❌ 搜索失败: {e}")
                await browser.close()
                return []

    def _download_image(self, url, filename):
        """下载并转换为 PNG"""
        try:
            # 确保 URL 是 https
            if url.startswith('//'): url = 'https:' + url
            
            # 微博图床有时需要 Referer
            headers = {'Referer': 'https://weibo.com/'}
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            image_data = io.BytesIO(response.content)
            with Image.open(image_data) as img:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")
                
                safe_filename = re.sub(r'[^\w\-_\.]', '_', filename)
                file_path = self.uploads_dir / f"{safe_filename}.png"
                img.save(file_path, "PNG")
            
            return str(file_path)
        except Exception as e:
            print(f"  ❌ 下载或转换失败 {url}: {e}")
            return None

async def main():
    parser = argparse.ArgumentParser(description='微博热搜图片获取工具 (Playwright版)')
    parser.add_argument('--topic', type=str, help='指定话题名称')
    parser.add_argument('--hot-search', action='store_true', help='获取热搜榜单图片')
    parser.add_argument('--limit', type=int, default=5, help='热搜话题数量限制')
    parser.add_argument('--images-per-topic', type=int, default=3, help='每个话题下载的图片数量')
    
    args = parser.parse_args()
    fetcher = WeiboImageFetcher()
    
    if args.topic:
        await fetcher.search_topic_images(args.topic, args.images_per_topic)
    elif args.hot_search:
        topics = await fetcher.get_hot_search_list(args.limit)
        for t in topics:
            await fetcher.search_topic_images(t['title'], args.images_per_topic)
    else:
        print("请指定 --topic 或 --hot-search 参数")

if __name__ == '__main__':
    asyncio.run(main())
