#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博全自动发布工具 (全技能整合版) - 修复版
集成：热搜搜图技能 + AI内容生成技能 + 图片上传发布技能
使用网页版发布逻辑
"""

import asyncio
import os
import sys
from pathlib import Path
import argparse

# 动态添加路径以确保可以导入各个技能模块
WORKSPACE_ROOT = Path('/home/ubuntu/.openclaw/workspace')
sys.path.append(str(WORKSPACE_ROOT / 'skills/weibo-hot-search-images/scripts'))
sys.path.append(str(WORKSPACE_ROOT / 'skills/weibo-image-upload/scripts'))
sys.path.append(str(WORKSPACE_ROOT / 'skills/weibo-publish-2/scripts'))

# 导入各个独立技能
try:
    from weibo_image_fetcher import WeiboImageFetcher
    from playwright_weibo_publisher import PlaywrightWeiboPublisher
    from improved_content_generator import call_dogegg_ai
    print("✅ 所有技能模块导入成功")
except ImportError as e:
    print(f"❌ 技能模块导入失败: {e}")
    # 提供降级兜底（如果模块不存在）
    class WeiboImageFetcher: 
        def __init__(self, **kwargs): pass
        async def search_topic_images(self, topic, **kwargs): return []
    class PlaywrightWeiboPublisher:
        def __init__(self, topic, **kwargs): pass
        async def init_browser(self): pass
        async def check_login_status(self): return True
        async def publish_weibo(self, content, image_paths=None): pass
        async def close(self): pass
    def call_dogegg_ai(topic, context): return f"关于#{topic}#的内容"

class UnifiedWeiboSkillOrchestrator:
    def __init__(self):
        # 统一路径：按照用户要求设置
        self.uploads_dir = Path('/home/ubuntu/.openclaw/workspace/uploads')
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化各个技能实例
        self.fetcher = WeiboImageFetcher(uploads_dir=str(self.uploads_dir))
        
    async def run_full_workflow(self, topic, images_count=3, publish=False):
        print(f"\n🌟 开始执行全技能整合工作流: {topic}")
        print("-" * 40)
        
        try:
            # 1. 执行【热搜图片获取技能】
            print("Step 1: 正在运行图片获取技能...")
            image_paths = await self.fetcher.search_topic_images(topic, max_images=images_count)
            
            if image_paths:
                print(f"✅ 图片获取成功，共 {len(image_paths)} 张")
                for i, path in enumerate(image_paths):
                    print(f"  📐 图片{i+1}: {path}")
            else:
                print("⚠️ 未获取到图片，将继续发布纯文本微博")
            
            # 2. 执行【AI内容生成技能】
            print("\nStep 2: 正在运行 AI 内容生成技能...")
            
            # 准备上下文信息
            context = {
                'topic': topic,
                'has_images': len(image_paths) > 0,
                'image_count': len(image_paths),
                'current_time': __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            content = call_dogegg_ai(topic, context)
            print(f"✅ AI内容生成成功，字数: {len(content)}")
            
            # 3. 执行【图片上传与发布技能】
            print("\nStep 3: 正在运行图片上传与发布技能 (网页版)...")
            
            publisher = PlaywrightWeiboPublisher(topic)
            await publisher.init_browser()
            
            if not await publisher.check_login_status():
                print("❌ 微博未登录，请先运行登录流程")
            else:
                if publish:
                    await publisher.publish_weibo(content, image_paths)
                else:
                    print("⚠️ publish 参数未设置，当前流程为：仅生成和获取图片，不执行点击发布")
                    
        except Exception as e:
            print(f"❌ 发布过程中发生错误: {e}")
            import traceback
            traceback.print_exc()
        finally:
            try:
                await publisher.close()
            except:
                pass
        
        print("-" * 40)
        print("🏁 全技能整合工作流执行完毕！")

async def main():
    parser = argparse.ArgumentParser(description='微博全自动发布工具 (全技能整合版) - 修复版')
    parser.add_argument('--topic', type=str, required=True, help='微博话题')
    parser.add_argument('--images', type=int, default=3, help='配图数量')
    parser.add_argument('--publish', action='store_true', help='是否直接发布')
    
    args = parser.parse_args()
    
    orchestrator = UnifiedWeiboSkillOrchestrator()
    await orchestrator.run_full_workflow(
        topic=args.topic,
        images_count=args.images,
        publish=args.publish
    )

if __name__ == "__main__":
    asyncio.run(main())
