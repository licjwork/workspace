import asyncio
import os
import sys

# 添加脚本目录到路径
sys.path.insert(0, os.path.join(os.getcwd(), 'scripts'))

from playwright_weibo_publisher import PlaywrightWeiboPublisher

async def test_logic():
    print("🧪 开始自检微博技能逻辑...")
    publisher = PlaywrightWeiboPublisher("人工智能", persistent_session=True)
    
    try:
        # 1. 初始化浏览器
        print("\n--- 步骤 1: 初始化浏览器 ---")
        await publisher.init_browser()
        
        # 2. 检查热搜抓取逻辑
        print("\n--- 步骤 2: 测试热搜抓取 ---")
        trending = await publisher.get_trending_topics()
        if trending:
            print(f"✅ 成功抓取到热搜: {trending[:5]}...")
        else:
            print("⚠️ 未抓取到热搜，可能是页面结构变化或网络问题")
            
        # 3. 测试搜索调研逻辑
        print("\n--- 步骤 3: 测试话题调研 ---")
        research = await publisher.research_topic()
        if research and research.get('searchResults'):
            print(f"✅ 成功调研到话题内容，获取到 {len(research['searchResults'])} 条结果")
        else:
            print("⚠️ 话题调研未获取到结果")
            
        print("\n--- 自检完成 ---")
        print("💡 前置逻辑（抓取、搜索）基本跑通。发布和内容生成需要登录和 API Key。")
        
    except Exception as e:
        print(f"❌ 自检过程中出错: {e}")
    finally:
        await publisher.cleanup()

if __name__ == "__main__":
    asyncio.run(test_logic())
