import json
import requests
import websocket
import time

def debug_weibo_research_v3(topic):
    """调试微博调研功能 - 版本3，查看实际内容"""
    print(f"🔍 调试微博调研V3: {topic}")
    
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
        
        # 直接获取前几个元素的原始内容
        js_code = r'''
        (function() {
            var results = [];
            
            // 获取前5个文本元素的内容
            var textElements = document.querySelectorAll('.card-wrap [class*="text"]');
            
            for (var i = 0; i < Math.min(5, textElements.length); i++) {
                var element = textElements[i];
                var rawText = element.textContent || element.innerText;
                
                results.push({
                    index: i,
                    rawLength: rawText.length,
                    rawContent: rawText.substring(0, 200),
                    elementHtml: element.outerHTML.substring(0, 300)
                });
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
            
            print(f"\n📋 前{len(results)}个文本元素的原始内容:")
            for item in results:
                print(f"\n--- 元素 {item['index'] + 1} ---")
                print(f"长度: {item['rawLength']}")
                print(f"内容: {item['rawContent']}")
                print(f"HTML: {item['elementHtml']}")
        
        ws.close()
        
    except Exception as e:
        print(f"❌ 调试失败: {e}")

# 调试
debug_weibo_research_v3("北京国际电影节阵容")
