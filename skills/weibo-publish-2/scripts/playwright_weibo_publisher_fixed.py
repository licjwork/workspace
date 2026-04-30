#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright 微博发布器 - 修复版，支持图片上传
基于移动端发布逻辑
"""

import asyncio
import os
import sys
from pathlib import Path

class PlaywrightWeiboPublisher:
    def __init__(self, topic, persistent_session=True):
        self.topic = topic
        self.persistent_session = persistent_session
        self.user_data_dir = os.path.expanduser('~/.weibo-profile')
        self.browser = None
        self.page = None
        self.playwright = None
        
    async def init_browser(self):
        """初始化浏览器"""
        from playwright.async_api import async_playwright
        
        print("🚀 正在启动Playwright浏览器...")
        self.playwright = await async_playwright().start()
        
        if self.persistent_session:
            print("📁 使用长期会话模式，用户数据将保存")
            self.browser = await self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.user_data_dir,
                headless=False,
                viewport={'width': 390, 'height': 844},
                device_scale_factor=3.0,
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
            )
            self.page = self.browser.pages[0] if self.browser.pages else await self.browser.new_page()
        else:
            print("📁 使用临时会话模式")
            browser = await self.playwright.chromium.launch(headless=False)
            self.browser = await browser.new_context(
                viewport={'width': 390, 'height': 844},
                device_scale_factor=3.0,
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
            )
            self.page = await self.browser.new_page()
            
        print("✅ 浏览器初始化完成")
        
    async def check_login_status(self):
        """检查登录状态"""
        print("🔍 检查微博登录状态...")
        
        try:
            await self.page.goto('https://m.weibo.cn', wait_until='networkidle')
            await asyncio.sleep(2)
            
            # 检查是否有登录相关的元素
            login_elements = await self.page.query_selector_all('.login-btn, .login, [data-login], .btn-login')
            
            if login_elements:
                print("❌ 检测到登录按钮，需要登录")
                return False
            else:
                print("✅ 检测到已登录状态")
                return True
                
        except Exception as e:
            print(f"⚠️ 检查登录状态时出错: {e}")
            return False
            
    async def publish_weibo(self, content, image_paths=None):
        """发布微博 - 移动端版本"""
        print("\n🚀 正在发布微博...")
        
        try:
            # 导航到发布页面
            await self.page.goto('https://m.weibo.cn/compose', wait_until='networkidle')
            await asyncio.sleep(3)
            
            # 等待文本框出现
            textarea = await self.page.query_selector('textarea')
            if not textarea:
                print("❌ 未找到文本输入框")
                return False
                
            # 输入内容
            await textarea.fill(content)
            await asyncio.sleep(1)
            print("✅ 已输入微博内容")
            
            # 上传图片
            if image_paths:
                print(f"📸 正在上传 {len(image_paths)} 张图片...")
                
                # 点击图片上传按钮
                image_btn = await self.page.query_selector('.m-font-pic')
                if image_btn:
                    await image_btn.click()
                    await asyncio.sleep(2)
                    
                    # 上传每张图片
                    for image_path in image_paths:
                        if os.path.exists(image_path):
                            file_input = await self.page.query_selector('input[type="file"]')
                            if file_input:
                                await file_input.set_input_files(image_path)
                                await asyncio.sleep(2)
                                print(f"✅ 已上传图片: {os.path.basename(image_path)}")
                            else:
                                print(f"❌ 未找到文件输入框，跳过图片: {image_path}")
                        else:
                            print(f"❌ 图片文件不存在: {image_path}")
                else:
                    print("⚠️ 未找到图片上传按钮")
            
            # 点击发布按钮
            publish_btn = await self.page.query_selector('a.m-send-btn')
            if publish_btn:
                await publish_btn.click()
                await asyncio.sleep(3)
                print("✅ 微博发布成功！")
                return True
            else:
                print("❌ 未找到发布按钮")
                return False
                
        except Exception as e:
            print(f"❌ 发布过程中出错: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    async def close(self):
        """关闭浏览器"""
        try:
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            print("🧹 资源清理完成")
        except Exception as e:
            print(f"⚠️ 清理资源时出错: {e}")
