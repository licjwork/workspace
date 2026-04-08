#!/usr/bin/env python3
"""
Enhanced Weibo Publisher Demo - 增强版功能演示
"""

import sys
sys.path.append('/home/ubuntu/.openclaw/workspace/skills/weibo-publish/scripts')
from enhanced_trigger import EnhancedWeiboTrigger

def demo_enhanced_features():
    """演示增强版功能"""
    print("🚀 微博发布Skill增强版功能演示")
    print("=" * 60)
    
    trigger = EnhancedWeiboTrigger()
    
    print("\n📋 增强版功能特色:")
    print("1. 🔥 热搜来源：VNC浏览器实时抓取")
    print("2. 🎯 吸睛标题：博人眼球的标题设计")
    print("3. 📝 300字内容：高质量深度分析")
    print("4. 💡 深度理解：结合热搜和评论观点")
    
    print("\n🎯 触发关键词演示:")
    
    # 演示不同的触发词
    demo_messages = [
        {
            "message": "微博热搜",
            "type": "🔥 增强版热搜",
            "description": "使用VNC浏览器抓取真实热搜，生成300字深度分析"
        },
        {
            "message": "热搜榜",
            "type": "🔥 增强版热搜", 
            "description": "同上，触发增强版热搜发布"
        },
        {
            "message": "热门话题",
            "type": "🔥 增强版热搜",
            "description": "获取当前最热门的话题进行分析"
        },
        {
            "message": "我想发一条关于音乐的微博",
            "type": "🎵 音乐内容",
            "description": "发布音乐相关的深度内容"
        },
        {
            "message": "发布科技资讯",
            "type": "💡 科技内容",
            "description": "发布科技相关的分析内容"
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
    print("📚 增强版热搜内容示例:")
    print("🔥 爆！[热搜标题]... 网友炸锅了！")
    print("📰 深度解析今日热搜TOP3：")
    print("🎯 【榜首话题】[话题1]")
    print("💡 【热点关注】[话题2]") 
    print("🎭 【娱乐动态】[话题3]")
    print("🤔 深度分析和网友观点...")
    print("#微博热搜 #深度解析 #今日话题")
    
    print("\n💡 使用建议:")
    print("- 热搜内容最适合日常发布")
    print("- 300字深度分析提高内容质量")
    print("- 吸睛标题增加点击率")
    print("- 结合评论观点增强互动性")
    
    print("\n🎮 现在你可以试试这些触发词:")
    print("- '微博热搜' - 获取今日热搜TOP3")
    print("- '热搜榜' - 同上")
    print("- '热门话题' - 获取热门话题分析")

if __name__ == "__main__":
    demo_enhanced_features()
