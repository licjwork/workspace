#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终修复版智能微博发布器
"""

import os
import sys
import time
import subprocess
import requests
import json
import websocket
from improved_content_generator import call_dogegg_ai

class WeiboPublisher:
    def __init__(self):
        self.browser_port = 18800
    
    def check_services(self):
        """检查服务状态"""
        print("🔍 检查服务状态...")
        try:
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            vnc_ok = 'vnc' in result.stdout
            browser_ok = 'chromium' in result.stdout
            
            if vnc_ok and browser_ok:
                print("✅ VNC和浏览器服务正常")
                return True
            else:
                print("❌ 服务检查失败")
                return False
        except Exception as e:
            print(f"❌ 服务检查错误: {e}")
            return False
    
    def generate_content(self, topic="今日热点"):
        """生成微博内容"""
        print(f"🎯 使用改进的AI系统生成话题内容: {topic}")
        
        content = call_dogegg_ai(topic)
        
        if content:
            print("✅ 高质量内容生成成功")
            return content
        else:
            print("⚠️ AI生成失败，使用应急兜底内容")
            return f"🔥 # {topic} # ：深度见解正在路上的狗蛋狗狗🐕建议大家保持关注！ #今日热点"
    
    def publish_weibo(self, content):
        """发布微博"""
        print("🚀 正在发布微博...")
        
        try:
            # 获取浏览器连接
            response = requests.get(f'http://localhost:{self.browser_port}/json/list', timeout=5)
            page_info = response.json()[0]
            ws_url = page_info['webSocketDebuggerUrl']
            
            ws = websocket.create_connection(ws_url, timeout=10)
            
            # 分步执行：先输入内容，再发布
            
            # 1. 输入内容到文本框
            input_js = '''
                (function() {
                    var textarea = document.querySelector('textarea[placeholder=\"分享新鲜事…\"]');
                    if (textarea) {
                        textarea.value = arguments[0];
                        textarea.dispatchEvent(new Event('input', {bubbles: true}));
                        return true;
                    }
                    return false;
                })();
            '''
            
            input_message = {
                'id': 1,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': input_js,
                    'arguments': [{'type': 'string', 'value': content}],
                    'returnByValue': True
                }
            }
            
            ws.send(json.dumps(input_message))
            input_result = ws.recv()
            input_data = json.loads(input_result)
            input_success = input_data.get('result', {}).get('result', {}).get('value', False)
            
            if not input_success:
                print("❌ 内容输入失败")
                ws.close()
                return False
            
            print("✅ 内容输入成功")
            
            # 2. 等待一下，然后点击发布按钮
            time.sleep(2)
            
            publish_js = '''
                (function() {
                    var sendBtn = document.querySelector('a.m-send-btn');
                    if (sendBtn && !sendBtn.classList.contains('disabled')) {
                        sendBtn.click();
                        return true;
                    }
                    return false;
                })();
            '''
            
            publish_message = {
                'id': 2,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': publish_js,
                    'returnByValue': True
                }
            }
            
            ws.send(json.dumps(publish_message))
            publish_result = ws.recv()
            publish_data = json.loads(publish_result)
            publish_success = publish_data.get('result', {}).get('result', {}).get('value', False)
            
            ws.close()
            
            if publish_success:
                print("✅ 微博发布成功！")
                return True
            else:
                print("❌ 发布按钮点击失败")
                return False
                
        except Exception as e:
            print(f"❌ 发布过程出错: {e}")
            return False
    
    def run(self, topic=None, preview=False):
        """运行发布流程"""
        print("🚀 启动微博发布系统")
        
        # 处理话题
        if not topic:
            topic = "今日热点"
        
        # 预览模式下跳过服务检查
        if not preview:
            # 检查服务
            if not self.check_services():
                return False
        
        # 生成内容
        content = self.generate_content(topic)
        print(f"\n📝 生成的内容:\n{content}")
        
        if preview:
            print("\n👀 预览模式：内容已生成，跳过发布步骤。")
            return True
        
        # 发布微博
        success = self.publish_weibo(content)
        
        if success:
            print("\n🎉 微博发布完成！")
            return True
        else:
            print("\n❌ 微博发布失败")
            return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='微博发布器')
    parser.add_argument('--topic', type=str, help='指定话题')
    parser.add_argument('--preview', action='store_true', help='预览模式，仅生成不发布')
    
    args = parser.parse_args()
    
    publisher = WeiboPublisher()
    success = publisher.run(args.topic, args.preview)
    
    if success:
        print("✅ 发布成功")
        sys.exit(0)
    else:
        print("❌ 发布失败")
        sys.exit(1)
