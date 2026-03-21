#!/bin/bash

# 国际最新新闻推送脚本（支持10条新闻）
# 流程：搜索 -> AI解析 -> AI翻译

set -e

WORKSPACE_DIR="/home/ubuntu/.openclaw/workspace"
NEWS_JSON="$WORKSPACE_DIR/news.json"
LOG_FILE="$WORKSPACE_DIR/news-push.log"

# 加载环境变量
if [ -f "/home/ubuntu/.openclaw/.env" ]; then
    # 直接加载.env文件（确保文件格式正确）
    set -o allexport
    source /home/ubuntu/.openclaw/.env
    set +o allexport
    API_KEY="$TAVILY_API_KEY"
else
    echo "错误：环境变量文件未找到" >> "$LOG_FILE"
    API_KEY="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"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 国际最新新闻推送开始（10条）" >> "$LOG_FILE"

# 执行搜索
cd "$WORKSPACE_DIR"

# 搜索国际最新新闻（10条）
SEARCH_RESULT=$(timeout 60 python3 skills/tavily/scripts/tavily_search.py "国际最新新闻" --api-key "$API_KEY" --topic news --max-results 10 2>&1)
SEARCH_EXIT_CODE=$?

echo "搜索退出码: $SEARCH_EXIT_CODE" >> "$LOG_FILE"

# 创建临时Python脚本来处理搜索结果（搜索->AI解析->AI翻译）
cat > /tmp/process_news_ai.py << 'EOF'
import json
import sys
import re
import subprocess

# 读取搜索结果
search_result = sys.stdin.read()

# AI解析函数：从搜索结果中提取新闻条目
def ai_parse_news(search_result):
    """使用AI解析搜索结果，提取新闻条目"""
    
    # 提取AI答案（用于主要内容）
    ai_answer_match = re.search(r'=== AI ANSWER ===\n(.*?)\n=== RESULTS ===', search_result, re.DOTALL)
    ai_answer = ai_answer_match.group(1).strip() if ai_answer_match else ""
    
    # 提取搜索结果条目
    results_match = re.search(r'=== RESULTS ===\n(.*)', search_result, re.DOTALL)
    results_section = results_match.group(1) if results_match else ""
    
    # 解析新闻条目
    news_items = []
    current_item = None
    lines = results_section.strip().split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 检查是否是新的新闻条目
        if line and line[0].isdigit() and '. ' in line and 'URL:' not in line and 'Score:' not in line:
            if current_item:
                news_items.append(current_item)
            
            parts = line.split('. ', 1)
            if len(parts) >= 2:
                index = int(parts[0])
                title_part = parts[1]
                
                # 提取标题
                title = title_part.split(' - URL:')[0].split(' - ')[0] if ' - ' in title_part else title_part
                current_item = {
                    "index": index,
                    "title": title.strip(),
                    "summary": "",
                    "keywords": [],
                    "key_data": []
                }
                
                # 查找摘要
                j = i + 1
                while j < len(lines) and current_item["summary"] == "":
                    if lines[j].strip().startswith('#') and len(lines[j].strip()) > 20:
                        summary = lines[j].strip()[1:].strip()
                        # 检查是否是股票指数信息
                        if not summary.startswith('KBW ') and not summary.startswith('S&P ') and not summary.startswith('For non-personal'):
                            if len(summary) > 350:
                                summary = summary[:350] + "..."
                            current_item["summary"] = summary
                        else:
                            # 股票指数信息，查找后面的行
                            k = j + 1
                            found_summary = False
                            while k < len(lines):
                                while k < len(lines) and lines[k].strip() == "":
                                    k += 1
                                if k >= len(lines):
                                    break
                                line_content = lines[k].strip()
                                if not line_content.startswith(('KBW ', 'S&P ', 'For non-personal', 'URL:', 'Score:', 'Image ', 'Copy ', 'As long as', 'For non-personal use')):
                                    summary = line_content
                                    if len(summary) > 350:
                                        summary = summary[:350] + "..."
                                    current_item["summary"] = summary
                                    found_summary = True
                                    break
                                k += 1
                            if not found_summary:
                                # 使用标题作为摘要
                                title_parts = current_item["title"].split(' - ')
                                if len(title_parts) > 1:
                                    summary = title_parts[0]
                                else:
                                    summary = current_item["title"]
                                if len(summary) > 350:
                                    summary = summary[:350] + "..."
                                current_item["summary"] = summary
                    j += 1
                
                # 如果没有找到摘要，尝试其他方式
                if current_item["summary"] == "":
                    j = i + 1
                    while j < len(lines) and current_item["summary"] == "":
                        line_content = lines[j].strip()
                        if len(line_content) > 30 and not line_content.startswith(('URL:', 'Score:', 'KBW ', 'S&P ', 'For non-personal', 'Image ', 'Copy ')):
                            summary = line_content
                            if len(summary) > 350:
                                summary = summary[:350] + "..."
                            current_item["summary"] = summary
                            break
                        j += 1
                
                # 达到10条新闻停止
                if len(news_items) >= 9:
                    break
        
        i += 1
    
    # 添加最后一个条目
    if current_item and current_item["summary"]:
        news_items.append(current_item)
    
    # 如果没有新闻，使用AI答案
    if len(news_items) == 0:
        if ai_answer:
            summary = ai_answer[:500] if len(ai_answer) > 500 else ai_answer
            news_items = [{"index": 1, "title": "国际最新新闻", "summary": summary}]
        else:
            news_items = [{"index": 1, "title": "国际新闻", "summary": "今日无新闻数据"}]
    
    # 按索引排序
    news_items.sort(key=lambda x: x["index"])
    
    # 创建结果结构
    import datetime
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 使用AI答案作为主要内容
    main_content = ai_answer[:1000] if len(ai_answer) > 1000 else ai_answer
    
    return {
        "last_update": now,
        "content": main_content,
        "news_list": news_items[:10]  # 最多保留10条新闻
    }

