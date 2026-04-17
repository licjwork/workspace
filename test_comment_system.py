#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博评论系统测试
"""

import os
import sys
import time

# 添加项目路径
sys.path.append('/home/ubuntu/.openclaw/workspace/skills/weibo-comment-reply/scripts')

from comment_replier import CommentAnalyzer, ReplyGenerator, WeiboCommentReplier

def test_comment_system():
    """测试评论系统核心功能"""
    print("🐕 微博评论智能回复系统测试")
    print("=" * 50)
    
    # 测试评论分析器
    analyzer = CommentAnalyzer()
    
    test_comments = [
        {
            'content': '这个新闻很有价值，市场监管越来越严格了！',
            'username': '财经观察者'
        },
        {
            'content': '35亿罚款太少了，应该罚更多！',
            'username': '正义网友'
        },
        {
            'content': '加微信123456，有内部消息！',
            'username': '广告机器人'
        },
        {
            'content': '请问这些罚款会怎么用？',
            'username': '好奇市民'
        }
    ]
    
    print("\n📊 评论质量分析:")
    for comment in test_comments:
        score = analyzer.analyze_comment(comment)
        quality = "✅ 高质量" if score >= 0.6 else "❌ 低质量"
        print(f"- {comment['content'][:30]}... | 分数: {score:.2f} | {quality}")
    
    # 测试回复生成器
    generator = ReplyGenerator()
    
    print("\n💬 智能回复生成:")
    for comment in test_comments[:3]:  # 只测试前3个
        if '好' in comment['content'] or '价值' in comment['content']:
            sentiment = 'positive'
        elif '?' in comment['content'] or '？' in comment['content']:
            sentiment = 'question'
        elif '少' in comment['content'] or '应该' in comment['content']:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        reply = generator.generate_reply(comment, sentiment)
        print(f"原评论: {comment['content'][:30]}...")
        print(f"生成回复: {reply}")
        print("-" * 40)
    
    print("\n✅ 核心功能测试完成！")
    print("\n📋 实际使用建议:")
    print("1. 需要具体的微博详情页面URL")
    print("2. 确保微博账号已登录")
    print("3. 建议先用--preview模式测试")
    print("4. 可以设置--daemon模式持续监控")

if __name__ == '__main__':
    test_comment_system()
