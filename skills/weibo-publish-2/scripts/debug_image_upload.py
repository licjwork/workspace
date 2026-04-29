#!/usr/bin/env python3
import os
import sys
import asyncio
from playwright.async_api import async_playwright
from improved_content_generator import call_dogegg_ai

async def debug_image_upload():
    # 获取WebSocket URL
    response = requests.get('http://localhost:18800/json/list')
    page_info = response.json()[0]
    ws_url = page_info['webSocketDebuggerUrl']

    # 建立CDP连接
    ws = websocket.create_connection(ws_url)

    # 检查发布页面的图片预览
    js_code = '''
    // 检查发布页面的所有图片相关元素
    const results = {
        fileInputs: document.querySelectorAll('input[type=\"file\"]').length,
        images: document.querySelectorAll('img').length,
        uploadPreviews: document.querySelectorAll('[class*=\"preview\"], [class*=\"thumb\"]').length,
        uploadAreas: document.querySelectorAll('[class*=\"upload\"], [class*=\"image\"]').length
    };
    JSON.stringify(results);
    '''

    ws.send(json.dumps({
        'id': 1,
        'method': 'Runtime.evaluate',
        'params': {
            'expression': js_code,
            'returnByValue': True
        }
    }))

    response = ws.recv()
    result = json.loads(response)

    if 'result' in result and 'result' in result['result']:
        if 'value' in result['result']['result']:
            data = json.loads(result['result']['result']['value'])
            print('发布页面状态检查:')
            print(f'文件输入框: {data[\"fileInputs\"]}')
            print(f'图片元素: {data[\"images\"]}')
            print(f'预览元素: {data[\"uploadPreviews\"]}')
            print(f'上传区域: {data[\"uploadAreas\"]}')
        else:
            print('检查失败:', result)
    else:
        print('CDP调用失败')

    ws.close()

if __name__ == "__main__":
    import requests
    import websocket
    import json
    asyncio.run(debug_image_upload())
