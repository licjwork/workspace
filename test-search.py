#!/usr/bin/env python3

import subprocess
import json
import time

# 测试搜索功能
print("开始测试微博热搜搜索...")

try:
    # 执行搜索
    result = subprocess.run([
        'python3', 'skills/tavily/scripts/tavily_search.py', 
        '微博热搜', 
        '--api-key', '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', 
        '--topic', 'news', 
        '--max-results', '5'
    ], capture_output=True, text=True, timeout=60)
    
    print(f"返回码: {result.returncode}")
    print(f"标准输出: {result.stdout}")
    print(f"标准错误: {result.stderr}")
    
    if result.returncode == 0:
        print("搜索成功!")
        # 尝试解析结果
        lines = result.stdout.strip().split('\n')
        for i, line in enumerate(lines):
            print(f"行{i+1}: {line}")
    else:
        print("搜索失败!")
        
except Exception as e:
    print(f"执行错误: {e}")