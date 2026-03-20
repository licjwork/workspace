#!/bin/bash

# 自动推送工作空间到GitHub
# 每天凌晨1点执行

set -e

WORKSPACE_DIR="/home/ubuntu/.openclaw/workspace"
LOG_FILE="/home/ubuntu/.openclaw/workspace/git-push.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始自动推送" >> "$LOG_FILE"

# 进入工作空间目录
cd "$WORKSPACE_DIR"

# 检查是否有修改需要提交
if [[ -n $(git status --porcelain) ]]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检测到代码修改" >> "$LOG_FILE"
    
    # 添加所有修改
    git add -A
    
    # 提交修改
    git commit -m "自动推送: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE" 2>&1
    
    # 推送到GitHub
    git push origin master >> "$LOG_FILE" 2>&1
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 代码推送成功" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 无代码修改需要推送" >> "$LOG_FILE"
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 自动推送完成" >> "$LOG_FILE"
