#!/usr/bin/env python3
import asyncio
import sys
sys.path.append('/home/ubuntu/.openclaw/workspace/skills/weibo-publish-2/scripts')
from single_image_publisher import SingleImageWeiboPublisher

async def debug_image_upload():
    print("🔍 调试图片上传...")
    
    publisher = SingleImageWeiboPublisher("调试")
    await publisher.init_browser()
    
    try:
        # 访问发布页面
        await publisher.page.goto('https://m.weibo.cn/compose', wait_until='networkidle')
        await asyncio.sleep(3)
        
        print("📄 页面标题:", await publisher.page.title())
        
        # 检查所有可能的图片上传元素
        selectors = [
            '.m-font-pic',
            '[class*="pic"]',
            '[class*="photo"]',
            '[class*="image"]',
            'button[class*="pic"]',
            'div[class*="pic"]',
            'span[class*="pic"]',
            'i[class*="pic"]',
            '.m-icon-pic',
            '.icon-pic',
            '.photo-icon',
            '.image-icon'
        ]
        
        for selector in selectors:
            elements = await publisher.page.query_selector_all(selector)
            if elements:
                print(f"✅ 找到选择器 {selector}: {len(elements)} 个元素")
                for i, el in enumerate(elements):
                    try:
                        class_name = await el.get_attribute('class')
                        print(f"  元素{i+1} class: {class_name}")
                    except:
                        pass
            else:
                print(f"❌ 未找到选择器 {selector}")
        
        # 检查所有按钮
        all_buttons = await publisher.page.query_selector_all('button, a, div, span, i')
        print(f"\n📋 页面共有 {len(all_buttons)} 个可点击元素")
        
        # 等待用户检查
        print("\n⏸️ 暂停，请检查浏览器窗口...")
        await asyncio.sleep(15)
        
    except Exception as e:
        print(f"❌ 调试过程中出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await publisher.close()

if __name__ == "__main__":
    asyncio.run(debug_image_upload())
