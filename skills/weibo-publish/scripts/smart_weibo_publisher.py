#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复版智能微博发布器 - 正确版本
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
        """发布微博内容"""
        print("🚀 正在发布微博...")
        
        try:
            # 获取WebSocket URL
            response = requests.get(f'http://localhost:{self.browser_port}/json/list')
            page_info = response.json()[0]
            ws_url = page_info['webSocketDebuggerUrl']
            
            # 建立连接
            ws = websocket.create_connection(ws_url)
            
            # 1. 输入内容 - 使用简单直接的JavaScript
            # 转义内容中的引号和特殊字符
            escaped_content = content.replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
            
            input_js = f'''
                (function() {{
                    var textarea = document.querySelector('textarea[placeholder*="分享新鲜事"]');
                    if (textarea) {{
                        textarea.value = "{escaped_content}";
                        textarea.dispatchEvent(new Event('input', {{bubbles: true}}));
                        return textarea.value.length > 0;
                    }}
                    return false;
                }})();
            '''
            
            input_message = {
                'id': 1,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': input_js,
                    'returnByValue': True
                }
            }
            
            ws.send(json.dumps(input_message))
            input_result = ws.recv()
            input_data = json.loads(input_result)
            
            # 调试信息
            print(f"输入响应: {input_data}")
            
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
            
            # 调试信息
            print(f"发布响应: {publish_data}")
            
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
    
    def run(self, topic="今日热点"):
        """运行微博发布"""
        print("🚀 启动微博发布系统")
        
        # 检查服务
        if not self.check_services():
            return False
        
        # 生成内容
        content = self.generate_content(topic)
        print(f"\n📝 生成的内容:\n{content}")
        
        # 发布微博
        success = self.publish_weibo(content)
        
        if success:
            print("\n🎉 微博发布完成！")
            print("✅ 发布成功")
            return True
        else:
            print("\n❌ 微博发布失败")
            return False

if __name__ == "__main__":
    import sys
    
    topic = "今日热点"
    if len(sys.argv) > 1:
        topic = sys.argv[1]
    
    publisher = WeiboPublisher()
    publisher.run(topic)
