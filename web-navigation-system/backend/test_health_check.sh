#!/bin/bash

# 网站健康检测测试脚本
# 检测前10个网站，避免超时

echo "=== 网站健康检测测试开始 $(date) ==="

cd /home/ubuntu/.openclaw/workspace/web-navigation-system/backend

# 检测前10个网站
for i in {1..10}; do
    echo "检测网站 $i..."
    response=$(curl -s http://localhost:5000/api/sites/$i/health)
    if echo "$response" | grep -q "healthy"; then
        status=$(echo "$response" | grep -o '"health_status":"[^"]*"' | cut -d'"' -f4)
        time=$(echo "$response" | grep -o '"response_time":[0-9]*' | cut -d':' -f2)
        echo "✅ 网站$i: $status (${time}ms)"
    else
        echo "❌ 网站$i: 检测失败"
    fi
    sleep 1  # 避免过快请求

done

echo "=== 网站健康检测测试完成 $(date) ==="
