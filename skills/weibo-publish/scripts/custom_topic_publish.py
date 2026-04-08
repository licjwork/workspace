#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from weibo_publisher import WeiboPublisher

def publish_custom_topic():
    topic = "住酒店不带毛巾的人天塌了"
    title = f"🔥 😱 {topic}背后的深层原因！网友炸锅了！"
    content = f"""
📰 4月8日热门话题深度解析：

🎯 【事件核心】{topic}

💡 【深度分析】
这个看似简单的话题实际上反映了现代人出门在外的各种困扰。酒店毛巾的质量参差不齐，很多人出于卫生考虑选择自带毛巾，这背后体现的是消费者对服务品质的高要求。

🤔 【社会观察】
这种现象折射出服务业标准化建设的迫切性。消费者宁愿自带用品也不愿使用酒店提供的，说明信任缺失问题严重。现代人越来越注重个人卫生和生活品质，对服务行业的标准要求也越来越高。

💭 【个人建议】
建议酒店行业加强用品品质管控，建立标准化服务体系，让消费者住得安心、用得放心。同时，消费者也可以选择信誉好的连锁酒店，降低风险。

你怎么看待这个现象？欢迎分享你的经历！#酒店生活 #消费观察 #服务质量
"""
    
    print("🎯 开始发布指定话题的热点内容...")
    print(f"🎯 选定话题: {topic}")
    print(f"🔥 吸睛标题: {title}")
    print(f"📝 内容长度: {len(content)} 字")
    
    # 发布微博
    publisher = WeiboPublisher()
    result = publisher.publish_weibo(content)
    
    if result:
        print("\n🎉 指定话题微博发布成功！")
        print(f"📊 发布统计: {len(content)}字 | 专注话题 | 深度分析")
        print(f"🎯 分析话题: {topic}")
        return True
    else:
        print("\n❌ 发布失败，请检查网络和登录状态")
        return False

if __name__ == "__main__":
    publish_custom_topic()
