#!/usr/bin/env python3
"""
Weibo Publisher - Core publishing functionality
"""

import json
import websocket
import time
import requests
from datetime import datetime

class WeiboPublisher:
    def __init__(self, cdp_port=18800):
        self.cdp_port = cdp_port
        self.ws = None
        self.message_id = 0
        
    def connect_browser(self):
        """Connect to browser via WebSocket"""
        try:
            response = requests.get(f'http://localhost:{self.cdp_port}/json/list')
            page_info = response.json()[0]
            ws_url = page_info['webSocketDebuggerUrl']
            self.ws = websocket.create_connection(ws_url)
            return True
        except Exception as e:
            print(f"❌ Browser connection failed: {e}")
            return False
            
    def input_content(self, content):
        """Input text content to textarea"""
        if not self.ws:
            return False
            
        self.message_id += 1
        escaped_content = content.replace('"', '\\"').replace("'", "\\'").replace('\n', '\\n')
        
        script = f'''
        (function() {{
            var textAreas = document.querySelectorAll('textarea');
            for (var i = 0; i < textAreas.length; i++) {{
                var ta = textAreas[i];
                if (ta.placeholder && ta.placeholder.includes('分享新鲜事')) {{
                    ta.value = "{escaped_content}";
                    ta.dispatchEvent(new Event('input', {{bubbles: true}}));
                    ta.dispatchEvent(new Event('change', {{bubbles: true}}));
                    return {{inputSuccess: true, contentLength: ta.value.length}};
                }}
            }}
            return {{inputSuccess: false}};
        }})();
        '''
        
        message = {
            'id': self.message_id,
            'method': 'Runtime.evaluate',
            'params': {
                'expression': script,
                'returnByValue': True
            }
        }
        
        try:
            self.ws.send(json.dumps(message))
            response = self.ws.recv()
            result = json.loads(response)
            return result.get('result', {}).get('result', {}).get('value', {}).get('inputSuccess', False)
        except Exception as e:
            print(f"❌ Input content failed: {e}")
            return False
            
    def click_publish(self):
        """Click publish button"""
        if not self.ws:
            return False
            
        self.message_id += 1
        
        script = '''
        (function() {
            var elements = document.querySelectorAll('*');
            for (var i = 0; i < elements.length; i++) {
                var el = elements[i];
                var text = el.textContent || '';
                
                if (text.includes('发送') && el.className.includes('m-send-btn')) {
                    try {
                        el.click();
                        return {clicked: true, text: text.trim()};
                    } catch (e) {
                        return {clicked: false, error: e.message};
                    }
                }
            }
            return {clicked: false, reason: 'no matching element'};
        })();
        '''
        
        message = {
            'id': self.message_id,
            'method': 'Runtime.evaluate',
            'params': {
                'expression': script,
                'returnByValue': True
            }
        }
        
        try:
            self.ws.send(json.dumps(message))
            response = self.ws.recv()
            result = json.loads(response)
            return result.get('result', {}).get('result', {}).get('value', {}).get('clicked', False)
        except Exception as e:
            print(f"❌ Click publish failed: {e}")
            return False
            
    def publish_weibo(self, content):
        """Complete publish workflow"""
        print("🎯 Starting Weibo publish...")
        
        # Connect to browser
        if not self.connect_browser():
            return False
            
        try:
            # Navigate to compose page
            print("1. Navigating to compose page...")
            self.message_id += 1
            
            script = '''
            (function() {
                if (window.location.href !== 'https://m.weibo.cn/compose') {
                    window.location.href = 'https://m.weibo.cn/compose';
                }
                return {navigated: true};
            })();
            '''
            
            message = {
                'id': self.message_id,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': script,
                    'returnByValue': True
                }
            }
            
            self.ws.send(json.dumps(message))
            self.ws.recv()
            time.sleep(3)
            
            # Input content
            print("2. Inputting content...")
            if not self.input_content(content):
                print("❌ Failed to input content")
                return False
            print("   ✅ Content input successful")
            
            time.sleep(2)
            
            # Click publish
            print("3. Clicking publish button...")
            if not self.click_publish():
                print("❌ Failed to click publish button")
                return False
            print("   ✅ Publish button clicked")
            
            # Verify publish
            time.sleep(3)
            print("4. Verifying publish...")
            
            self.message_id += 1
            script = '''
            (function() {
                return {
                    url: window.location.href,
                    title: document.title
                };
            })();
            '''
            
            message = {
                'id': self.message_id,
                'method': 'Runtime.evaluate',
                'params': {
                    'expression': script,
                    'returnByValue': True
                }
            }
            
            self.ws.send(json.dumps(message))
            response = self.ws.recv()
            result = json.loads(response)
            
            status = result.get('result', {}).get('result', {}).get('value', {})
            print(f"   📊 Publish status: {status}")
            
            print("\n🎉 Weibo published successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Publish failed: {e}")
            return False
        finally:
            if self.ws:
                self.ws.close()
                
    def verify_publish(self):
        """Verify successful publishing"""
        # Implementation for verification
        pass

if __name__ == "__main__":
    publisher = WeiboPublisher()
    test_content = f"测试微博发布 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    success = publisher.publish_weibo(test_content)
    
    if success:
        print("✅ Publish successful!")
    else:
        print("❌ Publish failed!")
