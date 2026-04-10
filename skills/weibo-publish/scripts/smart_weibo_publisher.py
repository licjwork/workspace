#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Weibo Publisher v21.0 - Autonomous Research Edition
Supports:
1. Auto hot search retrieval (if no topic provided)
2. Deep topic research (posts + comments) to inform AI generation
3. CDP-based browser automation for publishing
"""

import os
import sys
import time
import requests
import json
import websocket
from weibo_search_engine import WeiboSearchEngine
import improved_content_generator as generator

class SmartWeiboPublisher:
    def __init__(self, port=18800):
        self.port = port
        self.search_engine = WeiboSearchEngine(port)
        self.ws_url = self._get_ws_url()

    def _get_ws_url(self):
        try:
            response = requests.get(f'http://localhost:{self.port}/json/list', timeout=5)
            pages = response.json()
            if not pages:
                return None
            return pages[0]['webSocketDebuggerUrl']
        except Exception as e:
            print(f"❌ 无法连接到浏览器调试端口: {e}")
            return None

    def generate_content(self, topic):
        """调研话题并生成深度微博内容"""
        # 1. 对话题进行深度调研 (获取实时博文和评论背景)
        research_context = self.search_engine.get_topic_research(topic)
        
        # 2. 调用生成引擎生成文案
        content = generator.call_dogegg_ai(topic, research_context)
        return content

    def publish_weibo(self, content):
        """使用 CDP 直接发布到微博"""
        ws_url = self._get_ws_url()
        if not ws_url:
            print("❌ 浏览器 WebSocket 未就绪")
            return False

        print("🚀 正在准备发布到微博...")
        ws = websocket.create_connection(ws_url, timeout=20)
        try:
            # 确保在发布页面
            ws.send(json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": "https://m.weibo.cn/compose"}}))
            time.sleep(5)

            # 输入文案
            # 转义引号以防 JS 报错
            safe_content = content.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            js_code = f"""
            (function() {{
                var area = document.querySelector('textarea[placeholder*="分享新鲜事"]');
                if (area) {{
                    area.value = "{safe_content}";
                    area.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    return true;
                }}
                return false;
            }})()
            """
            ws.send(json.dumps({"id": 2, "method": "Runtime.evaluate", "params": {"expression": js_code, "returnByValue": True}}))
            time.sleep(2)

            # 点击发送
            click_js = """
            (function() {
                var btn = document.querySelector('a.m-send-btn');
                if (btn && !btn.classList.contains('disabled')) {
                    btn.click();
                    return true;
                }
                return false;
            })()
            """
            ws.send(json.dumps({"id": 3, "method": "Runtime.evaluate", "params": {"expression": click_js, "returnByValue": True}}))
            time.sleep(3)
            
            print("✅ 微博发布指令已发送")
            return True
        except Exception as e:
            print(f"❌ 发布过程中出现异常: {e}")
            return False
        finally:
            ws.close()

    def run(self, topic=None, preview=False):
        """执行全自动发布流程"""
        print("🚀 启动狗蛋智能发布系统 v21.0")
        
        # 1. 自动选题逻辑
        if not topic:
            print("💡 未指定话题，正在自动检索微博热搜榜首...")
            topic = self.search_engine.get_top_hot_search()
            if not topic:
                print("❌ 无法获取热搜话题")
                return
        
        # 2. 调研并生成内容
        content = self.generate_content(topic)
        if not content:
            print("❌ 生成内容失败")
            return

        if preview:
            print(f"\n--- [预览模式] 微博内容 ({topic}) ---")
            print(content)
            print("-" * 35)
            print(f"字数统计: {len(content)}")
        else:
            # 3. 执行发布
            success = self.publish_weibo(content)
            if success:
                print(f"🎉 话题 [{topic}] 发布流程已完成")
            else:
                print(f"⚠️ 话题 [{topic}] 发布失败")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Smart Weibo Publisher v21.0')
    parser.add_argument('--topic', type=str, help='微博话题 (不填则自动抓取热搜)')
    parser.add_argument('--preview', action='store_true', help='仅预览不发布')
    args = parser.parse_args()

    publisher = SmartWeiboPublisher()
    publisher.run(topic=args.topic, preview=args.preview)
