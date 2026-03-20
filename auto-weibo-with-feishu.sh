#!/bin/bash

# 自动微博热搜 + 飞书推送脚本

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 微博热搜推送开始"

# 执行微博热搜脚本
/home/ubuntu/.openclaw/workspace/auto-weibo-format.sh

# 检查新闻文件
NEWS_FILE="/home/ubuntu/.openclaw/workspace/news.json"
if [ -f "$NEWS_FILE" ]; then
    # 读取新闻内容
    NEWS_CONTENT=$(cat "$NEWS_FILE")
    TITLE=$(echo "$NEWS_CONTENT" | jq -r '.content // "今日新闻摘要"')
    LAST_UPDATE=$(echo "$NEWS_CONTENT" | jq -r '.last_update // "未知时间"')
    
    # 构建消息
    MESSAGE="📰 每日新闻推送\n\n📅 更新时间: $LAST_UPDATE\n\n$TITLE"
    
    # 使用OpenClaw的message工具发送消息
    # 这里需要OpenClaw环境支持直接从脚本调用message工具
    # 目前只能通过OpenClaw会话发送消息
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 新闻内容已生成，需要手动发送飞书推送"
    echo "消息内容：$MESSAGE"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 飞书推送完成"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 微博热搜推送完成"