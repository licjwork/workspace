# Weibo Publisher Skill Installation

## Prerequisites
- Ubuntu/Debian Linux
- Python 3.8+
- VNC server
- Chromium browser

## Quick Install
```bash
sudo snap install chromium
pip3 install websocket-client requests --break-system-packages
```

## Quick Start
```bash
vncserver :1 -geometry 1280x800 -depth 24
xhost +
DISPLAY=:1 /snap/bin/chromium --no-sandbox --remote-debugging-port=18800 --remote-allow-origins=* --disable-gpu --no-first-run --disable-default-apps https://m.weibo.cn/compose
```

## Test
```bash
python3 scripts/weibo_publish_test.py
```

## Publish
```bash
python3 scripts/weibo_hot_search_publish.py
```

See references/ for detailed documentation.
