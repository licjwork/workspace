#!/bin/bash

# 飞书推送测试脚本
WEBHOOK_URL="https://open.feishu.cn/open-apis/bot/v2/hook/132bf447-7a2b-4a47-a7e0-4e3f8d6e5e5e"

# 测试消息
MESSAGE="测试消息：飞书推送功能测试 - $(date '+%Y-%m-%d %H:%M:%S')"

echo "发送测试消息到飞书..."
echo "消息内容: $MESSAGE"

# 发送请求
RESPONSE=$(curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "text",
    "content": {
      "text": "'"$MESSAGE"'"
    }
  }')

echo "响应结果: $RESPONSE"

# 检查响应
if echo "$RESPONSE" | grep -q '"code":0'; then
    echo "✅ 飞书推送成功！"
else
    echo "❌ 飞书推送失败：$RESPONSE"
fi