#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright

async def debug_weibo_page():
    print("🔍 调试微博发布页面...")
    
    async with async_playwright() as p:
        user_data_dir = os.path.expanduser('~/.weibo-profile')
        
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        page = await browser.new_page()
        
        # 导航到移动端发布页面
        print("🌐 导航到 m.weibo.cn/compose...")
        await page.goto('https://m.weibo.cn/compose', wait_until='networkidle')
        await page.wait_for_timeout(3000)
        
        # 检查当前URL
        current_url = page.url
        print(f"📋 当前URL: {current_url}")
        
        # 检查页面标题
        title = await page.title()
        print(f"📋 页面标题: {title}")
        
        # 检查是否有PC版元素
        pc_elements = await page.query_selector_all('button.woo-button-main.woo-button-flat.woo-button-primary')
        print(f"📋 PC版发布按钮数量: {len(pc_elements)}")
        
        # 检查是否有移动端元素
        mobile_elements = await page.query_selector_all('a.m-send-btn')
        print(f"📋 移动端发布按钮数量: {len(mobile_elements)}")
        
        print("\n💡 请查看浏览器窗口中的页面样式...")
        await page.wait_for_timeout(10000)
        
        await browser.close()

if __name__ == "__main__":
    import os
    asyncio.run(debug_weibo_page())
