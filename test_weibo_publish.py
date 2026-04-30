#!/usr/bin/env python3
import asyncio
import sys
import os
sys.path.append('/home/ubuntu/.openclaw/workspace/skills/weibo-publish-2/scripts')
from playwright_weibo_publisher import PlaywrightWeiboPublisher

async def test_weibo_publish():
    print("🚀 开始微博发布测试...")
    
    try:
        # 初始化发布器
        publisher = PlaywrightWeiboPublisher("测试微博发布功能")
        print("✅ 发布器初始化完成")
        
        # 初始化浏览器
        await publisher.init_browser()
        print("✅ 浏览器初始化完成")
        
        # 检查登录状态
        await publisher.page.goto('https://m.weibo.cn')
        print("✅ 已访问微博首页")
        
        # 检查登录状态
        try:
            login_elements = await publisher.page.query_selector_all('.login-btn, .login, [data-login], .btn-login')
            if login_elements:
                print("❌ 检测到登录按钮，需要登录")
                return False
            else:
                print("✅ 已登录状态")
        except Exception as e:
            print(f"⚠️ 检查登录状态时出错: {e}")
        
        # 访问发布页面
        await publisher.page.goto('https://m.weibo.cn/compose')
        print("✅ 已访问发布页面")
        
        # 等待发布页面加载
        await asyncio.sleep(3)
        
        # 检查发布页面元素
        textarea = await publisher.page.query_selector('textarea')
        if textarea:
            print("✅ 找到文本输入框")
        else:
            print("❌ 未找到文本输入框")
            
        # 检查发布按钮
        publish_btn = await publisher.page.query_selector('a.m-send-btn, button.send-btn')
        if publish_btn:
            print("✅ 找到发布按钮")
        else:
            print("❌ 未找到发布按钮")
            
        print("\n🔍 页面源码片段:")
        content = await publisher.page.content()
        print(content[:1000] + "..." if len(content) > 1000 else content)
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            await publisher.close()
        except:
            pass

if __name__ == "__main__":
    result = asyncio.run(test_weibo_publish())
    print(f"\n测试结果: {'✅ 成功' if result else '❌ 失败'}")
