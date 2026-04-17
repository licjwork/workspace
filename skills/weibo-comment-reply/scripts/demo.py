#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博评论回复技能演示
"""

import os
import sys
import time

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from comment_replier import CommentAnalyzer, ReplyGenerator

def demo_comment_analysis():
    """演示评论分析功能"""
    print("\n=== 评论分析演示 ===")
    
    analyzer = CommentAnalyzer()
    
    test_comments = [
        {
            'content': '这个内容真的很棒，我非常喜欢！',
            'username': '真实用户1'
        },
        {
            'content': '加微信123456，有优惠！',
            'username': '疑似机器人1'
        },
        {
            'content': '很好很好很好很好很好',
            'username': '疑似机器人2'
        },
        {
            'content': '请问这个功能什么时候上线？',
            'username': '真实用户2'
        }
    ]
    
    for comment in test_comments:
        score = analyzer.analyze_comment(comment)
        print(f"评论: {comment['content'][:30]}...")
        print(f"用户名: {comment['username']}")
        print(f"质量分数: {score:.2f}")
        print(f"判断: {'✅ 真人评论' if score >= 0.6 else '❌ 疑似机器人'}")
        print("-" * 50)

def demo_reply_generation():
    """演示回复生成功能"""
    print("\n=== 回复生成演示 ===")
    
    generator = ReplyGenerator()
    
    test_comments = [
        {
            'content': '这个内容真的很棒，我非常喜欢！',
            'username': '真实用户1'
        },
        {
            'content': '请问这个功能什么时候上线？',
            'username': '真实用户2'
        },
        {
            'content': '体验很差，希望能改进',
            'username': '真实用户3'
        }
    ]
    
    for comment in test_comments:
        # 简单情感分析
        content = comment['content']
        if any(word in content for word in ['好', '棒', '喜欢', '不错']):
            sentiment = 'positive'
        elif any(word in content for word in ['差', '烂', '失望']):
            sentiment = 'negative'
        elif '?' in content or '？' in content:
            sentiment = 'question'
        else:
            sentiment = 'neutral'
        
        reply = generator.generate_reply(comment, sentiment)
        print(f"原评论: {comment['content']}")
        print(f"情感倾向: {sentiment}")
        print(f"生成回复: {reply}")
        print("-" * 50)

def main():
    print("🐕 微博评论智能回复技能演示")
    print("=" * 60)
    
    print("\n🎯 技能功能:")
    print("✅ 智能识别非机器人评论")
    print("✅ 定时自动回复")
    print("✅ 高质量回复生成")
    print("✅ 个性化定制回复")
    
    demo_comment_analysis()
    demo_reply_generation()
    
    print("\n📋 使用说明:")
    print("1. 确保VNC和浏览器服务正常运行")
    print("2. 配置目标微博URL")
    print("3. 运行命令: python3 scripts/comment_replier.py --preview")
    print("4. 预览模式确认无误后，去掉--preview参数正式运行")
    print("5. 可添加--daemon参数进入守护进程模式")
    
    print("\n⚙️  配置参数:")
    print("- check_interval: 检查间隔（秒）")
    print("- max_replies_per_session: 单次最大回复数")
    print("- min_comment_quality: 最低评论质量分数")
    print("- quiet_hours: 安静时段设置")
    print("- blacklist_keywords: 黑名单关键词")
    
    print("\n🎉 演示完成！技能已准备就绪")

if __name__ == '__main__':
    main()
