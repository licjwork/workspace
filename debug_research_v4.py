import json
import requests
import websocket
import time

def debug_weibo_research_v4(topic):
    """调试微博调研功能 - 版本4，尝试获取微博正文"""
    print(f"🔍 调试微博调研V4: {topic}")
    
    try:
        response = requests.get('http://localhost:18800/json/list')
        page_info = response.json()[0]
        ws_url = page_info['webSocketDebuggerUrl']
        
        ws = websocket.create_connection(ws_url)
        
        # 导航到搜索页面
        search_url = f'https://s.weibo.com/weibo?q={topic}'
        navigate_msg = {
            "id": 1,
            "method": "Page.navigate",
            "params": {"url": search_url}
        }
        ws.send(json.dumps(navigate_msg))
        ws.recv()
        
        time.sleep(5)
        
        # 尝试多种方式获取微博正文
        js_code = r'''
        (function() {
            var results = [];
            
            // 方法1: 尝试获取微博正文内容
            var contentSelectors = [
                '[node-type="feed_list_content"]',
                '.txt',
                '[class*="content_full"]',
                '.WB_text',
                '.detail_wbtext_428'
            ];
            
            for (var s = 0; s < contentSelectors.length; s++) {
                var selector = contentSelectors[s];
                var elements = document.querySelectorAll(selector);
                
                if (elements.length > 0) {
                    for (var i = 0; i < Math.min(3, elements.length); i++) {
                        var element = elements[i];
                        var text = element.textContent || element.innerText;
                        
                        if (text && text.trim().length > 30) {
                            results.push({
                                method: "微博正文 - " + selector,
                                length: text.length,
                                content: text.substring(0, 300),
                                html: element.outerHTML.substring(0, 200)
                            });
                        }
                    }
                    break;
                }
            }
            
            // 方法2: 如果没找到，尝试从卡片中获取
            if (results.length === 0) {
                var cards = document.querySelectorAll('.card-wrap');
                for (var i = 0; i < Math.min(3, cards.length); i++) {
                    var card = cards[i];
                    var cardText = card.textContent || card.innerText;
                    
                    // 清理文本
                    var cleanText = cardText
                        .replace(/热门|置顶|帮上头条|投诉|收藏|转发|评论|点赞|Play Video/g, '')
                        .replace(/\s+/g, ' ')
                        .trim();
                    
                    if (cleanText.length > 50) {
                        results.push({
                            method: "卡片文本",
                            length: cleanText.length,
                            content: cleanText.substring(0, 300),
                            html: "卡片内容"
                        });
                    }
                }
            }
            
            return JSON.stringify(results);
        })();
        '''
        
        js_msg = {
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {
                "expression": js_code,
                "returnByValue": True
            }
        }
        
        ws.send(json.dumps(js_msg))
        response = json.loads(ws.recv())
        
        if 'result' in response and 'result' in response['result']:
            data = response['result']['result'].get('value', '[]')
            results = json.loads(data)
            
            print(f"\n📋 获取到的微博内容 ({len(results)}条):")
            for i, item in enumerate(results):
                print(f"\n--- 内容 {i + 1} [{item['method']}] ---")
                print(f"长度: {item['length']}")
                print(f"内容: {item['content']}")
                print(f"HTML: {item['html']}")
            
            if len(results) == 0:
                print("\n❌ 未获取到有效的微博内容")
                print("💡 建议: 微博页面结构可能已更新，需要调整选择器")
        
        ws.close()
        
    except Exception as e:
        print(f"❌ 调试失败: {e}")

# 调试
debug_weibo_research_v4("北京国际电影节阵容")
