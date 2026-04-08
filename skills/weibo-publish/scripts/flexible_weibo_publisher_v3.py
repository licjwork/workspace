#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from weibo_publisher import WeiboPublisher
from content_validator import validate_content, preview_content

def generate_simple_content(topic, is_auto=False):
    """生成通俗易懂的微博内容"""
    
    if is_auto:
        # 自动热搜模式
        content = f"""
🔥 热搜第一！{topic}这个话题最近真的火了！

说实话，看到这个话题我第一反应是：这不是很正常吗？现在谁还敢随便用外面的东西啊！

记得上次住酒店，那个毛巾看起来就旧旧的，谁知道之前有多少人用过。现在出门我都自带毛巾、拖鞋，甚至床单都自己带。这不是矫情，是基本的自我保护好吧！

其实说白了，就是现在的酒店服务让人不放心。你说你开酒店的，连最基本的毛巾都搞不好，还指望客人相信你其他服务？

建议酒店老板们多想想，客人愿意花钱住店，不就是图个干净舒适吗？把这些基础服务做好了，比打多少广告都强！

大家出门都带什么必备物品？分享一下经验呗！#酒店生活 #出门必备 #消费观察
"""
    else:
        # 指定话题模式  
        content = f"""
🔥 {topic}这个选择真的值得吗？

说实话，看到这个新闻我第一反应是：这些人是不是太冲动了？花这么多钱买个这么低工资的工作，真的划算吗？

但是转念一想，可能每个人都有不同的处境和考虑吧。也许对有些人来说，稳定的工作比高薪更重要？

不过我还是觉得，同样的投入去做点别的什么，回报可能都会更高一些。毕竟现在这个时代，机会到处都是。

你们怎么看这种选择？欢迎分享你的观点！#职场观察 #就业选择 #生活决策
"""
    
    return content.strip()

class FlexibleWeiboPublisherV3:
    def __init__(self):
        self.publisher = WeiboPublisher()
        
    def publish_auto_hot_search(self):
        """自动发布热搜第一"""
        print("🎯 开始自动获取热搜第一发布...")
        
        # 使用默认话题（实际应用中这里会获取真实热搜）
        default_topic = "当前热门社会话题"
        content = generate_simple_content(default_topic, is_auto=True)
        
        # 内容验证
        print("\n🔍 正在验证内容...")
        validation_result = validate_content(content, default_topic)
        
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
        preview_content(content, default_topic)
        
        # 确认发布
        print("\n🚀 开始发布...")
        result = self.publisher.publish_weibo(content)
        
        if result:
            print(f"\n🎉 自动热搜发布成功！")
            print(f"🎯 话题: {default_topic}")
            print(f"📊 统计: {len(content)}字 | 自动选择 | 通俗易懂")
            return True
        else:
            print("\n❌ 发布失败")
            return False
    
    def publish_specific_topic(self, custom_topic):
        """发布指定话题"""
        print(f"🎯 开始发布指定话题: {custom_topic}")
        
        # 生成通俗易懂的内容
        content = generate_simple_content(custom_topic, is_auto=False)
        
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
            print(f"\n🎉 指定话题发布成功！")
            print(f"🎯 话题: {custom_topic}")
            print(f"📊 统计: {len(content)}字 | 指定话题 | 通俗易懂")
            return True
        else:
            print("\n❌ 发布失败")
            return False

def main():
    import sys
    
    if len(sys.argv) > 1:
        # 指定话题模式
        custom_topic = " ".join(sys.argv[1:])
        publisher = FlexibleWeiboPublisherV3()
        publisher.publish_specific_topic(custom_topic)
    else:
        # 自动热搜模式  
        publisher = FlexibleWeiboPublisherV3()
        publisher.publish_auto_hot_search()

if __name__ == "__main__":
    main()
