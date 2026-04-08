# 微博发布关键词触发配置

## 🔧 触发关键词配置

### 音乐相关内容
```python
'音乐|music|歌曲|song|榜单|billboard': self.publish_music_content,
'歌手|singer|专辑|album|演唱会|concert': self.publish_music_content,
```

**触发词**: 音乐、music、歌曲、歌手、榜单、演唱会、billboard、singer、album、concert
**内容类型**: 音乐推荐、榜单更新、歌手动态

### 科技相关内容
```python
'科技|tech|技术|technology|AI|人工智能': self.publish_tech_content,
'股票|stock|股市|投资|investment': self.publish_tech_content,
'数码|digital|手机|phone|电脑|computer': self.publish_tech_content,
```

**触发词**: 科技、技术、AI、人工智能、股票、股市、投资、数码、手机、电脑
**内容类型**: 科技资讯、股市动态、数码产品

### 时尚相关内容
```python
'时尚|fashion|穿搭|outfit|品牌|brand': self.publish_fashion_content,
'美妆|makeup|护肤|skincare|化妆品': self.publish_fashion_content,
```

**触发词**: 时尚、fashion、穿搭、品牌、美妆、护肤、化妆品
**内容类型**: 时尚潮流、品牌合作、美妆护肤

### 生活相关内容
```python
'美食|food|餐厅|restaurant|料理': self.publish_life_content,
'旅行|travel|旅游|vacation|景点': self.publish_life_content,
'健身|fitness|运动|exercise|减肥': self.publish_life_content,
```

**触发词**: 美食、餐厅、旅行、旅游、健身、运动、减肥
**内容类型**: 美食分享、旅行记录、健身打卡

### 热点相关内容
```python
'热点|hot|热门|trending|热搜': self.publish_hot_content,
'新闻|news|时事|current|事件': self.publish_hot_content,
```

**触发词**: 热点、热门、热搜、新闻、时事、事件
**内容类型**: 当前热搜话题、时事新闻

### 通用触发
```python
'发微博|post|发布|publish': self.publish_general_content,
'测试|test|demo': self.publish_test_content
```

**触发词**: 发微博、发布、publish、post、测试、test、demo
**内容类型**: 通用内容、功能测试

## 🎯 使用示例

### 示例1: 音乐内容
**用户输入**: "我想发一条关于音乐的微博"
**触发词**: "音乐"
**执行操作**: 发布音乐相关内容
**预期结果**: 发布包含音乐推荐和榜单信息的微博

### 示例2: 科技内容
**用户输入**: "发布一条科技资讯"
**触发词**: "科技"
**执行操作**: 发布科技相关内容
**预期结果**: 发布包含科技动态和股市信息的微博

### 示例3: 热点内容
**用户输入**: "来一条热门话题"
**触发词**: "热门"
**执行操作**: 发布热点相关内容
**预期结果**: 发布基于当前热搜话题的微博

## ⚙️ 自定义配置

### 添加新关键词
```python
# 在keywords字典中添加新的关键词映射
self.keywords = {
    # 现有配置...
    
    # 新增关键词
    '新关键词|new_keyword': self.new_handler_method,
}
```

### 创建新的处理方法
```python
def new_handler_method(self):
    """新的内容处理方法"""
    content = f"这是新关键词对应的内容 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    return self.publisher.publish_weibo(content)
```

## 🔍 触发检测逻辑

### 检测流程
1. 将输入文本转换为小写
2. 遍历所有关键词模式
3. 使用字符串匹配检测关键词
4. 执行对应的处理方法
5. 返回执行结果

### 匹配规则
- **大小写不敏感**: "音乐" 和 "Music" 都能触发
- **部分匹配**: 包含关键词即可触发
- **多关键词**: 支持多个关键词同时触发
- **优先级**: 按照配置顺序执行

## 📊 触发统计

### 成功指标
- ✅ 关键词检测成功率
- ✅ 内容发布成功率
- ✅ 用户满意度
- ✅ 发布频率控制

### 监控建议
```python
# 添加触发日志
import logging
logging.info(f"触发关键词: {keyword}, 消息: {message}, 结果: {success}")
```

## 🛠️ 故障排除

### 常见问题

#### 1. 关键词不触发
**原因**: 关键词配置错误或匹配逻辑问题
**解决方案**: 
- 检查关键词拼写
- 确认匹配逻辑
- 添加调试日志

#### 2. 重复触发
**原因**: 多个关键词匹配同一消息
**解决方案**:
- 优化关键词配置
- 添加去重逻辑
- 设置触发冷却时间

#### 3. 内容发布失败
**原因**: 浏览器连接问题或内容格式问题
**解决方案**:
- 检查浏览器状态
- 验证内容格式
- 添加错误重试机制

## 🚀 高级功能

### 条件触发
```python
# 基于时间的触发
if datetime.now().hour in [9, 12, 18]:  # 特定时间段
    return self.publish_weibo(content)
```

### 频率限制
```python
# 限制发布频率
if self.last_publish_time and (datetime.now() - self.last_publish_time).seconds < 300:
    print("发布频率过高，请稍后再试")
    return False
```

### 用户偏好
```python
# 基于用户历史偏好的触发
user_preferences = self.get_user_preferences(user_id)
if user_preferences.get('prefer_music'):
    return self.publish_music_content()
```

## 📝 配置最佳实践

1. **关键词设计**: 使用具体且有代表性的关键词
2. **内容质量**: 确保每个触发词对应高质量的内容模板
3. **错误处理**: 添加完善的错误处理和日志记录
4. **性能优化**: 避免过多的关键词匹配影响性能
5. **用户反馈**: 收集用户反馈优化关键词配置
6. **定期更新**: 根据热点变化更新关键词和内容模板

---
*最后更新: 2026-04-08 12:16*
