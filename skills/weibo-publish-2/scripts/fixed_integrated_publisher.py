#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博全自动发布工具 (修复版)
集成：热搜搜图技能 + AI内容生成技能 + 图片上传发布技能
"""

import asyncio
import os
from playwright.async_api import async_playwright
import sys
from pathlib import Path
import argparse

# 动态添加路径以确保可以导入各个技能模块
WORKSPACE_ROOT = Path('/home/ubuntu/.openclaw/workspace')
sys.path.append(str(WORKSPACE_ROOT / 'skills/weibo-hot-search-images/scripts'))
sys.path.append(str(WORKSPACE_ROOT / 'skills/weibo-image-upload/scripts'))
sys.path.append(str(WORKSPACE_ROOT / 'skills/weibo-publish-2/scripts'))

# 导入各个独立技能
try:
    from weibo_image_fetcher import WeiboImageFetcher
    # from stable_publisher_mobile_method import StableWeiboPublisherMobileMethod
    from improved_content_generator import call_dogegg_ai
    print("✅ 所有技能模块导入成功")
except ImportError as e:
    print(f"❌ 技能模块导入失败: {e}")
    # 提供降级兜底（如果模块不存在）
    class WeiboImageFetcher: 
        def __init__(self, **kwargs): pass
        async def search_topic_images(self, topic, **kwargs): return []
    class StableWeiboPublisherMobileMethod:
        def __init__(self, topic, **kwargs): pass
        async def init_browser(self): pass
        async def check_login_status(self): return True
        async def publish_weibo(self, content): pass
        async def cleanup(self): pass
    def call_dogegg_ai(topic, context): return f"关于#{topic}#的内容"

class StableWeiboPublisherMobileMethod:
    def __init__(self, topic, image_paths=None):
        self.topic = topic
        self.image_paths = image_paths or []
        self.user_data_dir = os.path.expanduser('~/.weibo-profile')
        self.browser = None
        self.page = None
        self.playwright = None
        
    async def init_browser(self):
        print("🚀 正在启动Playwright浏览器...")
        self.playwright = await async_playwright().start()
        
        self.browser = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=False,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        self.page = await self.browser.new_page()
        print("✅ 浏览器初始化完成")

    async def check_login_status(self):
        print("🔍 检查微博登录状态...")
        
        try:
            await self.page.goto('https://weibo.com', wait_until='networkidle')
            await self.page.wait_for_timeout(2000)
            
            current_url = self.page.url
            if 'login' in current_url or 'passport' in current_url:
                print("❌ 当前在登录页面，需要重新登录")
                return False
            else:
                print("✅ 检测到已登录状态")
                return True
                
        except Exception as e:
            print(f"❌ 检查登录状态失败: {e}")
            return False

    async def publish_weibo(self, content):
        print("\n🚀 正在发布微博...")
        
        try:
            await self.page.goto('https://weibo.com/', wait_until='networkidle')
            await self.page.wait_for_timeout(5000)
            
            textarea_selector = 'textarea._input_13iqr_8'
            await self.page.wait_for_selector(textarea_selector, timeout=10000)
            
            await self.page.fill(textarea_selector, content)
            await self.page.wait_for_timeout(2000)
            
            # 上传图片
            if self.image_paths:
                print(f"📸 正在上传 {len(self.image_paths)} 张图片...")
                
                try:
                    # 查找文件输入框
                    file_input = await self.page.query_selector('input[type="file"]._file_hqmwy_20')
                    
                    if file_input:
                        await file_input.set_input_files(self.image_paths)
                        await self.page.wait_for_timeout(35000)  # 增加等待时间到35秒，确保图片完全上传
                        print("✅ 图片上传成功")
                    else:
                        print("❌ 未找到文件输入框")
                        
                except Exception as e:
                    print(f"❌ 图片上传失败: {e}")
            
            send_button_selector = 'button.woo-button-main.woo-button-flat.woo-button-primary'
            await self.page.wait_for_selector(send_button_selector, timeout=10000)
            await self.page.click(send_button_selector)
            
            await self.page.wait_for_timeout(5000)
            
            print("✅ 微博发布成功！")
            return True
            
        except Exception as e:
            print(f"❌ 发布失败: {e}")
            return False

    async def cleanup(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("🧹 资源清理完成")

class FixedUnifiedWeiboSkillOrchestrator:
    def __init__(self):
        # 统一路径：按照用户要求设置
        self.uploads_dir = Path('/home/ubuntu/.openclaw/workspace/uploads')
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化各个技能实例
        self.fetcher = WeiboImageFetcher(uploads_dir=str(self.uploads_dir))
        
    async def run_full_workflow(self, topic, images_count=3, publish=False):
        print(f"\n🌟 开始执行全技能整合工作流: {topic}")
        print("-" * 40)
        
        # 1. 执行【热搜图片获取技能】
        print("Step 1: 正在运行图片获取技能...")
        image_paths = await self.fetcher.search_topic_images(topic, max_images=images_count)
        if not image_paths:
            print("⚠️ 未能获取到图片，将仅发布文字内容")
        else:
            print(f"✅ 图片获取成功，共 {len(image_paths)} 张")

        # 2. 执行【AI 内容生成技能】
        print("\nStep 2: 正在运行 AI 内容生成技能...")
        content = call_dogegg_ai(topic, f"针对话题#{topic}#生成一段博文")
        if not content:
            content = f"分享话题：#{topic}#"
        print(f"📝 生成内容: {content[:30]}...")

        # 3. 执行【图片上传与发布技能】
        print("\nStep 3: 正在运行图片上传与发布技能 (修复版)...")
        
        # 使用修复的发布方法
        publisher = StableWeiboPublisherMobileMethod(topic, image_paths if image_paths else [])
        
        try:
            await publisher.init_browser()
            
            if not await publisher.check_login_status():
                print("❌ 微博未登录，请先运行登录流程")
            else:
                if publish:
                    await publisher.publish_weibo(content)
                else:
                    print("⚠️ publish 参数未设置，当前流程为：仅生成和获取图片，不执行点击发布。")
        except Exception as e:
            print(f"❌ 发布过程中发生错误: {e}")
        finally:
            await publisher.cleanup()
        
        print("-" * 40)
        print("🏁 全技能整合工作流执行完毕！")

async def main():
    parser = argparse.ArgumentParser(description='微博全自动发布工具 (修复版)')
    parser.add_argument('--topic', type=str, required=True, help='微博话题')
    parser.add_argument('--images', type=int, default=3, help='配图数量')
    parser.add_argument('--publish', action='store_true', help='是否直接发布')
    
    args = parser.parse_args()
    
    orchestrator = FixedUnifiedWeiboSkillOrchestrator()
    await orchestrator.run_full_workflow(
        topic=args.topic, 
        images_count=args.images, 
        publish=args.publish
    )

if __name__ == '__main__':
    asyncio.run(main())
