#!/usr/bin/env python3
"""
Weibo Publisher Trigger Demo - 关键词触发功能演示
"""

import sys
sys.path.append('/home/ubuntu/.openclaw/workspace/skills/weibo-publish/scripts')

from weibo_trigger import WeiboTrigger
import time

def demo_keyword_triggers():
    """演示关键词触发功能"""
    print("🎯 微博发布关键词触发演示")
    print("=" * 60)
    
    trigger = WeiboTrigger()
    
    # 演示不同的关键词触发
    demo_messages = [
        {
            "message": "我想发一条关于音乐的微博",
            "expected_type": "音乐内容",
            "description": "触发音乐相关内容发布"
        },
        {
            "message": "发布一条科技资讯",
            "expected_type": "科技内容", 
            "description": "触发科技相关内容发布"
        },
        {
            "message": "来一条时尚潮流内容",
            "expected_type": "时尚内容",
            "description": "触发时尚相关内容发布"
        },
        {
            "message": "分享一些美食",
            "expected_type": "生活内容",
            "description": "触发生活相关内容发布"
        },
        {
            "message": "发一条热门话题",
            "expected_type": "热点内容",
            "description": "触发热点相关内容发布"
        },
        {
            "message": "测试一下微博功能",
            "expected_type": "测试内容",
            "description": "触发测试内容发布"
        }
    ]
    
    print("\n📋 演示列表:")
    for i, demo in enumerate(demo_messages, 1):
        print(f"{i}. {demo['message']} -> {demo['expected_type']}")
    
    print("\n🚀 开始演示...")
    
    for i, demo in enumerate(demo_messages, 1):
        print(f"\n--- 演示 {i}/{len(demo_messages)} ---")
        print(f"消息: {demo['message']}")
        print(f"预期: {demo['expected_type']}")
        print(f"描述: {demo['description']}")
        
        # 检测关键词
        triggered = trigger.detect_keywords(demo['message'])
        if triggered:
            keywords = [kw for kw, _ in triggered]
            print(f"✅ 检测到关键词: {', '.join(keywords)}")
            
            # 模拟发布（不实际发布，仅演示）
            print(f"📝 将发布: {demo['expected_type']}")
            print("⏳ 模拟发布中...")
            time.sleep(1)
            print("✅ 发布完成（演示模式）")
        else:
            print("❌ 未检测到触发关键词")
            
        time.sleep(1)  # 演示间隔
    
    print("\n" + "=" * 60)
    print("🎉 关键词触发演示完成！")
    print("\n📚 支持的关键词类型:")
    print(trigger.get_help_text())
    
    print("\n💡 实际使用示例:")
    print("# 在对话中发送以下任意消息即可触发微博发布:")
    print("- '我想发一条关于音乐的微博'")
    print("- '发布科技资讯'")
    print("- '来点时尚内容'")
    print("- '分享美食'")
    print("- '发微博'")
    print("- '测试功能'")
    
    print("\n🔧 自定义配置:")
    print("编辑 scripts/weibo_trigger.py 中的 keywords 字典来添加新的触发词")

def demo_real_publish():
    """演示实际发布功能"""
    print("\n🎯 实际发布演示")
    print("=" * 40)
    
    trigger = WeiboTrigger()
    
    # 询问用户是否要实际发布
    print("\n⚠️  注意: 以下操作将实际发布微博")
    print("是否要继续？(y/N): ", end="")
    
    # 为了安全，这里只是演示，不实际执行
    print("\n🔒 安全模式: 演示仅显示将要执行的操作，不实际发布")
    
    test_message = "测试微博发布功能"
    print(f"\n模拟处理消息: '{test_message}'")
    
    triggered = trigger.detect_keywords(test_message)
    if triggered:
        print("✅ 检测到触发词: 测试")
        print("📝 将发布测试内容")
        print("🔄 调用 publish_test_content() 方法")
        print("📤 实际发布需要取消演示模式的限制")
    
    print("\n✅ 演示完成！要实际使用，请直接调用 trigger.process_message() 方法")

if __name__ == "__main__":
    print("选择演示模式:")
    print("1. 关键词触发演示（推荐）")
    print("2. 实际发布演示")
    print("3. 完整演示")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == "1":
        demo_keyword_triggers()
    elif choice == "2":
        demo_real_publish()
    elif choice == "3":
        demo_keyword_triggers()
        demo_real_publish()
    else:
        print("❌ 无效选择，运行完整演示")
        demo_keyword_triggers()
        demo_real_publish()
