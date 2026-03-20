#!/bin/bash

# 简化的微博热搜推送脚本
# 使用直接搜索方式

set -e

WORKSPACE_DIR="/home/ubuntu/.openclaw/workspace"
NEWS_JSON="$WORKSPACE_DIR/news.json"
LOG_FILE="$WORKSPACE_DIR/news-push.log"
API_KEY="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"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 微博热搜推送开始" >> "$LOG_FILE"

# 直接调用搜索脚本
cd "$WORKSPACE_DIR"

# 执行搜索并捕获输出
SEARCH_OUTPUT=$(python3 skills/tavily/scripts/tavily_search.py "微博热搜" --api-key "$API_KEY" --topic news --max-results 10 2>&1)
SEARCH_EXIT_CODE=$?

echo "搜索退出码: $SEARCH_EXIT_CODE" >> "$LOG_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 微博热搜推送完成" >> "$LOG_FILE"