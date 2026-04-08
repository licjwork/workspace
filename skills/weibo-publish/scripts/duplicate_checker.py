#!/usr/bin/env python3
import os
import json
from datetime import datetime, timedelta

class DuplicateChecker:
    def __init__(self, history_file="/tmp/weibo_publish_history.json"):
        self.history_file = history_file
        self.load_history()
    
    def load_history(self):
        """加载发布历史"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except:
                self.history = {}
        else:
            self.history = {}
    
    def save_history(self):
        """保存发布历史"""
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
    
    def is_duplicate(self, topic, content, time_window_minutes=30):
        """检查是否为重复发布"""
        current_time = datetime.now()
        
        # 清理过期记录（超过1小时的）
        expired_time = current_time - timedelta(hours=1)
        self.history = {
            k: v for k, v in self.history.items() 
            if datetime.fromisoformat(v['timestamp']) > expired_time
        }
        
        # 检查相同话题
        for key, record in self.history.items():
            record_time = datetime.fromisoformat(record['timestamp'])
            time_diff = current_time - record_time
            
            # 如果在时间窗口内且话题相似，认为是重复
            if time_diff < timedelta(minutes=time_window_minutes):
                if self.is_similar_topic(topic, record['topic']):
                    return True, record['topic']
                # 检查内容相似度
                if self.is_similar_content(content, record['content']):
                    return True, record['topic']
        
        return False, None
    
    def is_similar_topic(self, topic1, topic2):
        """检查话题是否相似"""
        # 简单的关键词匹配
        topic1_words = set(topic1.replace("，", " ").replace("。", " ").split())
        topic2_words = set(topic2.replace("，", " ").replace("。", " ").split())
        
        # 如果有超过50%的关键词相同，认为是相似话题
        common_words = topic1_words.intersection(topic2_words)
        similarity = len(common_words) / max(len(topic1_words), len(topic2_words))
        
        return similarity > 0.5
    
    def is_similar_content(self, content1, content2):
        """检查内容是否相似（简化版）"""
        # 如果内容长度相差很大，不认为是重复
        len_diff = abs(len(content1) - len(content2))
        if len_diff > 50:
            return False
        
        # 简单的关键词相似度检查
        words1 = set(content1.replace("\n", " ").replace(" ", " ").split())
        words2 = set(content2.replace("\n", " ").replace(" ", " ").split())
        
        common_words = words1.intersection(words2)
        similarity = len(common_words) / max(len(words1), len(words2))
        
        return similarity > 0.7
    
    def record_publish(self, topic, content):
        """记录发布历史"""
        key = f"{topic}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self.history[key] = {
            'topic': topic,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        self.save_history()

if __name__ == "__main__":
    # 测试
    checker = DuplicateChecker()
    topic = "12人花30万买月薪2500的高铁工作"
    content = "🔥 这个选择真的值得吗？..."
    
    is_dup, similar_topic = checker.is_duplicate(topic, content)
    print(f"是否重复: {is_dup}, 相似话题: {similar_topic}")