# 简单的翻译函数，直接调用翻译API
def translate_with_ai(text):
    """使用AI翻译文本"""
    if not text:
        return ""
    
    # 如果文本太短，直接返回
    if len(text) < 10:
        return text
    
    try:
        # 调用LongCat AI翻译API
        import requests
        api_key = os.environ.get('LONGCAT_API_KEY')
        if not api_key:
            return text
        
        url = "https://api.longcat.chat/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""请将以下英文内容翻译成中文：

要求：
- 保持原文意思准确
- 使用专业流畅的中文表达
- 不要添加任何注释、说明或解释文字

需要翻译的内容：
{text}"""
        
        data = {
            "model": "LongCat-Flash-Chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 2000,
            "temperature": 0.3,
            "stream": False
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            translated = result['choices'][0]['message']['content'].strip()
            # 清理可能残留的注释
            translated = re.sub(r'（注：[^）]*）', '', translated)
            translated = re.sub(r'【注】[^】]*】', '', translated)
            translated = re.sub(r'\(注: [^)]*\)', '', translated)
            translated = re.sub(r'注释：[^\n]*', '', translated)
            translated = re.sub(r'说明：[^\n]*', '', translated)
            translated = re.sub(r'\n\s*\n', '\n\n', translated)
            return translated.strip()
        else:
            return text
    except Exception as e:
        return text

# AI解析新闻
parsed_data = ai_parse_news(search_result)

# AI翻译所有内容
def translate_news_data(data):
    """翻译新闻数据"""
    # 翻译主要内容
    if data["content"]:
        data["content"] = translate_with_ai(data["content"])
    
    # 翻译新闻列表
    for item in data["news_list"]:
        if item["summary"]:
            item["summary"] = translate_with_ai(item["summary"])
    
    return data

# 执行翻译
translated_data = translate_news_data(parsed_data)

# 输出最终JSON
print(json.dumps(translated_data, ensure_ascii=False, indent=2))
EOF

# 处理搜索结果并生成JSON（搜索->AI解析->AI翻译）
if [ $SEARCH_EXIT_CODE -eq 0 ]; then
    echo "$SEARCH_RESULT" | python3 /tmp/process_news_ai.py > "$NEWS_JSON"
    
    # 调试：输出新闻数量
    NEWS_COUNT=$(python3 -c "import json; data=json.load(open('$NEWS_JSON')); print(len(data.get('news_list', [])))")
    echo "解析到 $NEWS_COUNT 条新闻" >> "$LOG_FILE"
else
    # 如果搜索失败，使用默认内容
    cat > "$NEWS_JSON" << EOF
{
  "last_update": "$(date '+%Y-%m-%d %H:%M:%S')",
  "content": "国际新闻搜索失败，使用默认内容",
  "news_list": [
    {
      "index": 1,
      "title": "国际新闻",
      "summary": "今日国际新闻搜索失败，请稍后重试"
    }
  ]
}
EOF
fi

echo "已生成news.json文件" >> "$LOG_FILE"

# 复制到后端API期望的路径
cp "$NEWS_JSON" "/home/ubuntu/.openclaw/workspace/web-navigation-system/database/news.json"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 国际最新新闻推送完成（10条）" >> "$LOG_FILE"