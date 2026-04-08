#!/bin/bash
# 社交媒体发布脚本
# 创建时间：2026-03-29
# 用途：自动化发布微博和小红书内容

echo "=== 社交媒体发布脚本 ==="
echo "开始时间：$(date)"

# 检查必要文件
if [ ! -f "/home/ubuntu/.openclaw/workspace/微博内容.md" ]; then
    echo "❌ 微博内容文件不存在"
    exit 1
fi

if [ ! -f "/home/ubuntu/.openclaw/workspace/小红书内容.md" ]; then
    echo "❌ 小红书内容文件不存在"
    exit 1
fi

# 检查上传目录
if [ ! -d "/tmp/openclaw/uploads" ]; then
    echo "❌ 上传目录不存在，创建中..."
    mkdir -p /tmp/openclaw/uploads
fi

# 检查图片资源
image_count=$(ls /tmp/openclaw/uploads/*.jpg 2>/dev/null | wc -l)
echo "📁 找到 $image_count 张图片用于发布"

# 小红书发布流程
echo "\n=== 小红书发布流程 ==="
echo "1. 启动浏览器"
echo "2. 导航到小红书发布页面"
echo "3. 上传图片并填写内容"
echo "4. 发布笔记"

# 微博发布流程
echo "\n=== 微博发布流程 ==="
echo "1. 启动浏览器"
echo "2. 导航到微博发布页面"
echo "3. 填写内容并发布"
echo "4. 添加相关话题标签"

echo "\n=== 发布准备完成 ==="
echo "请确保："
echo "- 浏览器工具正常工作"
echo "- 已登录相关账号"
echo "- 图片资源准备就绪"
echo "\n开始时间：$(date)"