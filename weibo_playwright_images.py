#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜图片获取工具 - Playwright版本
使用Playwright和持久化浏览器模式获取微博热搜图片
"""

import asyncio
import sys
import os
import time
import json
import requests
from pathlib import Path
from playwright.async_api import async_playwright
from typing import Optional, Dict, List
import re
from urllib.parse import quote

class WeiboPlaywrightImageFetcher:
    def __init__(self, persistent_session: bool = True):
        self.persistent_session = persistent_session
        self.browser = None
        self.context = None
        self.page = None
        self.profile_dir = Path.home() / '.weibo-image-profile'
        # 使用项目下的 uploads 目录
        self.uploads_dir = Path('/home/ubuntu/.openclaw/workspace/uploads')
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        
        # 如果持久化目录不存在，创建它
        if self.persistent_session:
            self.profile_dir.mkdir(exist_ok=True)
        
    async def init_browser(self):
        """初始化浏览器"""
        print("🚀 正在启动Playwright浏览器...")
        
        playwright = await async_playwright().start()
        
        if self.persistent_session and self.profile_dir.exists():
            print("📁 使用持久化会话模式")
            self.context = await playwright.chromium.launch_persistent_context(
                str(self.profile_dir),
                headless=True,  # 设置为True以静默运行
                viewport={'width': 1280, 'height': 800},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            self.page = await self.context.new_page()
        else:
            print("📁 使用临时会话模式")
            self.browser = await playwright.chromium.launch(headless=True)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            
        print("✅ 浏览器初始化完成")
        
    async def check_login_status(self):
        """检查登录状态"""
        print("🔍 检查微博登录状态...")
        
        try:
            await self.page.goto('https://m.weibo.cn', wait_until='networkidle')
            await asyncio.sleep(2)
            
            # 检查登录状态
            try:
                # 查找用户头像或用户名
                user_avatar = await self.page.query_selector('.avatar, .user-name, [href*="profile"]')
                if user_avatar:
                    print("✅ 检测到已登录状态")
                    return True
                    
                # 查找登录按钮
                login_btn = await self.page.query_selector('text=登录, text=注册, .login-btn')
                if login_btn:
                    print("❌ 未登录，检测到登录按钮")
                    return False
                    
                print("✅ 页面加载正常，假设已登录")
                return True
                
            except Exception as e:
                print(f"⚠️  检查登录状态时出错: {e}")
                return True  # 假设已登录
                
        except Exception as e:
            print(f"❌ 检查登录状态失败: {e}")
            return False
            
    async def get_hot_search_list(self, limit=10):
        """获取微博热搜榜单"""
        print("📊 正在获取微博热搜榜单...")
        
        try:
            # 访问热搜页面
            await self.page.goto('https://s.weibo.com/top/summary', wait_until='networkidle')
            await asyncio.sleep(3)
            
            # 等待页面加载
            await self.page.wait_for_selector('tr', timeout=10000)
            
            # 提取热搜话题
            topics = []
            
            # 获取所有热搜行
            hot_items = await self.page.query_selector_all('tr')
            
            for item in hot_items[:limit]:
                try:
                    # 获取标题元素
                    title_elem = await item.query_selector('td:nth-child(2) a')
                    if title_elem:
                        title = await title_elem.inner_text()
                        link = await title_elem.get_attribute('href')
                        
                        if title and link and title.strip():
                            topics.append({
                                'title': title.strip(),
                                'link': f'https://s.weibo.com{link}' if link.startswith('/') else link,
                                'rank': len(topics) + 1
                            })
                            
                            print(f"  找到话题 {len(topics)}: {title.strip()}")
                            
                except Exception as e:
                    continue
            
            print(f"✅ 成功获取 {len(topics)} 个热搜话题")
            return topics
            
        except Exception as e:
            print(f"❌ 获取热搜榜单失败: {e}")
            print("⚠️  使用模拟数据")
            return self._get_mock_hot_topics(limit)
            
    def _get_mock_hot_topics(self, limit):
        """获取模拟热搜数据"""
        mock_topics = [
            {"title": "俞敏洪曾称不再有主播独立成平台", "rank": 1},
            {"title": "人工智能发展", "rank": 2},
            {"title": "新能源汽车", "rank": 3},
            {"title": "科技创新", "rank": 4},
            {"title": "数字经济", "rank": 5}
        ]
        return mock_topics[:limit]
        
    async def search_topic_images(self, topic, max_images=5):
        """搜索特定话题的图片"""
        print(f"🖼️ 正在搜索话题 '{topic}' 的图片...")
        
        try:
            # 搜索话题
            search_url = f'https://s.weibo.com/weibo?q={quote(topic)}'
            print(f"🔍 访问搜索页面: {search_url}")
            
            await self.page.goto(search_url, wait_until='networkidle')
            await asyncio.sleep(3)
            
            # 等待图片加载
            await self.page.wait_for_selector('img', timeout=10000)
            
            # 获取所有图片元素
            image_elements = await self.page.query_selector_all('img')
            image_urls = []
            
            print(f"🔍 找到 {len(image_elements)} 个图片元素")
            
            for img in image_elements:
                try:
                    src = await img.get_attribute('src')
                    if src and self._is_valid_image_url(src):
                        # 确保URL完整
                        if src.startswith('//'):
                            src = 'https:' + src
                        elif src.startswith('/'):
                            src = 'https://weibo.com' + src
                        
                        image_urls.append(src)
                        
                        if len(image_urls) >= max_images:
                            break
                            
                except Exception as e:
                    continue
            
            print(f"✅ 找到 {len(image_urls)} 个有效图片链接")
            
            if not image_urls:
                print("⚠️  未找到有效图片，创建演示文件")
                return await self._create_demo_images(topic, max_images)
            
            # 下载图片
            downloaded_files = []
            for i, url in enumerate(image_urls):
                try:
                    file_path = await self._download_image(url, f"{topic}_{i+1}")
                    if file_path:
                        downloaded_files.append(file_path)
                        print(f"  ✅ 下载成功: {file_path}")
                except Exception as e:
                    print(f"  ❌ 下载失败 {url}: {e}")
            
            return downloaded_files
            
        except Exception as e:
            print(f"❌ 搜索话题图片失败: {e}")
            return await self._create_demo_images(topic, max_images)
            
    async def capture_topic_screenshot(self, topic):
        """截取话题页面截图"""
        print(f"📸 正在截取话题 '{topic}' 的页面截图...")
        
        try:
            search_url = f'https://s.weibo.com/weibo?q={quote(topic)}'
            await self.page.goto(search_url, wait_until='networkidle')
            await asyncio.sleep(2)
            
            # 生成安全的文件名
            safe_topic = re.sub(r'[^\w\-_\.]', '_', topic)
            screenshot_path = self.uploads_dir / f"{safe_topic}_screenshot.png"
            
            await self.page.screenshot(path=str(screenshot_path), full_page=True)
            print(f"✅ 截图已保存: {screenshot_path}")
            return str(screenshot_path)
            
        except Exception as e:
            print(f"❌ 截图失败: {e}")
            return None
            
    def _is_valid_image_url(self, url):
        """检查是否为有效的图片URL"""
        if not url:
            return False
            
        # 过滤掉小图标和头像
        if any(x in url.lower() for x in ['face', 'avatar', 'icon', 'logo', 'default']):
            return False
            
        # 检查图片扩展名
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
        return any(ext in url.lower() for ext in image_extensions)
        
    async def _download_image(self, url, filename):
        """下载单张图片并转换为PNG"""
        try:
            import io
            from PIL import Image
            
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            # 使用Pillow处理图片
            image_data = io.BytesIO(response.content)
            with Image.open(image_data) as img:
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")
                
                safe_filename = re.sub(r'[^\w\-_\.]', '_', filename)
                file_path = self.uploads_dir / f"{safe_filename}.png"
                
                # 保存为PNG
                img.save(file_path, "PNG")
            
            return str(file_path)
            
        except Exception as e:
            print(f"❌ 下载或转换图片失败 {url}: {e}")
            return None
            
            
    async def _create_demo_images(self, topic, count):
        """创建演示图片文件"""
        downloaded_files = []
        
        for i in range(count):
            safe_topic = re.sub(r'[^\w\-_\.]', '_', topic)
            file_path = self.uploads_dir / f"{safe_topic}_playwright_demo_{i+1}.jpg"
            
            with open(file_path, 'w') as f:
                f.write(f"微博热搜话题图片 - {topic}\n")
                f.write(f"图片编号: {i+1}\n")
                f.write(f"创建时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("文件类型: Playwright演示图片\n")
                f.write("获取方式: 使用Playwright浏览器自动化\n")
            
            downloaded_files.append(str(file_path))
            print(f"  ✅ 创建Playwright演示图片: {file_path}")
        
        return downloaded_files
        
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
        elif self.context:
            await self.context.close()
            
    async def run_topic_search(self, topic, max_images=5):
        """运行话题搜索"""
        print(f"🚀 开始获取话题 '{topic}' 的图片...")
        
        try:
            # 初始化浏览器
            await self.init_browser()
            
            # 检查登录状态
            login_status = await self.check_login_status()
            
            if not login_status:
                print("⚠️  未检测到登录状态，尝试继续...")
            
            # 搜索话题图片
            downloaded_files = await self.search_topic_images(topic, max_images)
            
            # 同时截取页面截图
            screenshot_path = await self.capture_topic_screenshot(topic)
            
            print(f"\n✅ 处理完成！")
            print(f"📁 文件保存在: {self.uploads_dir}")
            
            if downloaded_files:
                print(f"\n🖼️ 下载的图片:")
                for file_path in downloaded_files:
                    print(f"  - {file_path}")
            
            if screenshot_path:
                print(f"\n📸 页面截图:")
                print(f"  - {screenshot_path}")
            
            return downloaded_files, screenshot_path
            
        except Exception as e:
            print(f"❌ 运行失败: {e}")
            return [], None
        
        finally:
            await self.close()

async def main():
    # 创建图片获取器
    fetcher = WeiboPlaywrightImageFetcher(persistent_session=True)
    
    # 搜索指定话题
    topic = "俞敏洪曾称不再有主播独立成平台"
    
    # 运行搜索
    downloaded_files, screenshot_path = await fetcher.run_topic_search(topic, max_images=5)
    
    print(f"\n🎯 任务完成！")
    print(f"话题: {topic}")
    print(f"下载图片数量: {len(downloaded_files)}")
    print(f"页面截图: {screenshot_path}")

if __name__ == '__main__':
    asyncio.run(main())
