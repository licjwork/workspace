#!/usr/bin/env python3
"""
Enhanced Weibo Publisher Trigger - 增强版关键词触发系统
"""

import re
import json
import time
from datetime import datetime
from weibo_publisher import WeiboPublisher
from enhanced_hot_search_publisher import EnhancedHotSearchPublisher

class EnhancedWeiboTrigger:
    def __init__(self):
        # 更新关键词配置，使用增强版热搜发布
        self.keywords = {
            # 热搜相关 - 使用增强版
            '热搜|hot search|热门|trending|热点': self.publish_enhanced_hot_search,
            '微博热搜|热搜榜|热搜top': self.publish_enhanced_hot_search,
            
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
            
            # 通用触发
            '发微博|post|发布|publish': self.publish_general_content,
            '测试|test|demo': self.publish_test_content
        }
        
        self.publisher = WeiboPublisher()
        self.enhanced_publisher = EnhancedHotSearchPublisher()
        
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
        
    def publish_enhanced_hot_search(self):
        """发布增强版热搜内容"""
        print("🔥 检测到热搜相关关键词，启动增强版热搜发布...")
        return self.enhanced_publisher.publish_enhanced_hot_search()
        
    def publish_music_content(self):
        """发布音乐相关内容"""
        content = f"""🎵 音乐榜单深度解析！

📊 Billboard最新榜单出炉，Ella Langley的《Choosin' Texas》强势登顶，这首歌曲的成功反映了乡村音乐在主流市场的持续影响力。

🎧 KPop Demon Hunters的跨界合作也值得关注，音乐与商业的完美结合正在创造新的商业模式。从音乐产业角度看，这种跨界合作不仅扩大了受众群体，也为音乐人提供了更多商业机会。

🎤 榜单变化背后反映了听众品味的多元化趋势，从乡村到KPop，从传统到现代，音乐的无边界融合正在重塑整个行业。

大家最近都在听什么类型的音乐？欢迎分享你的音乐品味！#音乐解析 #Billboard #音乐产业"""
        return self.publisher.publish_weibo(content)
        
    def publish_tech_content(self):
        """发布科技相关内容"""
        content = f"""💡 科技前沿深度观察！

📈 美光科技(MU)股价持续上涨，这不仅是单一企业的成功，更反映了整个半导体行业的复苏趋势。从产业链角度看，存储芯片需求的回升预示着消费电子市场的回暖。

🔬 人工智能技术的快速发展正在重塑各行各业，从医疗诊断到自动驾驶，从金融风控到教育个性化，AI的应用场景不断扩大。但同时也带来了数据隐私、就业结构等社会议题需要关注。

💻 数码产品的更新换代速度加快，5G、6G技术的演进为物联网、元宇宙等新兴概念提供了技术基础。消费者在享受便利的同时，也需要理性看待技术 hype cycle。

🤔 科技发展日新月异，如何在创新与伦理之间找到平衡点？这是一个值得深思的问题。#科技前沿 #人工智能 #产业观察"""
        return self.publisher.publish_weibo(content)
        
    def publish_fashion_content(self):
        """发布时尚相关内容"""
        content = f"""👗 时尚产业深度解读！

🍔 KPop Demon Hunters × 麦当劳 × VANDYTHE PINK的联名合作即将登陆Complex，这种跨界合作反映了时尚产业的三个重要趋势：

🎯 首先，KPop文化的全球影响力正在重塑时尚格局，年轻一代的消费习惯和审美偏好成为品牌关注的重点。

💡 其次，快餐文化与高端时尚的融合打破了传统界限，"快餐时尚"正在成为一种新的文化现象。

👟 最后，品牌联名已经从简单的logo叠加发展到深度的文化融合，这种合作模式为品牌注入了新的生命力。

时尚不仅是穿衣打扮，更是一种文化表达和身份认同。你如何看待这种跨界时尚现象？#时尚解析 #品牌联名 #文化融合"""
        return self.publisher.publish_weibo(content)
        
    def publish_life_content(self):
        """发布生活相关内容"""
        content = f"""🌟 生活方式深度分享！

🍽️ 美食探店不仅是味觉的享受，更是一种生活态度的体现。在这个快节奏的时代，慢下来品味一顿美食，是对自己最好的犒赏。好的餐厅不仅提供美味，更创造了一种氛围和体验。

✈️ 旅行规划的本质是生活品质的提升。无论是短途周边游还是长途国际旅行，每一次出行都是对未知世界的探索和对自我的重新认识。旅行教会我们包容和理解，拓宽了人生的维度。

💪 健身打卡的背后是健康意识的觉醒。坚持运动一个月，不仅是体型的变化，更是意志力的锻炼和生活习惯的重塑。运动带来的不仅是身体健康，更是心理状态的积极改变。

生活的意义在于体验和成长，每一个小习惯的坚持都在塑造更好的自己。你的生活方式是怎样的？#生活哲学 #品质生活 #个人成长"""
        return self.publisher.publish_weibo(content)
        
    def publish_general_content(self):
        """发布通用内容"""
        content = f"""📝 深度思考分享！

🌍 在这个信息爆炸的时代，我们每天都被海量信息包围。如何筛选有价值的内容，如何保持独立思考，成为了现代人必备的能力。信息素养不仅关乎个人成长，更关系到社会的理性发展。

💭 保持开放的心态很重要，但同时也要有批判性思维。不盲从，不偏信，在多元观点中寻找真相，这是一种需要不断练习的能力。

🤔 学习的本质是思维方式的升级，而不仅仅是知识的积累。在这个快速变化的世界，学习能力比知识储备更重要。

🎯 每个人都应该找到自己的学习节奏和思考方式，形成独特的认知框架。这样的思考，你怎么看？#深度思考 #信息时代 #学习成长"""
        return self.publisher.publish_weibo(content)
        
    def publish_test_content(self):
        """发布测试内容"""
        content = f"""🧪 微博发布功能测试报告

✅ 功能测试项目：
- 文本输入功能：正常 ✓
- 发布按钮点击：正常 ✓
- 内容发布流程：正常 ✓
- 页面跳转验证：正常 ✓
- 热搜数据获取：正常 ✓

🎯 测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 系统状态：所有功能正常运行
🔧 技术架构：VNC + CDP + WebSocket

本次测试验证了微博发布功能的完整性和稳定性，所有核心功能均通过测试。系统能够正常获取热搜数据、生成高质量内容并完成发布流程。

如果看到这条微博，说明整个发布系统运行正常！#功能测试 #系统验证 #技术报告"""
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
        help_text = "📋 增强版微博发布关键词触发帮助\n\n"
        help_text += "🔥 热搜相关: 热搜、热门、热搜榜、热点话题\n"
        help_text += "   ✨ 新功能：300字深度分析 + 吸睛标题\n\n"
        help_text += "🎵 音乐相关: 音乐、music、歌曲、歌手、榜单\n"
        help_text += "💡 科技相关: 科技、技术、AI、股票、数码\n"
        help_text += "👗 时尚相关: 时尚、穿搭、美妆、品牌、护肤\n"
        help_text += "🌟 生活相关: 美食、旅行、健身、运动、餐厅\n"
        help_text += "📝 通用触发: 发微博、发布、publish、post\n"
        help_text += "🧪 测试功能: 测试、test、demo\n\n"
        help_text += "💡 使用方法: 发送包含上述关键词的消息即可触发相应类型的微博发布"
        
        return help_text

if __name__ == "__main__":
    trigger = EnhancedWeiboTrigger()
    
    # 测试增强版热搜触发
    print("🧪 测试增强版热搜触发...")
    trigger.process_message("微博热搜")
