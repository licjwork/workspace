#!/bin/bash

# 微博热搜自动推送脚本
# 每天偶数小时执行

set -e

WORKSPACE_DIR="/home/ubuntu/.openclaw/workspace"
NEWS_JSON="$WORKSPACE_DIR/news.json"
LOG_FILE="$WORKSPACE_DIR/news-push.log"
API_KEY="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"

# 记录开始时间
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 微博热搜推送开始" >> "$LOG_FILE"

# 执行搜索并直接处理结果
cd "$WORKSPACE_DIR"

# 直接执行搜索并处理结果
python3 -c "
import json
import subprocess
import sys

# 执行搜索
result = subprocess.run([
    'python3', 'skills/tavily/scripts/tavily_search.py', 
    '微博热搜', 
    '--api-key', '$API_KEY', 
    '--topic', 'news', 
    '--max-results', '10'
], capture_output=True, text=True, timeout=30)

if result.returncode == 0 and result.stdout.strip():
    # 解析搜索结果
    lines = result.stdout.strip().split('\\n')
    results = []
    
    for line in lines:
        if 'Title:' in line:
            title = line.replace('Title: ', '').strip()
            if title:
                results.append({'title': title, 'url': ''})
    
    # 保存到JSON
    with open('$NEWS_JSON', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f'微博热搜搜索结果已保存，共{len(results)}条')
    
    # 构建消息内容
    message = '🔥 **微博热搜榜**\\n\\n'
    for i, item in enumerate(results[:10], 1):
        title = item.get('title', '').strip()
        if title:
            message += f'{i}. **{title}**\\n'
    
    message += '\\n🐕 来自狗蛋的实时热搜'
    
    print(f'准备发送微博热搜消息，共{len(results)}条')
    print(f'消息内容: {message}')
else:
    print('搜索失败，未获取到结果')
    with open('$NEWS_JSON', 'w', encoding='utf-8') as f:
        json.dump([], f)
" >> "$LOG_FILE" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 微博热搜推送完成" >> "$LOG_FILE"

# 清理临时文件
rm -f /tmp/weibo_search_result.txt