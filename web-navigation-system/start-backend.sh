#!/bin/bash
# 狗蛋导航系统后端后台启动脚本

echo "🐕 启动狗蛋导航系统后端服务..."
cd /home/ubuntu/.openclaw/workspace/web-navigation-system/backend

# 激活虚拟环境
source venv/bin/activate

# 后台启动后端服务
nohup python run.py > backend.log 2>&1 &
echo $! > backend.pid

echo "✅ 后端服务已启动 (PID: $(cat backend.pid))"
echo "📝 日志文件: backend.log"
echo "🌐 API地址: http://localhost:5000"