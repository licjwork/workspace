# Weibo Publisher Skill v5.0

智能微博发布技能，支持实时热搜分析和评论参考。

## 🚀 核心特性

- **实时热搜抓取**：使用VNC浏览器实时获取微博热搜数据
- **评论分析**：自动抓取热搜话题下的热门评论
- **情感分析**：分析评论情感倾向（正面/负面/中性）
- **智能内容生成**：基于真实数据和评论生成微博内容
- **安全防护**：重复检测 + 内容验证

## 📖 使用方法

### 智能分析实时热搜
```bash
python3 scripts/smart_weibo_publisher.py
```

### 智能分析指定话题
```bash
python3 scripts/smart_weibo_publisher.py "你的话题内容"
```

## 📁 核心文件

- `smart_weibo_publisher.py` - 智能发布主程序
- `hot_search_analyzer.py` - 热搜数据分析器
- `smart_content_generator.py` - 智能内容生成器
- `content_validator.py` - 内容验证器
- `duplicate_checker.py` - 重复检测器
