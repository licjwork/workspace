#!/bin/bash
# OpenClaw定时任务部署脚本

echo "🐕 部署OpenClaw定时任务平替方案..."

# 1. 创建必要的目录
mkdir -p /home/ubuntu/.openclaw/workspace/backups
mkdir -p /home/ubuntu/.openclaw/workspace/memory

# 2. 给脚本添加执行权限
chmod +x /home/ubuntu/.openclaw/workspace/scripts/*.py
chmod +x /home/ubuntu/.openclaw/workspace/scripts/deploy_cron.sh

# 3. 备份原有crontab
echo "备份原有crontab..."
crontab -l > /home/ubuntu/.openclaw/workspace/backups/crontab_backup_$(date +%Y%m%d_%H%M%S).txt

# 4. 移除原有定时任务
echo "移除原有定时任务..."
crontab -l | grep -v "intelligent_news_final.py" | crontab -

# 5. 配置OpenClaw heartbeat
echo "配置OpenClaw heartbeat..."
cat > /home/ubuntu/.openclaw/workspace/HEARTBEAT.md << 'EOF'
# OpenClaw定时任务管理

## 每日智能新闻推送
- **任务**: 每天8:00执行智能新闻搜索和翻译
- **触发条件**: 检测到当前时间是8:00-8:30之间且未执行今日任务
- **执行**: 运行智能新闻脚本并推送结果

## 服务状态监控
- **任务**: 每小时检查导航系统服务状态
- **触发条件**: 每整点执行一次
- **执行**: 检查前后端服务运行状态，异常时自动重启

## 数据库备份
- **任务**: 每天23:00备份数据库
- **触发条件**: 23:00-23:30之间
- **执行**: 备份SQLite数据库到指定目录
EOF

# 6. 创建测试任务
echo "创建测试任务..."
echo "0 8 * * * python3 /home/ubuntu/.openclaw/workspace/scripts/task_scheduler.py" | crontab -

# 7. 验证部署
echo "验证部署..."
echo "当前crontab:"
crontab -l

echo ""
echo "✅ OpenClaw定时任务平替方案部署完成！"
echo "📋 可用方案:"
echo "   1. Heartbeat模式: 编辑 HEARTBEAT.md"
echo "   2. Cron模式: 使用 task_scheduler.py"
echo "   3. 原生集成: 使用 openclaw_integration.py"
echo ""
echo "🐕 狗蛋定时任务系统已就绪！"