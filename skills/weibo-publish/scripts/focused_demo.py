#!/usr/bin/env python3
"""
Focused Weibo Publisher Demo - 专注单个话题功能演示
"""

import sys
sys.path.append('/home/ubuntu/.openclaw/workspace/skills/weibo-publish/scripts')
from focused_trigger import FocusedWeiboTrigger

def demo_focused_features():
    """演示专注单个话题功能"""
    print("🎯 微博发布Skill专注单个话题功能演示")
    print("=" * 60)
    
    trigger = FocusedWeiboTrigger()
    
    print("\n📋 专注单个话题功能特色:")
    print("1. 🎯 单一焦点：只分析一个热搜话题")
    print("2. 🔥 吸睛标题：博人眼球的标题设计")
    print("3. 📝 300字深度：针对单个话题的深入分析")
    print("4. 💡 独特视角：结合传播学和社会学分析")
    print("5. 📊 真实数据：VNC浏览器实时抓取热搜")
    
    print("\n🎯 内容生成策略:")
    print("- 民生争议类：深度分析社会意义")
    print("- 娱乐话题类：产业视角和文化思考") 
    print("- 科技话题类：产业影响和未来思考")
    print("- 通用话题类：传播规律和社会观察")
    
    print("\n🎯 触发关键词演示:")
    
    # 演示不同的触发词
    demo_messages = [
        {
            "message": "微博热搜",
            "type": "🎯 专注单个话题",
            "description": "选择一个热搜话题进行300字深度分析"
        },
        {
            "message": "热搜榜",
            "type": "🎯 专注单个话题", 
            "description": "从热搜榜选择焦点话题进行专注分析"
        },
        {
            "message": "单个热搜",
            "type": "🎯 专注单个话题",
            "description": "明确指定分析单个热搜话题"
        },
        {
            "message": "专注话题",
            "type": "🎯 专注单个话题",
            "description": "专注分析某个特定话题"
        },
        {
            "message": "深度分析",
            "type": "🎯 专注单个话题",
            "description": "进行深度的话题分析"
        }
    ]
    
    for i, demo in enumerate(demo_messages, 1):
        print(f"\n{i}. 触发词: '{demo['message']}'")
        print(f"   类型: {demo['type']}")
        print(f"   描述: {demo['description']}")
        
        # 检测关键词
        triggered = trigger.detect_keywords(demo['message'])
        if triggered:
            keywords = [kw for kw, _ in triggered]
            print(f"   ✅ 检测到: {keywords}")
        else:
            print("   ❌ 未检测到关键词")
    
    print("\n" + "=" * 60)
    print("📚 专注单个话题内容示例:")
    print("🔥 爆！[单个热搜话题]... 网友彻底炸锅了！")
    print()
    print("📰 [日期]最受关注话题深度解析：")
    print()
    print("🎯 【事件核心】[具体话题]")
    print()
    print("💡 【深度分析】")
    print("从传播学角度看，此类话题具有天然的'共情效应'...")
    print()
    print("🤔 【社会意义】")
    print("这种网络舆论监督的积极效应值得肯定...")
    print()
    print("你怎么看这个事件的处理方式？#深度解析 #理性讨论")
    
    print("\n💡 与之前版本的区别:")
    print("❌ 旧版：分析TOP3热搜话题，内容分散")
    print("✅ 新版：专注单个话题，深度分析")
    print("📈 优势：内容更聚焦，分析更深入，观点更明确")
    
    print("\n🎮 现在你可以试试这些触发词:")
    print("- '微博热搜' - 选择今日最热门话题进行深度分析")
    print("- '热搜榜' - 从热搜榜选择焦点话题")
    print("- '单个热搜' - 明确指定分析单个话题")
    print("- '专注话题' - 进行专注的话题分析")
    print("- '深度分析' - 生成深度分析内容")

if __name__ == "__main__":
    demo_focused_features()
