#!/bin/bash

# 网站健康检测定时任务
# 每天凌晨2点执行

cd /home/ubuntu/.openclaw/workspace/web-navigation-system/backend

echo "=== 网站健康检测开始 $(date) ==="

# 检查后端服务是否运行
if ! curl -s http://localhost:5000/api/sites > /dev/null; then
    echo "后端服务未运行，启动服务..."
    nohup python3 app.py > app.log 2>&1 &
    sleep 5
fi

# 执行健康检测
python3 health_check.py

echo "=== 网站健康检测完成 $(date) ==="
