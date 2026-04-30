#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright 微博发布器 - 网页版
基于 stable_publisher_mobile_method.py 的网页版发布逻辑
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
            await self.page.goto('https://weibo.com', wait_until='networkidle')
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
        """发布微博 - 网页版"""
        print("\n🚀 正在发布微博...")
        
        try:
            # 导航到发布页面
            await self.page.goto('https://weibo.com/compose', wait_until='networkidle')
            await self.page.wait_for_timeout(3000)
            
            # 等待文本框出现
            textarea_selector = 'textarea._input_13iqr_8'
            await self.page.wait_for_selector(textarea_selector, timeout=10000)
            
            # 输入内容
            await self.page.fill(textarea_selector, content)
            await self.page.wait_for_timeout(1000)
            print("✅ 已输入微博内容")
            
            # 上传图片
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
                                if (el.className && typeof el.className === 'string' && 
                                    (el.className.includes('pic') || el.className.includes('photo') || el.className.includes('image'))) {
                                    el.click();
                                    break;
                                }
                            }
                        ''')
                        await self.page.wait_for_timeout(1000)
                        file_input = await self.page.query_selector('input[type="file"]._file_hqmwy_20')
                    
                    # 上传图片并等待完成
                    if file_input:
                        for idx, image_path in enumerate(image_paths):
                            if os.path.exists(image_path):
                                await file_input.set_input_files(image_path)
                                print(f"⏳ 正在上传图片 {idx+1}: {os.path.basename(image_path)}")
                                
                                # 等待上传完成（增加重试和超时）
                                for attempt in range(3):  # 最多重试3次
                                    try:
                                        # 等待上传进度条消失 - 使用更可靠的selector（根据微博页面调整）
                                        await self.page.wait_for_selector(
                                            f'div[class*="woo-progress"]:nth-child({idx+1})',  # 微博常见的进度条class
                                            state='detached',
                                            timeout=60000  # 60秒超时
                                        )
                                        print(f"✅ 图片 {idx+1} 上传完成")
                                        break
                                    except Exception as e:
                                        print(f"⚠️ 图片 {idx+1} 上传等待超时 (尝试 {attempt+1}): {e}")
                                        await self.page.wait_for_timeout(5000)  # 等待5秒后重试
                                else:
                                    print(f"❌ 图片 {idx+1} 上传失败，跳过")
                            else:
                                print(f"❌ 图片文件不存在: {image_path}")
                            
                        await self.page.wait_for_timeout(2000)  # 所有图片上传后的额外等待
                    else:
                        print("❌ 未找到文件输入框，无法上传图片")
                        
                except Exception as e:
                    print(f"❌ 上传图片时出错: {e}")
            
            # 点击发布按钮
            try:
                send_button_selector = 'button.woo-button-main.woo-button-flat.woo-button-primary'
                await self.page.wait_for_selector(send_button_selector, timeout=10000)
                await self.page.click(send_button_selector)
                
                # 动态等待发布成功
                try:
                    await self.page.wait_for_selector(
                        'div[class*="publish-success"]',  # 假设成功提示的selector，根据实际页面调整
                        timeout=60000
                    )
                    print("✅ 微博发布成功（确认提示出现）！")
                    return True
                except Exception as e:
                    print(f"❌ 发布等待超时: {e}")
                    return False
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
