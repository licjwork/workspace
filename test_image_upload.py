#!/usr/bin/env python3
import asyncio
import os
from playwright.async_api import async_playwright

async def test_image_upload():
    print("🚀 测试图片上传功能...")
    
    async with async_playwright() as p:
        user_data_dir = os.path.expanduser('~/.weibo-profile')
        
        # 启动浏览器
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        page = await browser.new_page()
        
        # 导航到微博发布页面
        print("🌐 导航到微博发布页面...")
        await page.goto('https://weibo.com/compose', wait_until='networkidle')
        await page.wait_for_timeout(5000)
        
        # 输入一些测试内容
        textarea_selector = 'textarea._input_13iqr_8'
        await page.wait_for_selector(textarea_selector, timeout=10000)
        await page.fill(textarea_selector, "测试图片上传功能")
        await page.wait_for_timeout(2000)
        
        # 尝试找到图片上传元素
        print("🔍 查找图片上传元素...")
        
        # 尝试不同的选择器
        selectors_to_try = [
            'input[type="file"]._file_hqmwy_20',
            '.m-font-pic',
            '[class*="pic"]',
            '[class*="photo"]',
            '[class*="image"]',
            'button[class*="pic"]',
            'div[class*="pic"]',
            'span[class*="pic"]'
        ]
        
        file_input = None
        for selector in selectors_to_try:
            try:
                element = await page.query_selector(selector)
                if element:
                    print(f"✅ 找到元素: {selector}")
                    if 'input[type="file"]' in selector:
                        file_input = element
                        break
                    else:
                        # 点击图标来触发文件输入框
                        await element.click()
                        await page.wait_for_timeout(2000)
                        file_input = await page.query_selector('input[type="file"]._file_hqmwy_20')
                        if file_input:
                            print(f"✅ 通过点击 {selector} 触发了文件输入框")
                            break
            except Exception as e:
                print(f"❌ 选择器 {selector} 失败: {e}")
                continue
        
        if file_input:
            print("✅ 找到文件输入框，准备上传图片...")
            # 测试上传一张图片
            image_path = "/home/ubuntu/.openclaw/workspace/uploads/火箭vs湖人_1.png"
            if os.path.exists(image_path):
                await file_input.set_input_files(image_path)
                await page.wait_for_timeout(3000)
                print("✅ 图片上传成功！")
            else:
                print(f"❌ 图片文件不存在: {image_path}")
        else:
            print("❌ 未找到文件输入框")
            
        print("\n💡 请手动检查浏览器窗口中的情况...")
        await page.wait_for_timeout(10000)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_image_upload())
