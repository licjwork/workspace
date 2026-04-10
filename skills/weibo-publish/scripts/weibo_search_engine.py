#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import websocket
import json
import time

class WeiboSearchEngine:
    def __init__(self, port=18800):
        self.port = port
        self.ws_url = self._get_ws_url()

    def _get_ws_url(self):
        try:
            response = requests.get(f'http://localhost:{self.port}/json/list', timeout=5)
            pages = response.json()
            # 优先找一个空白页或者 compose 页，如果没有就新建一个或者用第一个
            return pages[0]['webSocketDebuggerUrl']
        except Exception as e:
            print(f"❌ 无法连接到浏览器调试端口: {e}")
            return None

    def _execute_js(self, js_code, ws):
        try:
            msg = {
                "id": round(time.time() * 1000),
                "method": "Runtime.evaluate",
                "params": {"expression": js_code, "returnByValue": True}
            }
            ws.send(json.dumps(msg))
            result = json.loads(ws.recv())
            return result.get('result', {}).get('result', {}).get('value')
        except Exception as e:
            print(f"❌ JS 执行失败: {e}")
            return None

    def get_top_hot_search(self):
        """获取当前微博热搜榜首话题"""
        if not self.ws_url: return None
        print("🕒 正在前往微博热搜榜...")
        
        ws = websocket.create_connection(self.ws_url, timeout=15)
        try:
            # 导航到搜索入口或热搜聚合页
            ws.send(json.dumps({"id": 1, "method": "Page.navigate", "params": {"url": "https://m.weibo.cn/search"}}))
            time.sleep(5) 
            
            # 在搜索页直接抓取带有“热”字样的话题或第一个列表项
            js_code = """
            (function() {
                // 尝试多个可能的选择器
                var selectors = [
                    '.main-text',  // 搜索首页的热搜列表项
                    '.card-main .p-main', // 专题页
                    '.card-item .main-text', // 列表页
                    '.card8 .alt' // 备选
                ];
                for (var s of selectors) {
                    var items = document.querySelectorAll(s);
                    if (items.length > 0) {
                        var topic = items[0].innerText.trim().split('\\n')[0];
                        if (topic && topic !== '大家都在搜' && topic !== '微博热搜') return topic;
                    }
                }
                // 最后手段：直接抓取 body 里的第一个看起来像话题的词
                var bodyText = document.body.innerText;
                var match = bodyText.match(/#([^#]+)#/);
                if (match) return match[1];
                return null;
            })()
            """
            topic = self._execute_js(js_code, ws)
            if topic:
                print(f"✅ 成功抓取当前热度话题: {topic}")
                return topic
            return "今日热议话题"
        except Exception as e:
            print(f"⚠️ 抓取热搜数据失败: {e}")
            return "今日热议话题"
        finally:
            ws.close()

    def get_topic_research(self, topic):
        """调研特定话题，获取博文和评论作为背景"""
        if not self.ws_url: return None
        print(f"🕵️ 正在对微博实时动态进行深度调研: [{topic}]...")
        
        ws = websocket.create_connection(self.ws_url, timeout=20)
        try:
            # 使用 containerid 构建最直接的搜索结果页
            search_url = f"https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D{topic}"
            ws.send(json.dumps({"id": 2, "method": "Page.navigate", "params": {"url": search_url}}))
            time.sleep(6) # 搜索页加载较慢
            
            js_code = """
            (function() {
                var results = { posts: [] };
                // 兼容多种博文容器
                var posts = document.querySelectorAll('.card9 .weibo-text, .card9 .content, .weibo-main .weibo-text');
                for (var i = 0; i < Math.min(posts.length, 3); i++) {
                    var t = posts[i].innerText.trim();
                    if (t.length > 20) results.posts.push(t.substring(0, 150) + "...");
                }
                return results;
            })()
            """
            data = self._execute_js(js_code, ws)
            if data and data.get('posts') and len(data['posts']) > 0:
                print(f"✅ 调研情报获取成功 ({len(data['posts'])}条)")
                context = "\n".join([f"- 实况记录: {p}" for p in data['posts']])
                return context
            
            print("⚠️ 未能从搜索结果中提取到有效文本")
            return ""
        except Exception as e:
            print(f"⚠️ 调研中断: {e}")
            return ""
        finally:
            ws.close()

if __name__ == "__main__":
    engine = WeiboSearchEngine()
    print("Test Hot Search:", engine.get_top_hot_search())
    print("Test Research:", engine.get_topic_research("人工智能"))
