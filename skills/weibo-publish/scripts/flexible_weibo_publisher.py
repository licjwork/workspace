#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from weibo_publisher import WeiboPublisher

class FlexibleWeiboPublisher:
    def __init__(self):
        self.publisher = WeiboPublisher()
        
    def generate_auto_content(self, topic):
        """自动生成热搜内容"""
        title = f"🔥 💥 热搜第一！{topic}引发全民热议"
        content = f"""
📰 实时热搜TOP1话题深度解析：

🎯 【焦点话题】{topic}

💡 【热点分析】
作为当前最受关注的社会话题，这一事件反映了公众对相关议题的高度关注。从传播学角度看，能够登上热搜第一说明其具有广泛的社会共鸣和讨论价值。

🤔 【深度思考】
这种现象背后体现了当代社会的信息传播特点和公众关注焦点。热点话题的形成往往与当前社会环境、民众心理和媒体传播机制密切相关。

💭 【个人观点】
每个热点话题都值得我们理性思考和深入讨论。建议大家在关注热点的同时，也要保持独立思考，形成自己的判断。

你怎么看这个话题？欢迎在评论区分享你的观点！#热点关注 #深度解析 #理性思考
"""
        return title, content
    
    def generate_custom_content(self, topic):
        """生成指定话题内容"""
        title = f"🔥 🎯 {topic}深度解析！网友都在讨论"
        content = f"""
📰 热门话题深度分析：

🎯 【话题核心】{topic}

💡 【内容解析】
这个话题之所以引发广泛关注，说明它具有很强的社会共鸣性。从话题本身来看，涉及到了公众普遍关心的重要议题。

🤔 【社会意义】
通过这个话题的讨论，我们可以看到社会对相关问题的关注程度和态度倾向。这种公众讨论有助于推动问题的解决和社会的进步。

💭 【思考建议】
面对热门话题，我们既要积极参与讨论，也要保持理性思考。建议从多个角度分析问题，形成客观全面的认识。

你怎么看待这个话题？期待听到你的声音！#热点话题 #深度分析 #社会观察
"""
        return title, content
    
    def publish_auto_hot_search(self):
        """自动发布热搜第一"""
        print("🎯 开始自动获取热搜第一发布...")
        
        # 使用现有的热搜获取逻辑
        try:
            # 这里可以集成现有的热搜获取功能
            # 暂时使用默认话题
            default_topic = "当前热门社会话题"
            title, content = self.generate_auto_content(default_topic)
            
            print(f"🔥 生成标题: {title}")
            print(f"📝 内容长度: {len(content)} 字")
            
            # 发布微博
            print("\n🚀 开始发布...")
            result = self.publisher.publish_weibo(content)
            
            if result:
                print(f"\n🎉 自动热搜发布成功！")
                print(f"🎯 话题: {default_topic}")
                print(f"📊 统计: {len(content)}字 | 自动选择 | 深度分析")
                return True
            else:
                print("\n❌ 发布失败")
                return False
        except Exception as e:
            print(f"❌ 自动发布失败: {e}")
            return False
    
    def publish_specific_topic(self, custom_topic):
        """发布指定话题"""
        print(f"🎯 开始发布指定话题: {custom_topic}")
        
        # 生成内容
        title, content = self.generate_custom_content(custom_topic)
        print(f"🔥 生成标题: {title}")
        print(f"📝 内容长度: {len(content)} 字")
        
        # 发布微博
        print("\n🚀 开始发布...")
        result = self.publisher.publish_weibo(content)
        
        if result:
            print(f"\n🎉 指定话题发布成功！")
            print(f"🎯 话题: {custom_topic}")
            print(f"📊 统计: {len(content)}字 | 指定话题 | 深度分析")
            return True
        else:
            print("\n❌ 发布失败")
            return False

def main():
    import sys
    
    if len(sys.argv) > 1:
        # 指定话题模式
        custom_topic = " ".join(sys.argv[1:])
        publisher = FlexibleWeiboPublisher()
        publisher.publish_specific_topic(custom_topic)
    else:
        # 自动热搜模式  
        publisher = FlexibleWeiboPublisher()
        publisher.publish_auto_hot_search()

if __name__ == "__main__":
    main()
