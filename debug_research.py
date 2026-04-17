import json
import requests
import websocket
import time

def debug_weibo_research(topic):
    """调试微博调研功能"""
    print(f"🔍 调试微博调研: {topic}")
    
    # 获取CDP连接信息
    try:
        response = requests.get('http://localhost:18800/json/list')
        page_info = response.json()[0]
        ws_url = page_info['webSocketDebuggerUrl']
        
        # 连接到浏览器
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
        
        # 等待页面加载
        time.sleep(5)
        
        # 获取详细调研数据
        js_code = '''
        (function() {
            var research = {
                searchResults: [],
                hotTopics: [],
                pageStats: {}
            };
            
            research.pageStats = {
                cardWrap: document.querySelectorAll('.card-wrap').length,
                cards: document.querySelectorAll('.card').length,
                textElements: document.querySelectorAll('[class*="text"]').length
            };
            
            // 获取主要内容
            var mainElements = document.querySelectorAll('.card-wrap, .card');
            
            for (var i = 0; i < Math.min(3, mainElements.length); i++) {
                var element = mainElements[i];
                var textElement = element.querySelector('[class*="text"]');
                if (textElement) {
                    var cleanText = textElement.textContent
                        .replace(/热门|置顶|帮上头条|投诉|收藏/g, '')
                        .replace(/Play Video.*$/g, '')
                        .replace(/\s+/g, ' ')
                        .trim();
                    
                    research.searchResults.push({
                        rank: i + 1,
                        content: cleanText,
                        fullLength: cleanText.length
                    });
                }
            }
            
            // 获取话题标签
            var hashtagElements = document.querySelectorAll('[href*="q=%23"]');
            for (var i = 0; i < Math.min(5, hashtagElements.length); i++) {
                var hashtag = hashtagElements[i].textContent.trim();
                if (hashtag && hashtag.startsWith('#') && hashtag.endsWith('#')) {
                    research.hotTopics.push(hashtag);
                }
            }
            
            return JSON.stringify(research);
        })();
        '''
        
        # 执行JavaScript获取数据
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
            data = response['result']['result'].get('value', '{}')
            research_data = json.loads(data)
            
            print("\n📊 页面统计:")
            print(f"   card-wrap: {research_data['pageStats']['cardWrap']}")
            print(f"   card: {research_data['pageStats']['cards']}")
            print(f"   text元素: {research_data['pageStats']['textElements']}")
            
            print(f"\n📋 搜索结果 ({len(research_data['searchResults'])}条):")
            for i, item in enumerate(research_data['searchResults']):
                print(f"   {i+1}. 长度{item['fullLength']}: {item['content'][:200]}")
            
            print(f"\n🏷️  热门标签 ({len(research_data['hotTopics'])}个):")
            for tag in research_data['hotTopics']:
                print(f"   - {tag}")
        
        ws.close()
        
    except Exception as e:
        print(f"❌ 调试失败: {e}")

# 调试北京国际电影节阵容话题
debug_weibo_research("北京国际电影节阵容")
