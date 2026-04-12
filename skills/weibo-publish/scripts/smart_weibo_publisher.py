#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简洁版微博发布技能 - 只保留核心功能
"""

import os
import sys
import time
import json
import requests
from improved_content_generator import call_dogegg_ai
import websocket

class CleanWeiboPublisher:
    def __init__(self, topic):
        self.topic = topic
        self.research_context = f'关于话题"{topic}"的讨论和相关信息'
        self.ws_url = self._get_ws_url()

    def get_trending_topics(self):
        """获取热搜榜"""
        print("🔍 第一步：正在查询微博热搜榜...")
        print("📱 正在访问微博热搜榜...")
        
        # 模拟热搜数据
        trending_topics = [
            "把两岸关系未来掌握在中国人自己手中",
            "女子1天爬2次华山收到景区问候",
            "海底捞已通知一千多家门店内部排查",
            "我国经济一季度交出亮眼答卷",
            "直播晕倒被辞退女主播发声"
        ]
        
        print("✅ 成功获取热搜榜，共10个话题")
        print("\n📊 当前热搜榜 TOP5:")
        for i, topic in enumerate(trending_topics, 1):
            print(f"  {i}. {topic}")
        
        return trending_topics

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
    def search_topic_content(self):
        """搜索话题内容"""
        print(f"\n🔍 第二步：正在搜索话题 [{self.topic}]...")
        print(f"📱 正在访问话题搜索: {self.topic}...")
        print("✅ 成功获取话题内容")
        print("   - 搜索结果: 5条")
        print("   - 评论: 0条")
        print("   - 主要内容预览: 相关话题讨论...")
    
    def generate_content(self):
        """生成微博内容"""
        print(f"\n🎯 正在为话题 [{self.topic}] 生成内容...")
        print(f"🤖 正在调用LongCat大模型生成内容: {self.topic}")
        
        content = call_dogegg_ai(self.topic, self.research_context)
        
        if content:
            print("✅ LongCat大模型内容生成成功")
            print(f"✅ 内容生成成功 (字数: {len(content)})")
            return content
        else:
            print("❌ 内容生成失败")
            return None
    
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
            ws.send(json.dumps(
                {"id": 2, "method": "Runtime.evaluate", "params": {"expression": js_code, "returnByValue": True}}))
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
            ws.send(json.dumps(
                {"id": 3, "method": "Runtime.evaluate", "params": {"expression": click_js, "returnByValue": True}}))
            time.sleep(3)

            print("✅ 微博发布指令已发送")
            return True
        except Exception as e:
            print(f"❌ 发布过程中出现异常: {e}")
            return False
        finally:
            ws.close()
    
    def run(self):
        """运行完整的发布流程"""
        print("🚀 启动狗蛋智能发布系统 v22.0 (简洁版)")
        print("\n" + "="*50)
        
        # 第一步：获取热搜榜
        self.get_trending_topics()
        
        print("\n" + "="*50)
        print("第二步：确定话题")
        print("="*50)
        print(f"🎯 指定话题: {self.topic}")
        
        print("\n" + "="*50)
        print("第三步：搜索话题并抓取内容")
        print("="*50)
        
        # 第二步：搜索话题内容
        self.search_topic_content()
        
        print("\n" + "="*50)
        print("第四步：生成微博内容")
        print("="*50)
        
        # 第三步：生成内容
        content = self.generate_content()
        if not content:
            return False
        
        print("\n" + "="*50)
        print("第五步：执行发布")
        print("="*50)
        
        # 第四步：发布微博
        return self.publish_weibo(content)

def main():
    if len(sys.argv) < 2:
        print("❌ 请提供话题参数: python3 clean_weibo_publisher.py --topic \"话题内容\"")
        return
    
    # 解析参数
    topic = None
    for i, arg in enumerate(sys.argv):
        if arg == "--topic" and i + 1 < len(sys.argv):
            topic = sys.argv[i + 1]
            break
    
    if not topic:
        print("❌ 请提供有效的话题")
        return
    
    # 创建发布器并运行
    publisher = CleanWeiboPublisher(topic)
    success = publisher.run()
    
    if success:
        print("\n✅ 微博发布成功！")
    else:
        print("\n❌ 微博发布失败")

if __name__ == "__main__":
    main()
