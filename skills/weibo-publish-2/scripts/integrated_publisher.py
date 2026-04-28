#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博全自动发布工具 (组合技能版)
流程：搜索话题图片 -> AI生成内容 -> 自动上传并发布
"""

import asyncio
import os
import sys
import re
import io
import time
import requests
from pathlib import Path
import argparse
from urllib.parse import quote
from PIL import Image
from playwright.async_api import async_playwright

# 导入现有的 AI 生成逻辑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from improved_content_generator import call_dogegg_ai
except ImportError:
    def call_dogegg_ai(topic, context):
        return f"关于#{topic}#的一些想法：这是一个非常有意思的话题。 #微博热搜#"

class IntegratedWeiboPublisher:
    def __init__(self, uploads_dir=None):
        self.profile_dir = Path.home() / '.weibo-image-profile'
        self.uploads_dir = Path(uploads_dir) if uploads_dir else Path('/home/ubuntu/.openclaw/workspace/uploads')
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        
    async def fetch_images(self, page, topic, max_images=3):
        """利用当前浏览器页面搜索并获取话题图片"""
        print(f"🖼️ 正在搜索话题 '{topic}' 的图片...")
        
        # 访问搜索页
        search_url = f'https://m.weibo.cn/search?containerid=100103type%3D1%26q={quote(topic)}'
        await page.goto(search_url, wait_until='networkidle')
        await asyncio.sleep(2)
        
        # 提取图片 URL
        image_urls = await page.evaluate("""() => {
            const imgs = Array.from(document.querySelectorAll('img'));
            return imgs.map(img => img.src || img.dataset.src)
                .filter(src => src && (src.includes('sinaimg.cn/large') || src.includes('sinaimg.cn/mw690')));
        }""")
        
        image_urls = list(dict.fromkeys(image_urls))[:max_images]
        
        downloaded_paths = []
        if not image_urls:
            print(f"⚠️ 未找到直接图片，尝试进入博文列表...")
            # 这里可以增加更深层的抓取逻辑，目前先处理直接显示的
        else:
            print(f"✅ 找到 {len(image_urls)} 个图片链接，正在下载...")
            for i, url in enumerate(image_urls):
                path = self._download_and_convert(url, f"{topic}_{i+1}")
                if path:
                    downloaded_paths.append(path)
        
        return downloaded_paths

    def _download_and_convert(self, url, filename):
        """下载并转换为 PNG"""
        try:
            if url.startswith('//'): url = 'https:' + url
            headers = {'Referer': 'https://weibo.com/'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            img = Image.open(io.BytesIO(response.content))
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGBA")
            else:
                img = img.convert("RGB")
            
            safe_filename = re.sub(r'[^\w\-_\.]', '_', filename)
            file_path = self.uploads_dir / f"{safe_filename}.png"
            img.save(file_path, "PNG")
            return str(file_path)
        except Exception as e:
            print(f"  ❌ 下载失败 {url}: {e}")
            return None

    async def publish(self, page, topic, content, image_paths):
        """上传图片并发布博文"""
        print(f"🚀 正在发布微博...")
        
        # 1. 进入发布页
        await page.goto('https://m.weibo.cn/compose/', wait_until='networkidle')
        await asyncio.sleep(2)
        
        # 2. 填写正文
        textarea = await page.query_selector('textarea')
        if textarea:
            await textarea.fill(content)
            print("📝 正文填写完成")
        
        # 3. 上传图片
        if image_paths:
            file_input = await page.query_selector('input[type="file"]')
            if not file_input:
                # 尝试点击图片图标触发 input
                pic_icon = await page.query_selector('.m-font-pic')
                if pic_icon: await pic_icon.click()
                await asyncio.sleep(1)
                file_input = await page.query_selector('input[type="file"]')
            
            if file_input:
                await file_input.set_input_files(image_paths)
                print(f"⏳ 正在上传 {len(image_paths)} 张图片...")
                await asyncio.sleep(5) # 等待上传完成
            else:
                print("❌ 未能定位上传控件")

        # 4. 点击发布
        send_btn = await page.query_selector('a.m-send-btn')
        if send_btn:
            await send_btn.click()
            print("🎉 发布指令已发送！")
            await asyncio.sleep(3)
            return True
        else:
            print("❌ 未找到发布按钮")
            return False

    async def run(self, topic, max_images=3, do_publish=False):
        async with async_playwright() as p:
            print(f"🎬 开始执行组合技能 - 话题: {topic}")
            
            # 1. 启动浏览器 (复用 session)
            self.profile_dir.mkdir(parents=True, exist_ok=True)
            context = await p.chromium.launch_persistent_context(
                str(self.profile_dir),
                headless=False,
                viewport={'width': 400, 'height': 800},
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
            )
            page = await context.new_page()
            
            try:
                # 2. 搜图
                image_paths = await self.fetch_images(page, topic, max_images)
                
                # 3. 生成内容
                content = call_dogegg_ai(topic, f"热门话题：{topic}")
                print(f"✍️ AI 生成内容: {content[:30]}...")
                
                # 4. 发布
                success = await self.publish(page, topic, content, image_paths)
                
                if success:
                    print("✅ 全流程执行成功！")
                else:
                    print("❌ 发布阶段出现异常")
                
                if not do_publish:
                    print("💡 当前为预览模式，浏览器将保持 10 秒供检查...")
                    await asyncio.sleep(10)
                
            except Exception as e:
                print(f"❌ 运行过程中出错: {e}")
            finally:
                await context.close()

async def main():
    parser = argparse.ArgumentParser(description='微博全自动发布工具 (组合技能)')
    parser.add_argument('--topic', type=str, required=True, help='发布的话题名称')
    parser.add_argument('--images', type=int, default=3, help='配图数量')
    parser.add_argument('--publish', action='store_true', help='是否执行最终发布')
    
    args = parser.parse_args()
    
    publisher = IntegratedWeiboPublisher()
    await publisher.run(args.topic, max_images=args.images, do_publish=args.publish)

if __name__ == '__main__':
    asyncio.run(main())
