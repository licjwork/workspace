#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博图片上传工具
用于将本地 uploads 文件夹中的图片上传到 m.weibo.cn 的发布区域。
"""

import asyncio
import os
import sys
from pathlib import Path
import argparse
from playwright.async_api import async_playwright

class WeiboImageUploader:
    def __init__(self, persistent_session=True):
        self.profile_dir = Path.home() / '.weibo-image-profile'
        self.uploads_dir = Path('/home/ubuntu/.openclaw/workspace/uploads')
        self.persistent_session = persistent_session
        
        if not self.uploads_dir.exists():
            print(f"⚠️ 目录 {self.uploads_dir} 不存在，将尝试创建")
            self.uploads_dir.mkdir(parents=True, exist_ok=True)

    async def upload_images(self, text="", files=None, publish=False):
        """
        上传图片到微博
        
        Args:
            text (str): 微博正文
            files (list): 要上传的文件名列表，如果为 None 则上传 uploads 下所有 png
            publish (bool): 是否点击发送按钮
        """
        async with async_playwright() as p:
            print("🚀 正在启动浏览器...")
            
            # 使用持久化上下文以复用登录状态
            if self.persistent_session:
                self.profile_dir.mkdir(parents=True, exist_ok=True)
                context = await p.chromium.launch_persistent_context(
                    str(self.profile_dir),
                    headless=False, # 建议非静默模式，方便观察或手动登录
                    viewport={'width': 400, 'height': 800}, # 模拟手机视图
                    user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
                )
            else:
                browser = await p.chromium.launch(headless=False)
                context = await browser.new_context(
                    viewport={'width': 400, 'height': 800},
                    user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
                )

            page = await context.new_page()
            
            # 1. 访问发布页面
            print("🌐 访问微博发布页面...")
            await page.goto('https://m.weibo.cn/compose/', wait_until='networkidle')
            await asyncio.sleep(2)

            # 检查是否需要登录
            if "login" in page.url or await page.query_selector('.login-wrapper'):
                print("🔑 检测到未登录状态，请在浏览器窗口中完成登录...")
                # 等待用户登录，直到跳转回 compose 页面
                while "compose" not in page.url:
                    await asyncio.sleep(1)
                print("✅ 登录成功，继续操作")

            # 2. 填写正文
            if text:
                print(f"📝 填写正文: {text[:20]}...")
                await page.fill('textarea', text)

            # 3. 准备文件路径
            if files:
                file_paths = [str(self.uploads_dir / f) for f in files]
            else:
                # 默认获取所有 png
                file_paths = [str(f) for f in self.uploads_dir.glob('*.png')]

            if not file_paths:
                print("❌ 没有找到待上传的图片文件")
                await asyncio.sleep(3)
                await context.close()
                return

            print(f"📸 准备上传 {len(file_paths)} 张图片...")

            # 4. 触发上传
            # 微博移动端通常有一个隐藏的 input[type="file"]
            file_input = await page.query_selector('input[type="file"]')
            if not file_input:
                # 有时需要点击“图片”图标才会显示 input
                image_icon = await page.query_selector('.m-font-pic')
                if image_icon:
                    await image_icon.click()
                    await asyncio.sleep(1)
                    file_input = await page.query_selector('input[type="file"]')

            if file_input:
                await file_input.set_input_files(file_paths)
                print("⏳ 等待图片上传完成...")
                # 微博上传通常有进度条或缩略图预览，等待一段时间
                await asyncio.sleep(5) 
            else:
                print("❌ 未能定位到文件上传控件")

            # 5. 发布或保持
            if publish:
                print("🚀 正在点击发送按钮...")
                send_btn = await page.query_selector('a.m-send-btn')
                if send_btn:
                    await send_btn.click()
                    await asyncio.sleep(3)
                    print("🎉 发布成功！")
                else:
                    print("❌ 未找到发送按钮")
            else:
                print("💾 图片已进入编辑区域，程序将保持 10 秒供你确认...")
                await asyncio.sleep(10)

            await context.close()
            print("✅ 任务完成")

def main():
    parser = argparse.ArgumentParser(description='微博图片上传工具')
    parser.add_argument('--text', type=str, default="", help='微博正文内容')
    parser.add_argument('--files', nargs='+', help='指定 uploads 目录下的文件名 (如: img1.png img2.png)')
    parser.add_argument('--publish', action='store_true', help='上传后立即发布')
    parser.add_argument('--no-persist', action='store_true', help='不使用持久化会话')
    
    args = parser.parse_args()
    
    uploader = WeiboImageUploader(persistent_session=not args.no_persist)
    asyncio.run(uploader.upload_images(text=args.text, files=args.files, publish=args.publish))

if __name__ == '__main__':
    main()
