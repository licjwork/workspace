import re

# 读取原文件
with open('/home/ubuntu/.openclaw/workspace/skills/weibo-publish/scripts/smart_weibo_publisher.py', 'r') as f:
    content = f.read()

# 检查是否已经添加了验证
if 'validate_research_content' not in content:
    # 添加验证方法 - 在generate_content方法之前插入
    validation_method = '''    def validate_research_content(self):
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

'''
    
    # 找到generate_content方法的位置并在之前插入验证方法
    generate_pos = content.find('    def generate_content(self):')
    if generate_pos != -1:
        new_content = content[:generate_pos] + validation_method + content[generate_pos:]
        
        # 在generate_content方法开始处添加验证调用
        lines = new_content.split('\n')
        for i, line in enumerate(lines):
            if 'def generate_content(self):' in line:
                # 找到print语句的下一行插入验证
                for j in range(i+1, min(i+10, len(lines))):
                    if 'print(f"\\n🎯 正在为话题' in lines[j]:
                        # 在该行后面插入验证调用
                        lines.insert(j+1, '        ')
                        lines.insert(j+2, '        # AI判断调研内容有效性')
                        lines.insert(j+3, '        if not self.validate_research_content():')
                        lines.insert(j+4, '            print("❌ 调研内容无效，终止微博生成任务")')
                        lines.insert(j+5, '            return None')
                        break
                break
        
        # 写入文件
        with open('/home/ubuntu/.openclaw/workspace/skills/weibo-publish/scripts/smart_weibo_publisher.py', 'w') as f:
            f.write('\n'.join(lines))
        
        print('✅ 已成功添加AI内容验证层')
    else:
        print('❌ 未找到generate_content方法')
else:
    print('✅ AI验证层已存在')
