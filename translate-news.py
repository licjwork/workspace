#!/usr/bin/env python3
# 新闻翻译脚本 - 使用LongCat AI进行翻译
# 将英文科技新闻翻译成中文，不添加注释

import os
import sys
import json
import requests

# 加载环境变量
def load_env():
    """从.env文件加载环境变量"""
    env_path = "/home/ubuntu/.openclaw/.env"
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value.strip('"')

# 翻译函数
def translate_to_chinese(text):
    """
    使用LongCat AI将英文翻译成中文
    保留原文格式和结构，不添加注释
    """
    try:
        # 获取API密钥
        api_key = os.getenv('LONGCAT_API_KEY')
        if not api_key:
            print("错误：未找到LONGCAT_API_KEY环境变量")
            return text
        
        # API请求配置
        url = "https://api.longcat.chat/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 构建翻译提示（明确要求不添加注释）
        prompt = f"""请将以下英文科技新闻内容翻译成中文：

要求：
- 保持原文意思准确
- 使用专业流畅的中文表达
- 保留技术术语准确性
- 适合中文读者阅读
- 不要添加任何注释、说明或解释文字
- 直接输出翻译结果，不要额外内容
- 翻译完成后直接结束，不要总结或评价

需要翻译的内容：
{text}"""
        
        data = {
            "model": "LongCat-Flash-Chat",
            "messages": [
                {"role": "system", "content": "你是一个专业的科技新闻翻译助手，擅长将英文科技新闻准确翻译成中文。翻译要求：1.保持原文意思准确 2.使用专业流畅的中文表达 3.保留技术术语准确性 4.适合中文读者阅读 5.不要添加任何注释或说明文字 6.直接输出翻译结果，不要额外说明 7.翻译完成后直接结束，不要总结或评价"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.3,  # 使用较低的温度确保翻译准确性
            "stream": False
        }
        
        # 发送请求
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            translated_content = result['choices'][0]['message']['content'].strip()
            
            # 清理可能残留的注释（以防万一）
            # 移除以"（注："、"【注】"等开头的注释
            import re
            translated_content = re.sub(r'（注：[^）]*）', '', translated_content)
            translated_content = re.sub(r'【注】[^】]*】', '', translated_content)
            translated_content = re.sub(r'\(注: [^)]*\)', '', translated_content)
            translated_content = re.sub(r'注释：[^\n]*', '', translated_content)
            translated_content = re.sub(r'说明：[^\n]*', '', translated_content)
            
            # 清理多余的空格和换行
            translated_content = re.sub(r'\n\s*\n', '\n\n', translated_content)
            translated_content = translated_content.strip()
            
            print("✅ 翻译成功完成")
            return translated_content
        else:
            print(f"❌ 翻译请求失败，状态码：{response.status_code}")
            print(f"错误信息：{response.text}")
            return text
            
    except requests.exceptions.Timeout:
        print("❌ 翻译请求超时")
        return text
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，请检查网络")
        return text
    except Exception as e:
        print(f"❌ 翻译过程中发生错误：{str(e)}")
        return text

# 主函数
def main():
    """主函数：读取新闻文件，翻译内容，保存结果"""
    print("🔄 开始翻译新闻内容...")
    
    # 加载环境变量
    load_env()
    
    # 文件路径
    news_file = "/home/ubuntu/.openclaw/workspace/news.json"
    
    try:
        # 读取新闻文件
        with open(news_file, 'r', encoding='utf-8') as f:
            news_data = json.load(f)
        
        # 翻译content字段
        if 'content' in news_data:
            print(f"📝 原文长度：{len(news_data['content'])} 字符")
            translated_content = translate_to_chinese(news_data['content'])
            news_data['content'] = translated_content
            news_data['original_content'] = news_data['content']  # 保留原文
            print(f"📝 译文长度：{len(translated_content)} 字符")
        
        # 翻译news_list中的summary字段
        if 'news_list' in news_data:
            for item in news_data['news_list']:
                if 'summary' in item:
                    translated_summary = translate_to_chinese(item['summary'])
                    item['summary'] = translated_summary
                    item['original_summary'] = item['summary']  # 保留原文
        
        # 添加翻译标记
        news_data['translated'] = True
        news_data['translation_time'] = os.popen('date "+%Y-%m-%d %H:%M:%S"').read().strip()
        
        # 保存翻译后的文件
        with open(news_file, 'w', encoding='utf-8') as f:
            json.dump(news_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 翻译完成，结果已保存到：{news_file}")
        
    except FileNotFoundError:
        print(f"❌ 新闻文件未找到：{news_file}")
    except json.JSONDecodeError:
        print(f"❌ 新闻文件格式错误：{news_file}")
    except Exception as e:
        print(f"❌ 处理过程中发生错误：{str(e)}")

if __name__ == "__main__":
    main()