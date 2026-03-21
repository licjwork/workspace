#!/bin/bash

# 自动国际最新新闻 + 飞书推送脚本
# 使用OpenClaw的心跳检测机制实现自动推送

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 国际最新新闻推送开始"

# 执行中国科技新闻脚本
/home/ubuntu/.openclaw/workspace/auto-weibo-format.sh

# 检查新闻文件
NEWS_FILE="/home/ubuntu/.openclaw/workspace/news.json"
if [ -f "$NEWS_FILE" ]; then
    # 读取新闻内容
    NEWS_CONTENT=$(cat "$NEWS_FILE")
    TITLE=$(echo "$NEWS_CONTENT" | jq -r '.content // "今日中国科技新闻摘要"')
    LAST_UPDATE=$(echo "$NEWS_CONTENT" | jq -r '.last_update // "未知时间"')
    
    # 构建消息
    MESSAGE="📰 中国科技新闻推送\n\n📅 更新时间: $LAST_UPDATE\n\n$TITLE"
    
    # 使用OpenClaw的message工具发送消息
    # 通过OpenClaw CLI直接发送飞书消息
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始发送飞书推送..."
    
    # 调用OpenClaw message命令发送消息
    openclaw message send --channel feishu --target user:ou_b3e9d506fffc28a72258bf51a107031d --message "$MESSAGE" 2>&1
    
    # 检查发送结果
    if [ $? -eq 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 飞书推送成功"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ 飞书推送失败，尝试备用方式"
        
        # 备用方式：记录消息内容，供手动发送
        echo "消息内容：$MESSAGE" > /tmp/feishu_message_backup.txt
        echo "请手动执行：openclaw message send --channel feishu --target user:ou_b3e9d506fffc28a72258bf51a107031d --message \"$MESSAGE\""
    fi
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 中国科技新闻推送完成"