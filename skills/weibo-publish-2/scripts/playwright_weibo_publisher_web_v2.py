#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright 微博发布器 - 网页版 v2
基于 stable_publisher_mobile_method.py 的完整网页版发布逻辑
包含完整的图片上传功能
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
                viewport={'width': 1280, 'height': 800}
            )
            self.page = self.browser.pages[0] if self.browser.pages else await self.browser.new_page()
        else:
            print("📁 使用临时会话模式")
            browser = await self.playwright.chromium.launch(headless=False)
            self.browser = await browser.new_context(
                viewport={'width': 1280, 'height': 800}
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
            login_elements = await self.page.query_selector_all('.login_btn, .login, [data-login], .btn-login')
            
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
        """发布微博 - 网页版 (完整图片上传功能)"""
        print("\n🚀 正在发布微博...")
        
        try:
            # 导航到发布页面
            await self.page.goto('https://m.weibo.cn/compose', wait_until='networkidle')
            await self.page.wait_for_timeout(3000)
            
            # 等待文本框出现
            textarea_selector = 'textarea'
            await self.page.wait_for_selector(textarea_selector, timeout=10000)
            
            # 输入内容
            await self.page.fill(textarea_selector, content)
            await self.page.wait_for_timeout(1000)
            print("✅ 已输入微博内容")
            
            # 上传图片（完整逻辑）
            if image_paths:
                print(f"📸 正在上传 {len(image_paths)} 张图片...")
                
                try:
                    # 借鉴移动端方法：先尝试点击图片图标
                    image_icon_selectors = [
                        '.m-font-pic',  # 移动端选择器
                        '[class*="pic"]',  # 可能的图片类名
                        '[class*="photo"]',  # 照片相关
                        '[class*="image"]',  # 图片相关
                        'button[class*="pic"]',
                        'div[class*="pic"]',
                        'span[class*="pic"]'
                    ]
                    
                    file_input = None
                    
                    # 首先查找是否已经有文件输入框
                    file_input = await self.page.query_selector('input[type="file"]._file_hqmwy_20')
                    
                    if not file_input:
                        # 尝试点击图片图标来触发文件输入框
                        for selector in image_icon_selectors:
                            try:
                                icon = await self.page.query_selector(selector)
                                if icon:
                                    await icon.click()
                                    await self.page.wait_for_timeout(1000)
                                    file_input = await self.page.query_selector('input[type="file"]._file_hqmwy_20')
                                    if file_input:
                                        print(f"✅ 通过点击 {selector} 触发了文件输入框")
                                        break
                            except:
                                continue
                    
                    # 如果还是找不到，尝试使用JavaScript触发
                    if not file_input:
                        await self.page.evaluate('''
                            // 尝试找到并点击图片上传相关的元素
                            const elements = document.querySelectorAll('*');
                            for (let el of elements) {
                                if (el.className && 
                                    (el.className.includes('pic') || 
                                     el.className.includes('photo') || 
                                     el.className.includes('image')) &&
                                    el.offsetWidth > 0 && el.offsetHeight > 0) {
                                    el.click();
                                    break;
                                }
                            }
                        ''')
                        await self.page.wait_for_timeout(1000)
                        file_input = await self.page.query_selector('input[type="file"]._file_hqmwy_20')
                    
                    # 上传文件
                    if file_input:
                        await file_input.set_input_files(image_paths)
                        await self.page.wait_for_timeout(5000)  # 等待图片上传
                        print("✅ 图片上传成功")
                    else:
                        # 最后尝试直接使用set_input_files
                        await self.page.set_input_files('input[type="file"]._file_hqmwy_20', image_paths)
                        await self.page.wait_for_timeout(5000)
                        print("✅ 使用直接方法上传成功")
                        
                except Exception as e:
                    print(f"❌ 图片上传失败: {e}")
                    import traceback
                    traceback.print_exc()
            
            # 点击发布按钮
            try:
                send_button_selector = 'a.m-send-btn'
                await self.page.wait_for_selector(send_button_selector, timeout=10000)
                await self.page.click(send_button_selector)
                
                await self.page.wait_for_timeout(3000)
                
                print("✅ 微博发布成功！")
                return True
            except Exception as e:
                print(f"❌ 点击发布按钮时出错: {e}")
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
