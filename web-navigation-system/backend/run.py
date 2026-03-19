#!/usr/bin/env python3
"""
后端服务启动脚本
"""

from app import app

if __name__ == '__main__':
    print("🐕 狗蛋导航系统后端服务启动中...")
    print("📊 API地址: http://localhost:5000")
    print("🔧 调试模式: 开启")
    app.run(debug=True, port=5000, host='0.0.0.0')