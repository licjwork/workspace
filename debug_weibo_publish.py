#!/usr/bin/env python3
import asyncio
import sys
sys.path.append('/home/ubuntu/.openclaw/workspace/skills/weibo-publish-2/scripts')
from playwright_weibo_publisher_web_v2 import PlaywrightWeiboPublisher

async def debug_publish():
    print("🔍 开始调试网页版发布...")
    
    publisher = PlaywrightWeiboPublisher("调试测试")
    await publisher.init_browser()
    
    try:
        # 访问发布页面
        await publisher.page.goto('https://weibo.com/compose', wait_until='networkidle')
        await asyncio.sleep(3)
        
        # 检查页面内容
        content = await publisher.page.content()
        print("📄 页面标题:", await publisher.page.title())
        
        # 检查文本框
        textarea = await publisher.page.query_selector('textarea._input_13iqr_8')
        if textarea:
            print("✅ 找到文本框")
            await textarea.fill("这是一条调试测试微博")
        else:
            print("❌ 未找到文本框")
            
        # 检查发布按钮
        send_btn = await publisher.page.query_selector('button.woo-button-main.woo-button-flat.woo-button-primary')
        if send_btn:
            print("✅ 找到发布按钮")
        else:
            print("❌ 未找到发布按钮")
            
        # 检查是否有其他发布按钮
        all_buttons = await publisher.page.query_selector_all('button')
        print(f"📋 页面共有 {len(all_buttons)} 个按钮")
        
        # 检查是否有其他文本框
        all_textareas = await publisher.page.query_selector_all('textarea')
        print(f"📝 页面共有 {len(all_textareas)} 个文本框")
        
        # 等待用户确认
        print("\n⏸️ 暂停，请检查浏览器窗口...")
        await asyncio.sleep(10)
        
    except Exception as e:
        print(f"❌ 调试过程中出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await publisher.close()

if __name__ == "__main__":
    asyncio.run(debug_publish())
