#!/usr/bin/env python3
# 修复集成发布器，使用移动端发布方法
import sys
import subprocess
import argparse

# 直接使用移动端发布器
def run_mobile_publish(topic):
    print(f"🚀 使用移动端发布器发布: {topic}")
    
    cmd = [
        'python3', 
        '/home/ubuntu/.openclaw/workspace/skills/weibo-publish-2/scripts/stable_publisher.py',
        topic
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        print(result.stdout)
        if result.stderr:
            print("错误输出:", result.stderr)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ 发布超时")
        return False
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', type=str, required=True, help='微博话题')
    args = parser.parse_args()
    
    success = run_mobile_publish(args.topic)
    print(f"\n发布结果: {'✅ 成功' if success else '❌ 失败'}")
