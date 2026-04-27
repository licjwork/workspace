#!/bin/bash
# 微博发布技能2 (长期会话版)

# 确保在脚本所在目录
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# 检查是否提供了话题
if [ -z "$1" ]; then
    echo "❌ 错误: 请提供微博话题"
    echo "用法: ./weibo-persistent.sh \"话题内容\""
    exit 1
fi

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "🔄 正在初始化虚拟环境..."
    python3 -m venv venv
    ./venv/bin/pip install -r requirements.txt
fi

# 运行发布脚本
echo "🚀 正在启动微博发布流程: $1"
./venv/bin/python3 scripts/__init__.py "$1" --persistent
