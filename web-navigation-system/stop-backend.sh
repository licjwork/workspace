#!/bin/bash
# 狗蛋导航系统后端停止脚本

echo "🐕 停止狗蛋导航系统后端服务..."
cd /home/ubuntu/.openclaw/workspace/web-navigation-system/backend

if [ -f backend.pid ]; then
    PID=$(cat backend.pid)
    if ps -p $PID > /dev/null; then
        kill $PID
        echo "✅ 后端服务已停止 (PID: $PID)"
    else
        echo "⚠️  后端服务未运行"
    fi
    rm -f backend.pid
else
    echo "⚠️  未找到后端PID文件"
fi