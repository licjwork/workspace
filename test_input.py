import requests
import json
import websocket

response = requests.get('http://localhost:18800/json/list')
page_info = response.json()[0]
ws_url = page_info['webSocketDebuggerUrl']

ws = websocket.create_connection(ws_url)

# 测试设置内容
test_js = 'document.querySelector("textarea[placeholder*=\\"分享新鲜事\\"]").value = "手动测试内容"'
message = {
    'id': 1,
    'method': 'Runtime.evaluate',
    'params': {
        'expression': test_js,
        'returnByValue': True
    }
}

ws.send(json.dumps(message))
result = json.loads(ws.recv())
print('设置结果:', result)

ws.close()
