#!/usr/bin/env python3
"""
微博发布技能2 - Playwright版 (长期会话支持)
"""

import asyncio
import sys
import os

# 将当前目录添加到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("请提供话题参数")
        return False
    
    topic = sys.argv[1]
    persistent = '--persistent' in sys.argv
    
    # 动态导入
    from playwright_weibo_publisher import PlaywrightWeiboPublisher
    
    publisher = PlaywrightWeiboPublisher(topic, persistent_session=persistent)
    
    try:
        success = await publisher.run()
        return success
    finally:
        await publisher.cleanup()

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
