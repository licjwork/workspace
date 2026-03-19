#!/bin/bash
# 狗蛋导航系统完整后台启动脚本

echo "🐕 启动狗蛋导航系统全部服务..."

# 启动后端
./start-backend.sh
sleep 3

# 启动前端
./start-frontend.sh
sleep 3

echo "✅ 所有服务已启动完成！"
echo "🌐 前端访问: http://82.156.52.192:8017"
echo "🌐 后端API: http://localhost:5000"
echo "📊 使用 ./status.sh 查看服务状态"