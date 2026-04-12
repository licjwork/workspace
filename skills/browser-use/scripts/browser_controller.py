#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用浏览器控制器 - 基于 CDP 协议
参考微博发布技能实现
"""

import sys
import time
import json
import argparse
import requests
import websocket

class BrowserController:
    def __init__(self, port=18800):
        self.port = port
        self.ws_url = self._get_ws_url()

    def _get_ws_url(self):
        """获取浏览器的 WebSocket 调试地址"""
        try:
            response = requests.get(f'http://localhost:{self.port}/json/list', timeout=5)
            pages = response.json()
            if not pages:
                print("❌ 浏览器中没有打开的页面")
                return None
            # 优先选择当前激活或第一个页面
            return pages[0]['webSocketDebuggerUrl']
        except Exception as e:
            print(f"❌ 无法连接到浏览器调试端口 {self.port}: {e}")
            return None

    def _send_command(self, method, params=None):
        """通过 WebSocket 发送 CDP 命令"""
        if not self.ws_url:
            print("❌ WebSocket URL 未就绪")
            return None

        ws = websocket.create_connection(self.ws_url, timeout=20)
        try:
            msg_id = int(time.time() * 1000)
            message = {
                "id": msg_id,
                "method": method,
                "params": params or {}
            }
            ws.send(json.dumps(message))
            
            # 循环读取直到获取到匹配的 ID
            while True:
                response = ws.recv()
                data = json.loads(response)
                if data.get('id') == msg_id:
                    return data
                # 如果是事件或者不相关的响应，继续监听
        except Exception as e:
            print(f"❌ 命令执行失败 ({method}): {e}")
            return None
        finally:
            ws.close()

    def navigate(self, url):
        """导航到指定 URL"""
        print(f"🌐 正在导航到: {url}")
        result = self._send_command("Page.navigate", {"url": url})
        # 等待页面加载
        time.sleep(5)
        return result

    def scrape(self, html=False):
        """抓取页面内容"""
        print("📄 正在提取页面内容...")
        js_code = "document.documentElement.outerHTML" if html else "document.body.innerText"
        result = self.evaluate(js_code)
        if result and 'result' in result and 'result' in result['result']:
            return result['result']['result'].get('value', '')
        return ""

    def evaluate(self, js_code):
        """在页面中执行 JS"""
        return self._send_command("Runtime.evaluate", {
            "expression": js_code,
            "returnByValue": True
        })

    def click(self, selector):
        """点击指定元素"""
        print(f"🖱️ 正在点击元素: {selector}")
        js_code = f"""
        (function() {{
            var el = document.querySelector("{selector}");
            if (el) {{
                el.click();
                return true;
            }}
            return false;
        }})()
        """
        result = self.evaluate(js_code)
        if result and 'result' in result and 'result' in result['result']:
            success = result['result']['result'].get('value', False)
            if success:
                print("✅ 点击成功")
                return True
        print("❌ 未能点击该元素，请检查选择器或页面状态")
        return False

    def type_text(self, selector, text):
        """在指定输入框中输入文本"""
        print(f"⌨️ 正在输入文本到: {selector}")
        # 转义文本以防止 JS 报错
        safe_text = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        js_code = f"""
        (function() {{
            var el = document.querySelector("{selector}");
            if (el) {{
                el.value = "{safe_text}";
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return true;
            }}
            return false;
        }})()
        """
        result = self.evaluate(js_code)
        if result and 'result' in result and 'result' in result['result']:
            success = result['result']['result'].get('value', False)
            if success:
                print("✅ 输入成功")
                return True
        print("❌ 未能输入文本，请检查选择器或页面状态")
        return False

def main():
    parser = argparse.ArgumentParser(description='通用浏览器控制器')
    parser.add_argument('--action', required=True, choices=['navigate', 'scrape', 'click', 'type', 'evaluate'], help='执行动作')
    parser.add_argument('--url', help='目标 URL')
    parser.add_argument('--selector', help='CSS 选择器')
    parser.add_argument('--text', help='输入的文本')
    parser.add_argument('--js', help='要执行的 JavaScript 代码')
    parser.add_argument('--html', action='store_true', help='scrape 时是否返回 HTML')
    parser.add_argument('--port', type=int, default=18800, help='CDP 端口')

    args = parser.parse_args()
    controller = BrowserController(port=args.port)

    if args.url and args.action != 'evaluate':
        controller.navigate(args.url)

    if args.action == 'navigate':
        print("✅ 导航完成")
    
    elif args.action == 'scrape':
        content = controller.scrape(html=args.html)
        print("\n--- 抓取内容摘要 ---")
        print(content[:500] + ("..." if len(content) > 500 else ""))
        print("------------------")
    
    elif args.action == 'click':
        if not args.selector:
            print("❌ 请提供 --selector")
        else:
            controller.click(args.selector)
    
    elif args.action == 'type':
        if not args.selector or not args.text:
            print("❌ 请提供 --selector 和 --text")
        else:
            controller.type_text(args.selector, args.text)
    
    elif args.action == 'evaluate':
        if not args.js:
            print("❌ 请提供 --js")
        else:
            result = controller.evaluate(args.js)
            print(f"✅ 执行结果: {json.dumps(result, indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    main()
