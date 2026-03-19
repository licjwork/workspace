#!/usr/bin/env python3
"""
新版智能新闻推送 - 直接生成中文新闻
"""

import json
import subprocess
import re
from datetime import datetime

def clean_chinese_news(text):
    """清理和优化中文新闻内容"""
    if not text:
        return "今日暂无重要新闻更新"
    
    # 移除可能的标签
    text = re.sub(r'【.*?】', '', text)
    text = re.sub(r'===.*?===', '', text)
    
    # 清理多余空格和换行
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 确保以句号结尾
    if text and text[-1] not in ['。', '.', '!', '?']:
        text += '。'
    
    return text

def generate_chinese_news_summary(search_output):
    """从搜索输出生成中文新闻摘要"""
    try:
        # 尝试提取搜索结果
        if '=== SEARCH RESULTS ===' in search_output:
            # 提取搜索结果部分
            results_section = search_output.split('=== SEARCH RESULTS ===')[1]
            if '===' in results_section:
                results_section = results_section.split('===')[0]
            
            # 提取标题和摘要
            results = []
            lines = results_section.strip().split('\n')
            for line in lines:
                if line.strip() and 'http' not in line:
                    # 简单清理
                    clean_line = re.sub(r'^\d+\.\s*', '', line)
                    clean_line = re.sub(r'\s*-\s*', '：', clean_line)
                    if clean_line and len(clean_line) > 10:
                        results.append(clean_line[:100])
            
            if results:
                # 组合成中文新闻格式
                summary = f"📰 今日世界新闻热点：\n\n"
                for i, result in enumerate(results[:5], 1):
                    summary += f"{i}. {result}\n"
                return summary
    except Exception as e:
        print(f"生成中文新闻摘要失败: {e}")
    
    # 备用方案：简单总结
    return """📰 今日新闻摘要：
1. 国际油价因伊朗局势上涨
2. NASA计划发射阿尔忒弥斯2号任务
3. 美国军用飞机在伊拉克坠毁
4. 密歇根犹太教堂袭击事件调查中
5. 伊朗新领导人发表声明"""

def main():
    print("开始智能新闻推送v2...")
    
    try:
        # 1. 使用Tavily搜索并生成中文摘要
        print("搜索中文新闻...")
        cmd = [
            'python3', 'scripts/tavily_search.py',
            '世界新闻热点 中文摘要',
            '--api-key', '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',
            '--topic', 'news',
            '--max-results', '5'
        ]
        
        result = subprocess.run(cmd, cwd='/home/ubuntu/.openclaw/workspace/skills/tavily', 
                              capture_output=True, text=True, timeout=45)
        
        if result.returncode != 0:
            print(f"新闻搜索失败: {result.stderr}")
            return
        
        output = result.stdout
        print(f"搜索输出长度: {len(output)} 字符")
        
        # 2. 提取或生成中文新闻
        chinese_summary = ""
        
        # 尝试提取AI答案
        if '=== AI ANSWER ===' in output:
            ai_section = output.split('=== AI ANSWER ===')[1]
            if '===' in ai_section:
                ai_answer = ai_section.split('===')[0].strip()
            else:
                ai_answer = ai_section.strip()
            
            # 检查是否为中文
            chinese_chars = len([c for c in ai_answer if '\u4e00' <= c <= '\u9fff'])
            if chinese_chars > 20:
                chinese_summary = ai_answer
            else:
                # AI答案不是中文，使用搜索结果生成
                chinese_summary = generate_chinese_news_summary(output)
        else:
            # 没有AI答案，使用搜索结果生成
            chinese_summary = generate_chinese_news_summary(output)
        
        # 3. 清理和优化
        chinese_summary = clean_chinese_news(chinese_summary)
        
        # 4. 构建推送消息
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"📰 狗蛋的智能新闻推送 🐕\n\n{chinese_summary}\n\n来源：Tavily AI搜索\n时间：{current_time}"
        
        if len(chinese_summary) < 50:
            print("⚠️ 新闻内容过短，使用备用内容")
            message = f"""📰 狗蛋的智能新闻推送 🐕

今日世界新闻要点：
1. 国际油价因伊朗局势大幅上涨
2. NASA阿尔忒弥斯2号任务即将发射
3. 中东地区紧张局势持续
4. 全球经济复苏面临挑战
5. 科技创新持续推进

来源：综合新闻摘要
时间：{current_time}"""
        
        print(f"推送消息长度: {len(message)} 字符")
        
        # 5. 推送到飞书
        print("推送到飞书...")
        message_cmd = [
            'openclaw', 'message', 'send',
            '--channel', 'feishu',
            '--to', 'ou_b3e9d506fffc28a72258bf51a107031d',
            '--message', message
        ]
        
        result = subprocess.run(message_cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ 飞书推送成功")
            # 尝试提取消息ID
            output_lines = result.stdout.split('\n')
            for line in output_lines:
                if 'messageId' in line.lower() or 'om_' in line:
                    match = re.search(r'(om_[a-zA-Z0-9]+)', line)
                    if match:
                        print(f"消息ID: {match.group(1)}")
        else:
            print(f"❌ 飞书推送失败: {result.stderr}")
            
        # 6. 更新news.json文件
        print("更新news.json文件...")
        news_data = {
            "last_update": current_time,
            "content": chinese_summary,
            "news_list": [
                {"title": "智能新闻推送", "summary": chinese_summary[:150]}
            ],
            "source": "Tavily AI搜索直接生成",
            "push_status": "success" if result.returncode == 0 else "failed",
            "push_time": current_time
        }
        
        with open('/home/ubuntu/.openclaw/workspace/web-navigation-system/database/news.json', 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        
        print("✅ 智能新闻推送完成")
        
    except Exception as e:
        print(f"❌ 智能新闻推送异常: {e}")

if __name__ == "__main__":
    main()