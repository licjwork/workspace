#!/usr/bin/env python3
"""
修复数据库路径脚本
"""

import os

# 读取原始文件
with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换所有数据库路径
content = content.replace("sqlite3.connect('database/navigation.db')", 
                         "sqlite3.connect('/home/ubuntu/.openclaw/workspace/web-navigation-system/database/navigation.db')")

# 写回文件
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("数据库路径修复完成")