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
