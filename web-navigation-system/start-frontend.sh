#!/bin/bash
# 狗蛋导航系统前端后台启动脚本

echo "🐕 启动狗蛋导航系统前端服务..."
cd /home/ubuntu/.openclaw/workspace/web-navigation-system/frontend

# 后台启动前端服务
nohup npm start > frontend.log 2>&1 &
echo $! > frontend.pid

echo "✅ 前端服务已启动 (PID: $(cat frontend.pid))"
echo "📝 日志文件: frontend.log"
echo "🌐 访问地址: http://82.156.52.192:8017"