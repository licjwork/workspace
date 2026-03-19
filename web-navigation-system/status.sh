#!/bin/bash
# 狗蛋导航系统服务状态检查脚本

echo "🐕 检查狗蛋导航系统服务状态..."

# 检查后端服务
cd /home/ubuntu/.openclaw/workspace/web-navigation-system/backend
if [ -f backend.pid ]; then
    PID=$(cat backend.pid)
    if ps -p $PID > /dev/null; then
        echo "✅ 后端服务: 运行中 (PID: $PID)"
    else
        echo "❌ 后端服务: 已停止"
        rm -f backend.pid
    fi
else
    echo "❌ 后端服务: 未启动"
fi

# 检查前端服务
cd /home/ubuntu/.openclaw/workspace/web-navigation-system/frontend
if [ -f frontend.pid ]; then
    PID=$(cat frontend.pid)
    if ps -p $PID > /dev/null; then
        echo "✅ 前端服务: 运行中 (PID: $PID)"
    else
        echo "❌ 前端服务: 已停止"
        rm -f frontend.pid
    fi
else
    echo "❌ 前端服务: 未启动"
fi

# 检查端口占用情况
echo ""
echo "🌐 端口占用检查:"
if netstat -tulpn 2>/dev/null | grep :5000 > /dev/null; then
    echo "✅ 端口5000: 被占用 (后端服务)"
else
    echo "❌ 端口5000: 空闲"
fi

if netstat -tulpn 2>/dev/null | grep :8017 > /dev/null; then
    echo "✅ 端口8017: 被占用 (前端服务)"
else
    echo "❌ 端口8017: 空闲"
fi