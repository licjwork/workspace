# 微博热搜榜获取技能

用于获取微博实时热搜榜单标题，支持格式化输出。

## 功能特点

- ✅ 获取微博实时热搜榜单
- ✅ 支持自定义数量限制
- ✅ 返回热搜排名、标题、分类、热度等信息
- ✅ 支持格式化输出和JSON输出
- ✅ 支持热搜标识（🔥热榜、🆕新榜）
- ✅ 提供模拟数据作为备用

## 使用方法

```bash
# 获取前10条热搜（默认）
python3 skills/weibo-hot-search-list/scripts/weibo_hot_search.py

# 获取前20条热搜
python3 skills/weibo-hot-search-list/scripts/weibo_hot_search.py --limit 20

# 获取并格式化输出
python3 skills/weibo-hot-search-list/scripts/weibo_hot_search.py --limit 15 --format
```

## 返回数据格式

```json
[
  {
    "rank": 1,
    "title": "热搜标题",
    "category": "分类",
    "num": 1234567,
    "is_hot": true,
    "is_new": false
  }
]
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --limit | 获取热搜数量 | 10 |
| --format | 格式化输出 | 否 |

## 注意事项

- 需要安装 Playwright 环境
- 首次使用需安装浏览器：`playwright install chromium`
- 网络异常时会返回模拟数据