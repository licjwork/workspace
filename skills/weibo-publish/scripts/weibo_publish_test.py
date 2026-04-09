#!/usr/bin/env python3
"""
微博发布功能测试脚本

使用方法:
1. 确保VNC和浏览器已启动
2. 运行此脚本: python3 weibo_publish_test.py
3. 查看测试结果
"""

import json
import websocket
import time
import requests
from datetime import datetime

def test_weibo_publish():
    """测试微博发布功能"""
    print("=== 微博发布功能测试 ===")
    
    try:
        # 1. 获取浏览器信息
        print("1. 连接浏览器...")
        response = requests.get('http://localhost:18800/json/list')
        page_info = response.json()[0]
        ws_url = page_info['webSocketDebuggerUrl']
        print(f"   ✅ 浏览器连接成功: {page_info['title']}")
        
        # 2. 建立WebSocket连接
        print("2. 建立WebSocket连接...")
        ws = websocket.create_connection(ws_url, timeout=10)
        print("   ✅ WebSocket连接成功")
        
        message_id = 1
        
        # 3. 输入微博内容
        print("3. 输入微博内容...")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        test_content = f"测试微博发布功能 - {current_time}"
        
        input_script = f"""
        (function() {{
            var textAreas = document.querySelectorAll('textarea');
            for (var i = 0; i < textAreas.length; i++) {{
                var ta = textAreas[i];
                if (ta.placeholder && ta.placeholder.includes('分享新鲜事')) {{
                    ta.value = '{test_content}';
                    ta.dispatchEvent(new Event('input', {{bubbles: true}}));
                    ta.dispatchEvent(new Event('change', {{bubbles: true}}));
                    return {{inputSuccess: true, content: ta.value}};
                }}
            }}
            return {{inputSuccess: false, textareaCount: textAreas.length}};
        }})();
        """
        
        message = {
            "id": message_id,
            "method": "Runtime.evaluate",
            "params": {
                "expression": input_script,
                "returnByValue": True
            }
        }
        
        ws.send(json.dumps(message))
        response = ws.recv()
        result = json.loads(response)
        
        if result.get('result', {}).get('result', {}).get('value', {}).get('inputSuccess'):
            print(f"   ✅ 文本输入成功: {test_content}")
        else:
            print("   ❌ 文本输入失败")
            return False
        
        # 等待页面响应
        time.sleep(2)
        
        # 4. 查找发布按钮
        print("4. 查找发布按钮...")
        message_id += 1
        
        button_script = """
        (function() {
            var elements = document.querySelectorAll('*');
            for (var i = 0; i < elements.length; i++) {
                var el = elements[i];
                var text = el.textContent || '';
                
                if (text.includes('发送') && el.className.includes('m-send-btn')) {
                    return {
                        found: true,
                        element: {
                            tag: el.tagName,
                            text: text.trim(),
                            className: el.className
                        }
                    };
                }
            }
            return {found: false};
        })();
        """
        
        message = {
            "id": message_id,
            "method": "Runtime.evaluate",
            "params": {
                "expression": button_script,
                "returnByValue": True
            }
        }
        
        ws.send(json.dumps(message))
        response = ws.recv()
        result = json.loads(response)
        
        if result.get('result', {}).get('result', {}).get('value', {}).get('found'):
            print("   ✅ 发布按钮查找成功")
        else:
            print("   ❌ 发布按钮查找失败")
            return False
        
        # 5. 点击发布按钮
        print("5. 点击发布按钮...")
        message_id += 1
        
        click_script = """
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
        """
        
        message = {
            "id": message_id,
            "method": "Runtime.evaluate",
            "params": {
                "expression": click_script,
                "returnByValue": True
            }
        }
        
        ws.send(json.dumps(message))
        response = ws.recv()
        result = json.loads(response)
        
        if result.get('result', {}).get('result', {}).get('value', {}).get('clicked'):
            print("   ✅ 发布按钮点击成功")
            print("\n🎉 微博发布功能测试完成！")
            return True
        else:
            print("   ❌ 发布按钮点击失败")
            return False
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False
    finally:
        try:
            ws.close()
        except:
            pass

if __name__ == "__main__":
    success = test_weibo_publish()
    if success:
        print("\n✅ 所有测试通过！微博发布功能正常。")
    else:
        print("\n❌ 测试失败，请检查环境和配置。")
