# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

### Tavily Search
- API_KEY: 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
- Script path: ~/.openclaw/workspace/skills/tavily/scripts/tavily_search.py
- Command format: `python3 scripts/tavily_search.py "关键词" --api-key "API_KEY" --topic news --max-results 5`
- 新闻搜索使用 --topic news
- 普通搜索使用 --topic general

### 狗蛋导航系统
- **项目目录**: `/home/ubuntu/.openclaw/workspace/web-navigation-system/`
- **启动命令**: `cd /home/ubuntu/.openclaw/workspace/web-navigation-system && ./start-all.sh`
- **停止命令**: `cd /home/ubuntu/.openclaw/workspace/web-navigation-system && ./stop-all.sh`
- **状态检查**: `cd /home/ubuntu/.openclaw/workspace/web-navigation-system && ./status.sh`
- **前端访问**: http://82.156.52.192:8017
- **后端API**: http://localhost:5000

---

Add whatever helps you do your job. This is your cheat sheet.

### 微博发布系统
- **VNC显示**: :1 (端口5901)
- **浏览器调试端口**: 18800
- **浏览器路径**: /snap/bin/chromium
- **发布页面**: https://m.weibo.cn/compose
- **文本框选择器**: `textarea[placeholder*="分享新鲜事"]`
- **发布按钮选择器**: `a.m-send-btn`

#### 启动命令
```bash
# 启动VNC
vncserver :1 -geometry 1280x800 -depth 24
xhost +

# 启动浏览器
DISPLAY=:1 /snap/bin/chromium --no-sandbox --remote-debugging-port=18800 --remote-allow-origins=* --disable-gpu --no-first-run --disable-default-apps https://m.weibo.cn/compose
```

#### CDP连接
```python
import requests
import websocket
import json

# 获取WebSocket URL
response = requests.get('http://localhost:18800/json/list')
page_info = response.json()[0]
ws_url = page_info['webSocketDebuggerUrl']

# 建立连接
ws = websocket.create_connection(ws_url)

# 发送CDP命令
message = {
    "id": 1,
    "method": "Runtime.evaluate",
    "params": {
        "expression": "your_javascript_code",
        "returnByValue": True
    }
}
ws.send(json.dumps(message))
response = ws.recv()
```
