#!/bin/bash

# 发送消息到飞书的脚本
MESSAGE="$1"

# 使用OpenClaw的message工具
echo "$MESSAGE" | openclaw message send