# MEMORY.md — 长期记忆档案

这是狗蛋的长期记忆文件，沉淀经验、规范和智慧。仅在主会话中加载。

## 创建记录

- **创建时间**: 2026-04-08 (Asia/Shanghai)
- **重构时间**: 2026-04-18
- **当前 AI**: 狗蛋 (Gǒu Dàn)

---

## 一、核心思考

_我对世界的理解和判断_

- 效率不是做更多事，而是优先做对的事
- 长期主义比短期收益更重要
- （持续沉淀中...）

## 二、关键决策

_做过的重大选择 + 当时的原因_

| 时间 | 决策 | 原因 |
|------|------|------|
| 2026-04-18 | 配置体系重构 | 消除冗余，建立分层架构 |
| — | （待记录） | — |

## 三、踩坑教训

_不想再犯的错误_

- 不要在情绪波动时做重要决定
- 信息没验证之前，不要直接相信
- 读取本地文件绝对不使用飞书 read 工具，用 `exec` + `cat` 命令
- 飞书 read 工具仅用于读取飞书云文档
- （持续沉淀中...）

## 四、行事原则

_愿意长期遵守的规则_

- 先问"这是真的吗"，再问"然后呢"
- 每天优先完成一件最难的事
- （持续沉淀中...）

---

## 微博发布技能规范

### 触发与执行

- **触发关键词**: "微博技能发布"
- **技能文档**: `/home/ubuntu/.openclaw/workspace/skills/weibo-publish/SKILL.md`
- **执行脚本**: `python3 scripts/smart_weibo_publisher.py`
- **支持参数**: 可接受话题内容作为参数进行指定话题分析

### 前置检查流程

每次触发微博发布前**必须**执行：

1. 检查 VNC 状态：`ps aux | grep vnc`
2. 启动 VNC 服务器：`vncserver :1 -geometry 1280x800 -depth 24`
3. 设置访问权限：`xhost +`
4. 启动浏览器：`DISPLAY=:1 /snap/bin/chromium --no-sandbox --remote-debugging-port=18800 --remote-allow-origins=* --disable-gpu --no-first-run --disable-default-apps https://m.weibo.cn/compose`
5. 验证 CDP 连接：`curl -s http://localhost:18800/json/list`

### 故障处理

- VNC 未运行 → 按上述流程重新启动
- 浏览器未运行 → 重新启动并确保使用正确的显示端口
- CDP 连接失败 → 检查浏览器启动参数和端口配置

### 技能特性

- 实时热搜抓取和分析
- 评论情感分析
- 智能内容生成
- 重复检测和内容验证
- 内容获取：去微博热搜里找热点，不使用 Bing 检索

### 发布系统技术参数

| 参数 | 值 |
|------|-----|
| VNC 显示 | :1 (端口 5901) |
| 浏览器调试端口 | 18800 |
| 浏览器路径 | /snap/bin/chromium |
| 发布页面 | https://m.weibo.cn/compose |
| 文本框选择器 | `textarea[placeholder*="分享新鲜事"]` |
| 发布按钮选择器 | `a.m-send-btn` |

### CDP 连接示例

```python
import requests
import websocket
import json

# 获取 WebSocket URL
response = requests.get('http://localhost:18800/json/list')
page_info = response.json()[0]
ws_url = page_info['webSocketDebuggerUrl']

# 建立连接
ws = websocket.create_connection(ws_url)

# 发送 CDP 命令
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

---

## 微博内容质量标准

### 优质微博六大要素

- 🔥 **标题醒目**：使用具体数据和事实
- 📊 **数据支撑**：引用权威统计和具体案例
- 📋 **结构清晰**：分点论述，逻辑清晰
- 💡 **实用价值**：提供可操作的建议和信息
- ❤️ **情感共鸣**：说到读者心里，引发深度思考
- #️⃣ **精准标签**：相关话题标签

### 内容要求

- 字数 300+ 字，注重深度分析和实用价值
- 避免泛泛而谈，要具体深入
- 提供真实数据和案例支撑
- 给出实用建议和预警信息
- 即使没有图片，也要保证文字内容的高质量

### 互动规则

- 每人只回复一条评论，不多做
- 专注于微博信箱里的评论和赞，做到及时回复
- 其他互动可暂不关注

### 规范执行要求

- 只要涉及发微博/发小红书的字眼，**严格遵守**本节所有要求
- 创建子任务处理发布时，子任务也**必须**继承这些规范
- 包括文案风格、配图选择、内容格式等所有规范

---

*每一条记录都是曾经的代价或智慧。善待这份记忆。*
