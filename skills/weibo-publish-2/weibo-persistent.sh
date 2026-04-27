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

# Linux 环境下的 VNC 处理
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 检测到 Linux 环境，正在检查 VNC 状态..."
    
    # 检查 VNC 是否已经在运行
    if ! ps aux | grep -v grep | grep -q "vncserver :1"; then
        echo "🖥️  正在启动 VNC 服务器 (:1)..."
        vncserver :1 -geometry 1280x800 -depth 24
        xhost +
    else
        echo "✅ VNC 服务器已经在运行"
    fi
    
    # 设置 DISPLAY 变量
    export DISPLAY=:1
fi

# 运行发布脚本
echo "🚀 正在启动微博发布流程: $1"
./venv/bin/python3 scripts/__init__.py "$1" --persistent
