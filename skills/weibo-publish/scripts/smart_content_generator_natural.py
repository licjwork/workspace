#!/usr/bin/env python3
from hot_search_analyzer_fixed import HotSearchAnalyzer

class SmartContentGenerator:
    def __init__(self):
        self.analyzer = HotSearchAnalyzer()
        
    def generate_real_hot_search_content(self, custom_topic=None):
        """生成基于真实热搜分析的内容"""
        
        # 连接浏览器
        if not self.analyzer.connect_browser():
            return None, "❌ 浏览器连接失败"
        
        try:
            if custom_topic:
                # 指定话题模式
                print(f"🎯 分析指定话题: {custom_topic}")
                return self._analyze_specific_topic(custom_topic)
            else:
                # 自动热搜模式
                print("🎯 分析实时热搜...")
                return self._analyze_hot_search()
                
        except Exception as e:
            return None, f"❌ 内容生成失败: {str(e)}"
    
    def _analyze_specific_topic(self, topic):
        """分析指定话题"""
        # 获取热搜数据作为参考
        hot_topics = self.analyzer.get_hot_search_topics(5)
        
        # 查找相似话题
        similar_topic = None
        for hot_topic in hot_topics:
            if self._is_similar_topic(topic, hot_topic['title']):
                similar_topic = hot_topic
                break
        
        if similar_topic:
            # 如果找到相似热搜，获取其评论
            comments = self.analyzer.get_topic_comments(similar_topic['link'])
            sentiment, sentiment_desc = self.analyzer.analyze_topic_sentiment(topic, comments)
            contexts = self.analyzer.get_topic_context(topic)
            
            content = self._generate_content_with_analysis(
                topic, comments, sentiment, contexts, is_hot=True
            )
            
            return content, f"✅ 基于热搜#{similar_topic['rank']}分析生成"
        else:
            # 没有找到相似热搜，使用通用分析
            contexts = self.analyzer.get_topic_context(topic)
            content = self._generate_content_with_analysis(
                topic, [], "中性", contexts, is_hot=False
            )
            
            return content, "✅ 基于话题分析生成"
    
    def _analyze_hot_search(self):
        """分析实时热搜第一"""
        hot_topics = self.analyzer.get_hot_search_topics(1)
        
        if not hot_topics:
            return None, "❌ 获取热搜失败"
        
        top_topic = hot_topics[0]
        print(f"🎯 分析热搜第一: {top_topic['title']}")
        
        # 获取评论和情感分析
        comments = self.analyzer.get_topic_comments(top_topic['link'])
        sentiment, sentiment_desc = self.analyzer.analyze_topic_sentiment(top_topic['title'], comments)
        contexts = self.analyzer.get_topic_context(top_topic['title'])
        
        content = self._generate_content_with_analysis(
            top_topic['title'], comments, sentiment, contexts, is_hot=True
        )
        
        return content, f"✅ 基于实时热搜#{top_topic['rank']}分析生成"
    
    def _is_similar_topic(self, topic1, topic2):
        """检查话题相似度"""
        # 简单的关键词匹配
        words1 = set(topic1.replace("，", " ").replace("。", " ").split())
        words2 = set(topic2.replace("，", " ").replace("。", " ").split())
        
        common_words = words1.intersection(words2)
        similarity = len(common_words) / max(len(words1), len(words2)) if max(len(words1), len(words2)) > 0 else 0
        
        return similarity > 0.3
    
    def _extract_comment_insights(self, comments):
        """从评论中提取观点洞察"""
        if not comments:
            return []
        
        insights = []
        
        # 分析评论内容，提取关键观点
        for comment in comments[:3]:  # 取前3条评论
            text = comment.get('text', '')
            
            # 提取一些常见的观点模式
            if "支持" in text or "赞同" in text or "同意" in text:
                insights.append("有人表示支持和赞同")
            elif "反对" in text or "质疑" in text or "不认同" in text:
                insights.append("也有人提出质疑和反对")
            elif "理解" in text or "能懂" in text or "明白" in text:
                insights.append("不少人表示能够理解")
            elif "不理解" in text or "不懂" in text or "奇怪" in text:
                insights.append("也有人表示不太理解")
            elif "建议" in text or "应该" in text or "希望" in text:
                insights.append("大家给出了各种建议")
            elif "经历" in text or "遇到" in text or "亲身" in text:
                insights.append("有人分享了类似经历")
        
        # 去重
        return list(set(insights))
    
    def _generate_content_with_analysis(self, topic, comments, sentiment, contexts, is_hot=False):
        """基于分析结果生成内容"""
        
        # 提取评论洞察
        insights = self._extract_comment_insights(comments)
        
        # 根据情感倾向调整语气
        if sentiment == "正面":
            sentiment_phrase = "从网上的讨论来看，大多数人还是比较认可这个观点的"
            reaction = "👍"
        elif sentiment == "负面":
            sentiment_phrase = "不过从讨论中也能看出，有不少人持保留态度"
            reaction = "🤔"
        else:
            sentiment_phrase = "大家的看法比较多元，各有各的观点"
            reaction = "💭"
        
        # 根据是否热搜调整标题
        if is_hot:
            title = f"🔥 热搜话题！{topic}引发热议！"
        else:
            title = f"🔥 {topic}这个话题你怎么看？"
        
        # 构建洞察内容
        insight_text = ""
        if insights:
            # 随机选择1-2个洞察点
            selected_insights = insights[:2]
            if len(selected_insights) == 1:
                insight_text = f"\n\n{selected_insights[0]}，这确实值得我们深入思考。"
            else:
                insight_text = f"\n\n{selected_insights[0]}，同时{selected_insights[1]}，这确实值得我们深入思考。"
        
        # 生成完整内容
        content = f"""
{title}

说实话，{topic}这个话题确实很有意思。{sentiment_phrase}{reaction}

从{', '.join(contexts[:2])}的角度来看，这个现象反映了当下的一些现实情况。{insight_text}

我觉得每个话题都有不同的角度可以思考，重要的是保持理性讨论的态度。大家都是从自己的经历和立场出发，有不同的看法很正常。

你们对{topic}这个话题有什么想法？欢迎在评论区分享你的观点！#热点话题 #理性讨论 #社会观察
"""
        
        return content.strip()
