#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试完整集成流程
"""

import sys
import os

# 添加技能路径
sys.path.append('/home/ubuntu/.openclaw/workspace/skills/weibo-publish-2/scripts')

from topic_research import TopicResearcher
from improved_content_generator import call_dogegg_ai

def test_full_integration(topic):
    """测试完整集成流程"""
    print(f"🚀 测试完整集成流程: {topic}")
    print("="*80)
    
    # 1. 研究话题
    print("\n1. 🔍 话题研究阶段")
    print("-" * 40)
    researcher = TopicResearcher()
    research_context = researcher.get_research_context(topic)
    
    print(f"📝 研究背景信息 (前200字): {research_context[:200]}...")
    print(f"📊 研究背景信息长度: {len(research_context)} 字符")
    
    # 2. 生成内容
    print("\n2. 🤖 AI内容生成阶段")
    print("-" * 40)
    result = call_dogegg_ai(topic, research_context)
    
    if result:
        print("✅ 生成成功!")
        print(f"📊 生成内容长度: {len(result)}")
        print("\n📄 完整生成内容:")
        print("-" * 40)
        print(result)
        print("-" * 40)
        return True
    else:
        print("❌ 生成失败!")
        return False

def main():
    """主测试函数"""
    if len(sys.argv) < 2:
        print("请提供测试话题作为参数")
        return
    
    topic = sys.argv[1]
    success = test_full_integration(topic)
    
    if success:
        print("\n🎉 完整集成测试成功!")
    else:
        print("\n❌ 完整集成测试失败!")

if __name__ == "__main__":
    main()
