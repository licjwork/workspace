import json
import requests
import websocket
import time

def debug_weibo_research_v2(topic):
    """调试微博调研功能 - 版本2"""
    print(f"🔍 调试微博调研V2: {topic}")
    
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
        
        # 尝试多种选择器获取内容
        js_code = r'''
        (function() {
            var research = {
                searchResults: [],
                hotTopics: [],
                debug: []
            };
            
            // 尝试多种内容选择器
            var selectors = [
                '.card-wrap [class*="text"]',
                '.card [class*="text"]', 
                '[class*="content"]',
                '.txt',
                '[node-type="feed_list_content"]'
            ];
            
            research.debug.push("页面URL: " + window.location.href);
            
            for (var s = 0; s < selectors.length; s++) {
                var selector = selectors[s];
                var elements = document.querySelectorAll(selector);
                research.debug.push("选择器 " + selector + ": " + elements.length + " 个元素");
                
                if (elements.length > 0) {
                    for (var i = 0; i < Math.min(3, elements.length); i++) {
                        var element = elements[i];
                        var text = element.textContent || element.innerText;
                        
                        if (text && text.trim().length > 20) {
                            var cleanText = text
                                .replace(/热门|置顶|帮上头条|投诉|收藏|转发|评论|点赞/g, '')
                                .replace(/Play Video.*$/g, '')
                                .replace(/\s+/g, ' ')
                                .trim();
                            
                            if (cleanText.length > 20) {
                                research.searchResults.push({
                                    selector: selector,
                                    content: cleanText.substring(0, 300),
                                    fullLength: cleanText.length
                                });
                            }
                        }
                    }
                    break; // 找到有效选择器就停止
                }
            }
            
            // 获取话题标签
            var hashtagElements = document.querySelectorAll('[href*="q=%23"]');
            for (var i = 0; i < Math.min(10, hashtagElements.length); i++) {
                var hashtag = hashtagElements[i].textContent.trim();
                if (hashtag && hashtag.startsWith('#') && hashtag.endsWith('#')) {
                    research.hotTopics.push(hashtag);
                }
            }
            
            return JSON.stringify(research);
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
            data = response['result']['result'].get('value', '{}')
            research_data = json.loads(data)
            
            print("\n🐛 调试信息:")
            for debug_info in research_data.get('debug', []):
                print(f"   {debug_info}")
            
            print(f"\n📋 搜索结果 ({len(research_data['searchResults'])}条):")
            for i, item in enumerate(research_data['searchResults']):
                print(f"   {i+1}. [{item['selector']}] 长度{item['fullLength']}: {item['content']}")
            
            print(f"\n🏷️  热门标签 ({len(research_data['hotTopics'])}个):")
            for tag in research_data['hotTopics']:
                print(f"   - {tag}")
        
        ws.close()
        
    except Exception as e:
        print(f"❌ 调试失败: {e}")

# 调试
debug_weibo_research_v2("北京国际电影节阵容")
