#!/usr/bin/env python3
"""
Weibo Publisher Trigger - Keyword-based publishing system
"""

import re
import json
import time
from datetime import datetime
from weibo_hot_search_publish import HotSearchPublisher
from weibo_publisher import WeiboPublisher

class WeiboTrigger:
    def __init__(self):
        self.keywords = {
            # 音乐相关
            '音乐|music|歌曲|song|榜单|billboard': self.publish_music_content,
            '歌手|singer|专辑|album|演唱会|concert': self.publish_music_content,
            
            # 科技相关
            '科技|tech|技术|technology|AI|人工智能': self.publish_tech_content,
            '股票|stock|股市|投资|investment': self.publish_tech_content,
            '数码|digital|手机|phone|电脑|computer': self.publish_tech_content,
            
            # 时尚相关
            '时尚|fashion|穿搭|outfit|品牌|brand': self.publish_fashion_content,
            '美妆|makeup|护肤|skincare|化妆品': self.publish_fashion_content,
            
            # 生活相关
            '美食|food|餐厅|restaurant|料理': self.publish_life_content,
            '旅行|travel|旅游|vacation|景点': self.publish_life_content,
            '健身|fitness|运动|exercise|减肥': self.publish_life_content,
            
            # 热点相关
            '热点|hot|热门|trending|热搜': self.publish_hot_content,
            '新闻|news|时事|current|事件': self.publish_hot_content,
            
            # 通用触发
            '发微博|post|发布|publish': self.publish_general_content,
            '测试|test|demo': self.publish_test_content
        }
        
        self.publisher = WeiboPublisher()
        self.hot_publisher = HotSearchPublisher()
        
    def detect_keywords(self, text):
        """检测文本中的关键词"""
        text = text.lower()
        triggered_keywords = []
        
        for keyword_pattern, handler in self.keywords.items():
            patterns = keyword_pattern.split('|')
            for pattern in patterns:
                if pattern.lower() in text:
                    triggered_keywords.append((pattern, handler))
                    break  # 避免重复添加同一个handler
                    
        return triggered_keywords
        
    def publish_music_content(self):
        """发布音乐相关内容"""
        content = f"🎵 今日音乐推荐！\n\n刚刚关注了最新的音乐动态，Billboard榜单更新，Ella Langley的《Choosin' Texas》表现亮眼！\n\n🎧 KPop Demon Hunters的跨界合作也值得关注，音乐与时尚的完美结合。\n\n大家最近都在听什么歌？欢迎分享！#音乐推荐 #Billboard #新歌分享"
        return self.publisher.publish_weibo(content)
        
    def publish_tech_content(self):
        """发布科技相关内容"""
        content = f"💡 科技资讯速递！\n\n📈 美光科技(MU)股价持续上涨，半导体行业迎来新机遇。\n\n🔬 人工智能技术不断发展，为各行各业带来创新变革。\n\n💻 数码产品的更新换代速度越来越快，消费者有了更多选择。\n\n科技改变生活，你怎么看未来的发展趋势？#科技资讯 #人工智能 #数码生活"
        return self.publisher.publish_weibo(content)
        
    def publish_fashion_content(self):
        """发布时尚相关内容"""
        content = f"👗 时尚潮流观察！\n\n🍔 KPop Demon Hunters × 麦当劳 × VANDYTHE PINK联名系列即将登陆Complex，这次的合作会带来什么惊喜？\n\n👟 时尚界的跨界合作越来越频繁，品牌联名为消费者带来更多选择。\n\n💄 无论是美妆还是穿搭，个性化表达成为了新的时尚趋势。\n\n你最喜欢哪个品牌的联名合作？#时尚潮流 #品牌联名 #KPop"
        return self.publisher.publish_weibo(content)
        
    def publish_life_content(self):
        """发布生活相关内容"""
        content = f"🌟 美好生活分享！\n\n🍽️ 美食探店：发现了一家新开的餐厅，环境很棒，菜品也很有特色。\n\n✈️ 旅行计划：最近在规划一次短途旅行，想要放松一下心情。\n\n💪 健身打卡：坚持运动已经一个月了，感觉身体状态好了很多。\n\n生活需要仪式感，也要有健康的节奏。你的美好生活是什么样子的？#生活分享 #美食 #旅行 #健身"
        return self.publisher.publish_weibo(content)
        
    def publish_hot_content(self):
        """发布热点相关内容"""
        return self.hot_publisher.publish_from_hot_search()
        
    def publish_general_content(self):
        """发布通用内容"""
        content = f"📝 日常分享！\n\n今天想和大家聊聊最近的观察和思考。\n\n🌍 世界变化很快，每天都有新的信息和观点涌现。\n\n💭 保持开放的心态，不断学习和适应，这是应对变化最好的方式。\n\n🤔 在这个信息爆炸的时代，如何筛选有价值的内容？\n\n欢迎在评论区分享你的看法！#日常思考 #信息时代 #学习成长"
        return self.publisher.publish_weibo(content)
        
    def publish_test_content(self):
        """发布测试内容"""
        content = f"🧪 测试微博发布功能 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n这是一条测试微博，用于验证发布功能是否正常工作。\n\n✅ 功能测试项目：\n- 文本输入 ✓\n- 发布按钮点击 ✓\n- 内容发布 ✓\n\n如果看到这条微博，说明发布功能正常！#测试 #功能验证"
        return self.publisher.publish_weibo(content)
        
    def process_message(self, message):
        """处理消息并触发相应的发布操作"""
        print(f"🔍 处理消息: {message}")
        
        # 检测关键词
        triggered_actions = self.detect_keywords(message)
        
        if not triggered_actions:
            print("❌ 未检测到触发关键词")
            return False
            
        print(f"✅ 检测到 {len(triggered_actions)} 个触发词")
        
        # 执行触发动作
        success_count = 0
        for keyword, handler in triggered_actions:
            print(f"🚀 执行关键词 '{keyword}' 对应的发布操作...")
            try:
                if handler():
                    print(f"✅ 关键词 '{keyword}' 发布成功")
                    success_count += 1
                else:
                    print(f"❌ 关键词 '{keyword}' 发布失败")
            except Exception as e:
                print(f"❌ 关键词 '{keyword}' 执行出错: {e}")
                
        return success_count > 0
        
    def get_help_text(self):
        """获取帮助文本"""
        help_text = "📋 微博发布关键词触发帮助\n\n"
        help_text += "🎵 音乐相关: 音乐、music、歌曲、歌手、榜单、演唱会\n"
        help_text += "💡 科技相关: 科技、技术、AI、股票、数码、手机\n"
        help_text += "👗 时尚相关: 时尚、穿搭、美妆、品牌、护肤\n"
        help_text += "🌟 生活相关: 美食、旅行、健身、运动、餐厅\n"
        help_text += "🔥 热点相关: 热点、热门、热搜、新闻、时事\n"
        help_text += "📝 通用触发: 发微博、发布、publish、post\n"
        help_text += "🧪 测试功能: 测试、test、demo\n\n"
        help_text += "💡 使用方法: 发送包含上述关键词的消息即可触发相应类型的微博发布"
        
        return help_text

if __name__ == "__main__":
    trigger = WeiboTrigger()
    
    # 测试不同的关键词
    test_messages = [
        "我想发一条关于音乐的微博",
        "发布一条科技资讯",
        "来一条时尚内容",
        "分享一些生活感悟",
        "发微博",
        "测试一下功能"
    ]
    
    print("🧪 开始关键词触发测试...")
    for message in test_messages:
        print(f"\n--- 测试消息: {message} ---")
        trigger.process_message(message)
        time.sleep(2)  # 间隔2秒
        
    print("\n📚 关键词触发帮助:")
    print(trigger.get_help_text())
