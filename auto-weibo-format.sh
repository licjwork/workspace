#!/bin/bash

# 格式化的微博热搜推送脚本
# news.json格式与前端期望的格式匹配

set -e

WORKSPACE_DIR="/home/ubuntu/.openclaw/workspace"
NEWS_JSON="$WORKSPACE_DIR/news.json"
LOG_FILE="$WORKSPACE_DIR/news-push.log"
API_KEY="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"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 微博热搜推送开始" >> "$LOG_FILE"

# 执行搜索
cd "$WORKSPACE_DIR"

# 搜索最新科技新闻
SEARCH_RESULT=$(timeout 60 python3 skills/tavily/scripts/tavily_search.py "最新科技新闻" --api-key "$API_KEY" --topic news --max-results 5 2>&1)
SEARCH_EXIT_CODE=$?

echo "搜索退出码: $SEARCH_EXIT_CODE" >> "$LOG_FILE"

# 解析搜索结果
if [ $SEARCH_EXIT_CODE -eq 0 ]; then
    # 提取AI答案（只取=== AI ANSWER ===到=== RESULTS ===之间的内容）
    AI_ANSWER=$(echo "$SEARCH_RESULT" | sed -n '/=== AI ANSWER ===/,/=== RESULTS ===/{/=== AI ANSWER ===/!{/=== RESULTS ===/!p;}}' | tr '\n' ' ' | sed 's/  */ /g' | sed 's/^ *//g' | sed 's/ *$//g')
    
    # 如果AI答案为空，使用默认内容
    if [ -z "$AI_ANSWER" ]; then
        AI_ANSWER="今日科技新闻搜索失败，请稍后重试"
    fi
    
    # 创建与前端期望格式匹配的JSON数据
    cat > "$NEWS_JSON" << EOF
{
  "last_update": "$(date '+%Y-%m-%d %H:%M:%S')",
  "content": "$AI_ANSWER",
  "news_list": [
    {
      "index": 1,
      "title": "科技新闻速递",
      "summary": "$AI_ANSWER"
    }
  ]
}
EOF
else
    # 如果搜索失败，使用默认内容
    cat > "$NEWS_JSON" << EOF
{
  "last_update": "$(date '+%Y-%m-%d %H:%M:%S')",
  "content": "科技新闻搜索失败，使用默认内容",
  "news_list": [
    {
      "index": 1,
      "title": "科技新闻速递",
      "summary": "今日科技新闻搜索失败，请稍后重试"
    }
  ]
}
EOF
fi

echo "已生成news.json文件" >> "$LOG_FILE"

# 复制到后端API期望的路径
cp "$NEWS_JSON" "/home/ubuntu/.openclaw/workspace/web-navigation-system/database/news.json"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 微博热搜推送完成" >> "$LOG_FILE"