#!/bin/bash
# 狗蛋导航系统前端停止脚本

echo "🐕 停止狗蛋导航系统前端服务..."
cd /home/ubuntu/.openclaw/workspace/web-navigation-system/frontend

if [ -f frontend.pid ]; then
    PID=$(cat frontend.pid)
    if ps -p $PID > /dev/null; then
        kill $PID
        echo "✅ 前端服务已停止 (PID: $PID)"
    else
        echo "⚠️  前端服务未运行"
    fi
    rm -f frontend.pid
else
    echo "⚠️  未找到前端PID文件"
fi