# 模拟测试验证逻辑
class MockPublisher:
    def __init__(self):
        # 模拟无效的调研数据
        self.research_data = {
            'searchResults': [
                {'content': ''},  # 空内容
                {'content': '   '},  # 只有空格  
                {'content': '短'}  # 内容太短
            ]
        }
        self.topic = "测试话题"
    
    def validate_research_content(self):
        """使用AI判断调研内容是否有效"""
        print(f"\\n🔍 正在判断调研内容有效性...")
        
        if not self.research_data or not self.research_data.get('searchResults'):
            print("❌ 调研数据为空，内容无效")
            return False
        
        # 检查是否有实质性内容
        valid_content_count = 0
        for item in self.research_data['searchResults']:
            if item['content'] and len(item['content'].strip()) > 20:
                valid_content_count += 1
        
        if valid_content_count >= 2:
            print("✅ 调研内容有效")
            return True
        else:
            print("❌ 调研内容无效，终止任务")
            return False

# 测试
publisher = MockPublisher()
result = publisher.validate_research_content()
print(f"验证结果: {result}")
