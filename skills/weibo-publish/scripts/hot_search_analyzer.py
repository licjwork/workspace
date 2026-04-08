#!/usr/bin/env python3
import sys
import os
import time
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from weibo_publisher import WeiboPublisher

class HotSearchAnalyzer:
    def __init__(self):
        self.publisher = WeiboPublisher()
        
    def connect_browser(self):
        """连接浏览器"""
        return self.publisher.connect_browser()
    
    def get_hot_search_topics(self, limit=10):
        """获取热搜话题列表"""
        try:
            # 导航到热搜页面
            print("🔍 正在获取微博热搜...")
            self.publisher.cdp.navigate("https://s.weibo.com/top/summary")
            self.publisher.cdp.wait_load()
            
            # 提取热搜话题
            script = """
            const topics = [];
            const items = document.querySelectorAll('.td-02 a');
            items.forEach((el, index) => {
                if (index < 10 && el.textContent.trim()) {
                    const title = el.textContent.trim();
                    const link = el.href;
                    topics.push({
                        title: title,
                        link: link,
                        rank: index + 1
                    });
                }
            });
            topics;
            """
            
            topics = self.publisher.cdp.evaluate(script)
            print(f"✅ 成功获取 {len(topics)} 个热搜话题")
            return topics if topics else []
            
        except Exception as e:
            print(f"❌ 获取热搜失败: {e}")
            return []
    
    def get_topic_comments(self, topic_url, limit=5):
        """获取话题下的热门评论"""
        try:
            print(f"🔍 正在获取话题评论: {topic_url}")
            
            # 导航到话题页面
            self.publisher.cdp.navigate(topic_url)
            self.publisher.cdp.wait_load()
            
            # 等待评论加载
            time.sleep(3)
            
            # 提取热门评论
            script = """
            const comments = [];
            const commentEls = document.querySelectorAll('.txt, .comment_txt');
            commentEls.forEach((el, index) => {
                if (index < 5 && el.textContent.trim()) {
                    comments.push({
                        text: el.textContent.trim(),
                        index: index + 1
                    });
                }
            });
            comments;
            """
            
            comments = self.publisher.cdp.evaluate(script)
            print(f"✅ 成功获取 {len(comments)} 条评论")
            return comments if comments else []
            
        except Exception as e:
            print(f"❌ 获取评论失败: {e}")
            return []
    
    def analyze_topic_sentiment(self, topic, comments):
        """分析话题情感倾向"""
        if not comments:
            return "中性", "暂无足够评论数据"
        
        # 简单的情感分析
        positive_words = ["好", "支持", "赞同", "喜欢", "不错", "可以", "厉害", "牛逼"]
        negative_words = ["差", "反对", "讨厌", "垃圾", "不行", "垃圾", "傻", "蠢"]
        
        positive_count = 0
        negative_count = 0
        
        all_text = " ".join([comment.get('text', '') for comment in comments])
        
        for word in positive_words:
            if word in all_text:
                positive_count += 1
        
        for word in negative_words:
            if word in all_text:
                negative_count += 1
        
        if positive_count > negative_count:
            return "正面", f"正面评论较多 ({positive_count} vs {negative_count})"
        elif negative_count > positive_count:
            return "负面", f"负面评论较多 ({negative_count} vs {positive_count})"
        else:
            return "中性", "正负面评论相当"
    
    def get_topic_context(self, topic):
        """获取话题背景信息"""
        # 基于话题内容的简单分析
        context_hints = {
            "工作": "就业市场",
            "工资": "收入水平", 
            "高铁": "交通运输",
            "花钱": "消费行为",
            "选择": "决策分析",
            "生活": "生活方式",
            "社会": "社会现象",
            "新闻": "时事热点"
        }
        
        contexts = []
        for keyword, context in context_hints.items():
            if keyword in topic:
                contexts.append(context)
        
        return contexts if contexts else ["社会热点"]

if __name__ == "__main__":
    analyzer = HotSearchAnalyzer()
    
    if analyzer.connect_browser():
        # 测试获取热搜
        topics = analyzer.get_hot_search_topics()
        print("\n📊 热搜话题:")
        for topic in topics[:5]:
            print(f"   {topic['rank']}. {topic['title']}")
        
        # 测试获取评论
        if topics:
            comments = analyzer.get_topic_comments(topics[0]['link'])
            print(f"\n💬 热门评论:")
            for comment in comments[:3]:
                print(f"   • {comment['text'][:50]}...")
    else:
        print("❌ 浏览器连接失败")
