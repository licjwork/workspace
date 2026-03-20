#!/bin/bash

# 飞书新闻推送脚本（使用appid/appsecret认证）
APP_ID="cli_a925064fe4385bdf"
APP_SECRET="ngR7VkQFEqctphPhYdA0Ecd5m7FRUmq4"

# 获取tenant_access_token
TOKEN_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "'"$APP_ID"'",
    "app_secret": "'"$APP_SECRET"'"
  }')

TOKEN=$(echo "$TOKEN_RESPONSE" | jq -r '.tenant_access_token // empty')
TOKEN_CODE=$(echo "$TOKEN_RESPONSE" | jq -r '.code // 99999')

if [ "$TOKEN_CODE" != "0" ] || [ -z "$TOKEN" ]; then
    echo "❌ 获取token失败: $TOKEN_RESPONSE"
    exit 1
fi

echo "✅ 成功获取tenant_access_token"

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

# 构建飞书消息内容
MESSAGE_CONTENT="📰 每日新闻推送\n\n📅 更新时间: $LAST_UPDATE\n\n$TITLE"

# 发送消息到飞书（使用你的用户ID）
RECEIVER_ID="ou_b3e9d506fffc28a72258bf51a107031d"

# 创建JSON文件避免引号问题
cat > /tmp/feishu_message.json << EOF
{
    "receive_id": "$RECEIVER_ID",
    "msg_type": "text",
    "content": "{\"text\":\"$MESSAGE_CONTENT\"}"
}
EOF

SEND_RESPONSE=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d @/tmp/feishu_message.json)

# 记录日志
LOG_FILE="/home/ubuntu/.openclaw/workspace/news-push-to-feishu.log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] App推送结果: $SEND_RESPONSE" >> "$LOG_FILE"

# 检查响应
SEND_CODE=$(echo "$SEND_RESPONSE" | jq -r '.code // 99999')
if [ "$SEND_CODE" == "0" ]; then
    echo "✅ 飞书推送成功！"
    echo "消息已发送到你的飞书账号"
else
    echo "❌ 飞书推送失败：$SEND_RESPONSE"
fi