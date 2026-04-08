#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from weibo_publisher import WeiboPublisher
from content_validator import validate_content, preview_content
from duplicate_checker import DuplicateChecker
from smart_content_generator import SmartContentGenerator

class SmartWeiboPublisher:
    def __init__(self):
        self.publisher = WeiboPublisher()
        self.duplicate_checker = DuplicateChecker()
        self.content_generator = SmartContentGenerator()
        
    def publish_auto_hot_search(self):
        """智能分析并发布热搜第一"""
        print("🎯 开始智能分析实时热搜...")
        
        # 生成基于真实热搜分析的内容
        content, status = self.content_generator.generate_real_hot_search_content()
        
        if not content:
            print(f"❌ 内容生成失败: {status}")
            return False
        
        print(f"\n📊 内容生成状态: {status}")
        
        # 提取话题用于重复检测
        topic = self._extract_topic_from_content(content)
        
        # 重复检查
        print("\n🔍 正在检查是否重复...")
        is_duplicate, similar_topic = self.duplicate_checker.is_duplicate(topic, content)
        if is_duplicate:
            print(f"❌ 检测到重复内容！相似话题: {similar_topic}")
            print("🚫 为避免重复发布，本次操作已取消")
            return False
        
        # 内容验证
        print("\n🔍 正在验证内容...")
        validation_result = validate_content(content, topic)
        
        if not validation_result['is_valid']:
            print("❌ 内容验证失败:")
            for error in validation_result['errors']:
                print(f"   • {error}")
            return False
        
        # 显示警告
        if validation_result['warnings']:
            print("⚠️  内容警告:")
            for warning in validation_result['warnings']:
                print(f"   • {warning}")
        
        # 内容预览
        preview_content(content, topic)
        
        # 确认发布
        print("\n🚀 开始发布...")
        result = self.publisher.publish_weibo(content)
        
        if result:
            # 记录发布历史
            self.duplicate_checker.record_publish(topic, content)
            
            print(f"\n🎉 智能热搜发布成功！")
            print(f"🎯 话题: {topic}")
            print(f"📊 统计: {len(content)}字 | 智能分析 | 实时数据")
            print(f"📈 来源: {status}")
            return True
        else:
            print("\n❌ 发布失败")
            return False
    
    def publish_specific_topic(self, custom_topic):
        """智能分析并发布指定话题"""
        print(f"🎯 开始智能分析指定话题: {custom_topic}")
        
        # 生成基于热搜参考的内容
        content, status = self.content_generator.generate_real_hot_search_content(custom_topic)
        
        if not content:
            print(f"❌ 内容生成失败: {status}")
            return False
        
        print(f"\n📊 内容生成状态: {status}")
        
        # 重复检查
        print("\n🔍 正在检查是否重复...")
        is_duplicate, similar_topic = self.duplicate_checker.is_duplicate(custom_topic, content)
        if is_duplicate:
            print(f"❌ 检测到重复内容！相似话题: {similar_topic}")
            print("🚫 为避免重复发布，本次操作已取消")
            return False
        
        # 内容验证
        print("\n🔍 正在验证内容...")
        validation_result = validate_content(content, custom_topic)
        
        if not validation_result['is_valid']:
            print("❌ 内容验证失败:")
            for error in validation_result['errors']:
                print(f"   • {error}")
            return False
        
        # 显示警告
        if validation_result['warnings']:
            print("⚠️  内容警告:")
            for warning in validation_result['warnings']:
                print(f"   • {warning}")
        
        # 内容预览
        preview_content(content, custom_topic)
        
        # 确认发布
        print("\n🚀 开始发布...")
        result = self.publisher.publish_weibo(content)
        
        if result:
            # 记录发布历史
            self.duplicate_checker.record_publish(custom_topic, content)
            
            print(f"\n🎉 智能话题发布成功！")
            print(f"🎯 话题: {custom_topic}")
            print(f"📊 统计: {len(content)}字 | 智能分析 | 热搜参考")
            print(f"📈 来源: {status}")
            return True
        else:
            print("\n❌ 发布失败")
            return False
    
    def _extract_topic_from_content(self, content):
        """从内容中提取话题"""
        # 简单的提取逻辑，取第一行的关键部分
        lines = content.split('\n')
        if lines:
            first_line = lines[0]
            # 移除表情符号和标点
            clean_line = first_line.replace('🔥', '').replace('！', '').replace('?', '').strip()
            return clean_line[:20]  # 取前20个字符作为话题
        return "未知话题"

def main():
    import sys
    
    if len(sys.argv) > 1:
        # 指定话题模式
        custom_topic = " ".join(sys.argv[1:])
        publisher = SmartWeiboPublisher()
        publisher.publish_specific_topic(custom_topic)
    else:
        # 自动热搜模式  
        publisher = SmartWeiboPublisher()
        publisher.publish_auto_hot_search()

if __name__ == "__main__":
    main()
