# 微博发布关键词触发集成指南

## 🎯 快速集成

### 1. 基本使用
```python
from skills.weibo_publish.scripts.weibo_trigger import WeiboTrigger
trigger = WeiboTrigger()
trigger.process_message("发微博")
```

### 2. 关键词分类
- 音乐: 音乐、music、歌曲、歌手
- 科技: 科技、技术、AI、股票  
- 时尚: 时尚、穿搭、美妆、品牌
- 生活: 美食、旅行、健身、运动
- 热点: 热点、热门、热搜、新闻
- 通用: 发微博、发布、post
- 测试: 测试、test、demo

### 3. 演示运行
```bash
python3 skills/weibo-publish/scripts/weibo_trigger_demo.py
```

### 4. 自定义配置
编辑 scripts/weibo_trigger.py 中的 keywords 字典

## 📚 参考文档
- SKILL.md - 主文档
- references/trigger_config.md - 配置指南
- references/examples.md - 代码示例

## 🔧 故障排除
- 关键词不触发: 检查关键词拼写
- 浏览器连接失败: 检查CDP端口 18800
- 发布失败: 检查登录状态和网络连接
