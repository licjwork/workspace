#!/usr/bin/env python3
import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    print("🚀 正在启动专门的登录浏览器...")
    print("💡 请在弹出的浏览器窗口中完成微博登录。")
    print("💡 登录成功后，您可以直接关闭浏览器窗口，登录状态会自动保存到 ~/.weibo-profile 中。")
    
    async with async_playwright() as p:
        user_data_dir = os.path.expanduser('~/.weibo-profile')
        
        # 启动持久化上下文，非静默模式
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        
        # 获取第一个页面或新建页面
        if browser.pages:
            page = browser.pages[0]
        else:
            page = await browser.new_page()
            
        print("🌐 正在打开网页版微博...")
        await page.goto('https://weibo.com', wait_until='domcontentloaded')
        
        print("\n⏳ 浏览器将保持打开状态，请随时进行登录操作...")
        print("⌨️  (或者在终端按 Ctrl+C 退出脚本)")
        
        # 保持浏览器打开，直到用户手动关闭窗口
        try:
            while len(browser.pages) > 0:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
        except KeyboardInterrupt:
            pass
            
        print("\n✅ 浏览器已关闭，环境退出。")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 已退出")
