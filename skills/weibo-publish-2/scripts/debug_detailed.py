#!/usr/bin/env python3
import os
import sys
import asyncio
from playwright.async_api import async_playwright
from improved_content_generator import call_dogegg_ai

class DebugWeiboPublisher:
    def __init__(self, topic):
        self.topic = topic
        self.user_data_dir = os.path.expanduser('~/.weibo-profile')
        self.image_paths = ['/home/ubuntu/.openclaw/workspace/uploads/小狗每次拿外卖都把家具暴打一遍_1.png']
        
    async def debug_publish(self):
        async with async_playwright() as p:
            # 使用VNC浏览器进行调试
            context = await p.chromium.connect_over_cdp('http://localhost:18800')
            page = context.pages[0]
            
            print("🌐 访问发布页面...")
            await page.goto('https://weibo.com/compose', wait_until='networkidle')
            await page.wait_for_timeout(3000)
            
            # 填写内容
            content = "调试图片上传功能"
            await page.fill('textarea._input_13iqr_8', content)
            await page.wait_for_timeout(1000)
            
            # 上传图片前检查
            print("📋 上传前状态检查...")
            before_state = await page.evaluate('''
                () => {
                    const images = document.querySelectorAll('img');
                    const uploads = document.querySelectorAll('[class*="upload"]');
                    return {
                        imageCount: images.length,
                        uploadCount: uploads.length
                    };
                }
            ''')
            print(f"上传前: {before_state}")
            
            # 上传图片
            print(f"📸 上传图片: {self.image_paths[0]}")
            await page.set_input_files('input[type="file"]._file_hqmwy_20', self.image_paths)
            await page.wait_for_timeout(5000)
            
            # 上传后检查
            print("📋 上传后状态检查...")
            after_state = await page.evaluate('''
                () => {
                    const images = document.querySelectorAll('img');
                    const uploads = document.querySelectorAll('[class*="upload"]');
                    const previews = document.querySelectorAll('[class*="preview"]');
                    return {
                        imageCount: images.length,
                        uploadCount: uploads.length,
                        previewCount: previews.length
                    };
                }
            ''')
            print(f"上传后: {after_state}")
            
            # 保持页面打开供手动检查
            print("🔍 保持页面打开10秒供检查...")
            await page.wait_for_timeout(10000)
            
            print("✅ 调试完成")

async def main():
    topic = "调试图片上传"
    publisher = DebugWeiboPublisher(topic)
    await publisher.debug_publish()

if __name__ == "__main__":
    asyncio.run(main())
