#!/usr/bin/env python3
import asyncio
import sys
import os
import datetime
sys.path.append('/home/ubuntu/.openclaw/workspace/skills/weibo-publish-2/scripts')
from playwright_weibo_publisher import PlaywrightWeiboPublisher

async def test_full_publish():
    print("🚀 开始完整发布测试...")
    
    try:
        # 初始化发布器
        publisher = PlaywrightWeiboPublisher("测试完整发布流程")
        await publisher.init_browser()
        
        # 访问发布页面
        await publisher.page.goto('https://m.weibo.cn/compose')
        await asyncio.sleep(3)
        
        # 输入测试内容
        test_content = "这是一条测试微博，用于验证发布功能是否正常。时间：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        textarea = await publisher.page.query_selector('textarea')
        await textarea.fill(test_content)
        print("✅ 已输入测试内容")
        
        # 尝试发布
        publish_btn = await publisher.page.query_selector('a.m-send-btn')
        if publish_btn:
            await publish_btn.click()
            print("✅ 已点击发布按钮")
            
            # 等待发布完成
            await asyncio.sleep(5)
            
            # 检查是否还在发布页面
            current_url = publisher.page.url
            if 'compose' not in current_url:
                print("✅ 发布成功，已离开发布页面")
                return True
            else:
                print("❌ 仍在发布页面，可能发布失败")
                return False
        else:
            print("❌ 未找到发布按钮")
            return False
            
    except Exception as e:
        print(f"❌ 发布测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            await publisher.close()
        except:
            pass

if __name__ == "__main__":
    result = asyncio.run(test_full_publish())
    print(f"\n发布测试结果: {'✅ 成功' if result else '❌ 失败'}")
