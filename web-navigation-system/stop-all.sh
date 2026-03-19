#!/bin/bash
# 狗蛋导航系统完整停止脚本

echo "🐕 停止狗蛋导航系统全部服务..."

# 停止前端
./stop-frontend.sh

# 停止后端
./stop-backend.sh

echo "✅ 所有服务已停止！"