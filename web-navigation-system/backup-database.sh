#!/bin/bash

# 数据库备份脚本
echo "🐕 开始备份狗蛋导航系统数据库..."

# 备份目录
BACKUP_DIR="/home/ubuntu/.openclaw/workspace/web-navigation-system/database/backup"
mkdir -p $BACKUP_DIR

# 源数据库文件
SOURCE_DB="/home/ubuntu/.openclaw/workspace/web-navigation-system/backend/database/navigation.db"

# 备份文件名（带时间戳）
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/navigation_backup_${TIMESTAMP}.db"

# 执行备份
if [ -f "$SOURCE_DB" ]; then
    cp "$SOURCE_DB" "$BACKUP_FILE"
    echo "✅ 数据库备份成功"
    echo "📁 备份文件: $BACKUP_FILE"
    echo "📊 文件大小: $(du -h "$BACKUP_FILE" | cut -f1)"
    
    # 清理7天前的备份文件
    find "$BACKUP_DIR" -name "navigation_backup_*.db" -mtime +7 -delete
    echo "🗑️  已清理7天前的旧备份"
else
    echo "❌ 源数据库文件不存在: $SOURCE_DB"
    exit 1
fi

echo "✅ 数据库备份任务完成"