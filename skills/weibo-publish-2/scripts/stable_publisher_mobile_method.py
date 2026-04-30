#!/usr/bin/env python3
import os
import sys
import asyncio
from playwright.async_api import async_playwright
from improved_content_generator import call_dogegg_ai

class StableWeiboPublisherMobileMethod:
    def __init__(self, topic, persistent_session=True):
        self.topic = topic
        self.persistent_session = persistent_session
        self.user_data_dir = os.path.expanduser('~/.weibo-profile')
        self.browser = None
        self.page = None
        self.playwright = None
        self.image_paths = []
        
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

    async def generate_content(self):
        print("\n✍️ 正在生成微博内容...")
        
        content = call_dogegg_ai(self.topic, f"关于话题'{self.topic}'的讨论和相关信息")
        print(f"📝 内容生成完成，字数: {len(content)}")
        return content

    async def publish_weibo(self, content):
        print("\n🚀 正在发布微博...")
        
        try:
            await self.page.goto('https://weibo.com/', wait_until='networkidle')
            await self.page.wait_for_timeout(30000)
            
            textarea_selector = 'textarea._input_13iqr_8'
            await self.page.wait_for_selector(textarea_selector, timeout=10000)
            
            await self.page.fill(textarea_selector, content)
            await self.page.wait_for_timeout(10000)
            
            # 上传图片（借鉴移动端方法）
            if self.image_paths:
                print(f"📸 正在上传 {len(self.image_paths)} 张图片...")
                
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
                                    await self.page.wait_for_timeout(10000)
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
                        await self.page.wait_for_timeout(10000)
                        file_input = await self.page.query_selector('input[type="file"]._file_hqmwy_20')
                    
                    # 上传文件
                    if file_input:
                        await file_input.set_input_files(self.image_paths)
                        await self.page.wait_for_timeout(15000)  # 等待图片上传
                        print("✅ 图片上传成功")
                    else:
                        # 最后尝试直接使用set_input_files
                        await self.page.set_input_files('input[type="file"]._file_hqmwy_20', self.image_paths)
                        await self.page.wait_for_timeout(15000)
                        print("✅ 使用直接方法上传成功")
                        
                except Exception as e:
                    print(f"❌ 图片上传失败: {e}")
            
            send_button_selector = 'button.woo-button-main.woo-button-flat.woo-button-primary'
            await self.page.wait_for_selector(send_button_selector, timeout=10000)
            await self.page.click(send_button_selector)
            
            await self.page.wait_for_timeout(30000)
            
            print("✅ 微博发布成功！")
            return True
            
        except Exception as e:
            print(f"❌ 发布失败: {e}")
            return False

    async def run(self):
        try:
            await self.init_browser()
            
            if not await self.check_login_status():
                print("❌ 需要登录，请先运行登录助手")
                return False
            
            content = await self.generate_content()
            if not content:
                print("❌ 内容生成失败")
                return False
            
            success = await self.publish_weibo(content)
            return success
            
        except Exception as e:
            print(f"❌ 运行失败: {e}")
            return False
        finally:
            await self.cleanup()

    async def cleanup(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("🧹 资源清理完成")

async def main():
    if len(sys.argv) < 2:
        print("请提供话题参数")
        sys.exit(1)
    
    topic = sys.argv[1]
    
    # 解析图片路径参数
    image_paths = []
    for arg in sys.argv[2:]:
        if arg.startswith('--images='):
            paths = arg.replace('--images=', '').split(',')
            image_paths.extend([path.strip() for path in paths if path.strip()])
    
    publisher = StableWeiboPublisherMobileMethod(topic, persistent_session=True)
    publisher.image_paths = image_paths
    
    try:
        success = await publisher.run()
        return success
    finally:
        await publisher.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
