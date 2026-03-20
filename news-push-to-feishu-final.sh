#!/bin/bash

# 飞书新闻推送脚本（使用webhook方式）
WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/oc_6923bc623b1d9c2cbc58cbb33570b4fe"

# 检查新闻文件是否存在
NEWS_FILE="/home/ubuntu/.openclaw/workspace/news.json"
if [ ! -f "$NEWS_FILE" ]; then
    echo "❌ 新闻文件不存在: $NEWS_FILE"
    exit 1
fi

# 读取新闻内容
NEWS_CONTENT=$(cat "$NEWS_FILE")
TITLE=$(echo "$NEWS_CONTENT" | jq -r '.content // "今日新闻摘要"')
LAST_UPDATE=$(echo "$NEWS_CONTENT" | jq -r '.last_update // "未知时间"')

# 构建飞书消息
MESSAGE="📰 每日新闻推送\n\n📅 更新时间: $LAST_UPDATE\n\n$TITLE"

echo "发送新闻到飞书..."
echo "消息内容: $MESSAGE"

# 发送到飞书
RESPONSE=$(curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "text",
    "content": {
      "text": "'"$MESSAGE"'"
    }
  }')

# 记录日志
LOG_FILE="/home/ubuntu/.openclaw/workspace/news-push-to-feishu.log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 飞书推送结果: $RESPONSE" >> "$LOG_FILE"

# 检查响应
if echo "$RESPONSE" | grep -q '"code":0'; then
    echo "✅ 飞书推送成功！"
    echo "消息已发送到飞书群组"
else
    echo "❌ 飞书推送失败：$RESPONSE"
fi