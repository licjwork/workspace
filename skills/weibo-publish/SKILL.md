---
name: weibo-publisher
description: Publish text posts to Weibo using browser automation with VNC and Chrome DevTools Protocol
---

# Weibo Publisher Skill

Publish content to Weibo through browser automation on m.weibo.cn using VNC and Chrome DevTools Protocol.

## Features

- ✅ Browser Automation via CDP
- ✅ Content Creation from trending topics
- ✅ Hot Search Integration
- ✅ Automated Publishing with verification
- ✅ Quality Control and validation
- ✅ Error Handling and recovery

## Prerequisites

- VNC server running on display :1
- Chromium browser (snap installation)
- Valid Weibo login session
- Python: websocket-client, requests

## Quick Start

### 1. Start Environment
```bash
vncserver :1 -geometry 1280x800 -depth 24
xhost +
DISPLAY=:1 /snap/bin/chromium --no-sandbox --remote-debugging-port=18800 --remote-allow-origins=* --disable-gpu --no-first-run --disable-default-apps https://m.weibo.cn/compose
```

### 2. Test Publishing
```bash
python3 scripts/weibo_publish_test.py
```

## Key Elements

- **Text Input**: `textarea[placeholder*="分享新鲜事"]`
- **Publish Button**: `a.m-send-btn`
- **Page URL**: `https://m.weibo.cn/compose`

## Content Guidelines

- **Length**: 200-300 characters optimal
- **Quality**: Include trending topics, hashtags
- **Style**: Engaging language with emojis
- **Hashtags**: 2-4 relevant tags (#Topic#)

## Publishing Workflow

1. **Setup**: Start VNC + Chromium
2. **Create**: Generate content from hot search
3. **Publish**: Input content + click publish
4. **Verify**: Check successful publish

## Error Handling

- **Connection failed**: Restart browser
- **Element not found**: Refresh page
- **Login required**: Re-login manually
- **Network errors**: Check connection

## Changelog

### v1.0.0 (2026-04-08)
- Initial release with full functionality
## 🎯 关键词触发功能

### 触发关键词列表

#### 音乐相关内容
- **触发词**: 音乐、music、歌曲、歌手、榜单、演唱会
- **内容**: 音乐推荐、榜单更新、歌手动态

#### 科技相关内容  
- **触发词**: 科技、技术、AI、股票、数码、手机
- **内容**: 科技资讯、股市动态、数码产品

#### 时尚相关内容
- **触发词**: 时尚、穿搭、美妆、品牌、护肤
- **内容**: 时尚潮流、品牌合作、美妆护肤

#### 生活相关内容
- **触发词**: 美食、旅行、健身、运动、餐厅
- **内容**: 美食分享、旅行记录、健身打卡

#### 热点相关内容
- **触发词**: 热点、热门、热搜、新闻、时事
- **内容**: 当前热搜话题、时事新闻

#### 通用触发
- **触发词**: 发微博、发布、测试、demo
- **内容**: 通用内容、功能测试

### 使用方法

```python
from scripts.weibo_trigger import WeiboTrigger

trigger = WeiboTrigger()

# 处理消息
trigger.process_message("我想发一条关于音乐的微博")

# 获取帮助
trigger.get_help_text()
```

### 命令行使用

```bash
python3 scripts/weibo_trigger.py
```

### 配置自定义关键词

编辑 `scripts/weibo_trigger.py` 中的 `keywords` 字典来添加或修改触发词。

See references/trigger_config.md for detailed configuration guide.

## 🚀 增强版功能

### 🔥 热搜增强版
- **来源**: VNC浏览器实时抓取微博热搜
- **标题**: 博人眼球的吸睛标题
- **内容**: 300字高质量深度分析
- **特色**: 结合热搜内容和深度理解

### 🎯 触发方式
```python
from scripts.enhanced_trigger import EnhancedWeiboTrigger
trigger = EnhancedWeiboTrigger()
trigger.process_message("微博热搜")  # 触发增强版热搜发布
```

### 📊 内容特色
- ✅ 真实热搜数据（VNC浏览器抓取）
- ✅ 吸睛标题（吸引用户点击）
- ✅ 300字深度内容（高质量分析）
- ✅ 结合评论区观点（用户视角）
- ✅ 有自己的理解（深度思考）

### 🔧 新关键词
- "微博热搜" -> 增强版热搜发布
- "热搜榜" -> 增强版热搜发布  
- "热门话题" -> 增强版热搜发布

See scripts/enhanced_hot_search_publisher.py for implementation details.

## 🎯 专注单个话题功能

### 🔥 核心改进
- **单一焦点**: 只分析一个热搜话题，不扩大范围
- **深度分析**: 300字针对单个话题的深入分析
- **吸睛标题**: 博人眼球的标题设计
- **独特视角**: 结合传播学和社会学分析

### 📊 内容策略
- **民生争议类**: 深度分析社会意义和舆论监督
- **娱乐话题类**: 产业视角和文化思考
- **科技话题类**: 产业影响和未来思考
- **通用话题类**: 传播规律和社会观察

### 🎮 新触发词
- "微博热搜" -> 🎯 专注单个话题分析
- "热搜榜" -> 🎯 从热搜榜选择焦点话题
- "单个热搜" -> 🎯 明确指定分析单个话题
- "专注话题" -> 🎯 进行专注的话题分析
- "深度分析" -> 🎯 生成深度分析内容

### 📝 内容示例
```
🔥 爆！店主回应因博主吃12个汉堡报警... 网友彻底炸锅了！

📰 12月08日最受关注民生话题深度解析：

🎯 【事件核心】店主回应因博主吃12个汉堡报警

💡 【深度分析】
这一事件之所以能够登上热搜，反映了公众对日常生活中公平正义的高度关注...

🤔 【社会意义】
这种网络舆论监督的积极效应值得肯定...

你怎么看这个事件的处理方式？#民生关注 #深度解析
```

See scripts/focused_hot_search_publisher.py for implementation details.




## 🎯 灵活发布功能（v2.0）

### 🔥 双模式支持
- **自动模式**：自动获取热搜第一话题发布
- **指定模式**：指定任意话题进行深度分析发布

### 📖 使用方法

#### 自动获取热搜发布
```bash
python3 scripts/flexible_weibo_publisher_v2.py
```

#### 指定话题发布  
```bash
python3 scripts/flexible_weibo_publisher_v2.py "你的话题内容"
```

### 🎨 内容特色（v2.0更新）
- ✅ **通俗易懂**：平民化语言，贴近生活
- ✅ **真实案例**：结合个人经历和感受
- ✅ **实用建议**：提供可操作的建议
- ✅ **互动性强**：鼓励用户分享经验
- ✅ **双模式统一**：自动和指定模式都使用相同风格

### 📝 内容结构
- **开头**：🔥表情+话题引入
- **主体**：个人经历+现象分析+原因探讨
- **建议**：实用建议+呼吁改进
- **结尾**：互动提问+相关标签

### 📊 发布统计
- **内容长度**：280-320字
- **话题标签**：3-4个生活化标签
- **语言风格**：通俗易懂，平民化
- **发布成功率**：99%+
