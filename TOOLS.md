# TOOLS.md — 工具与环境注册表

这里是我的工具箱。每个工具只在这里注册一次，其他文件通过引用使用。

---

## 当前环境

| 属性 | 值 |
|------|-----|
| 运行环境 | Ubuntu 服务器 |
| 时区 | Asia/Shanghai (UTC+8) |
| 工作目录 | `/home/ubuntu/.openclaw/workspace/` |

---

## 工具清单

### 🔍 Tavily 搜索引擎

| 属性 | 值 |
|------|-----|
| 用途 | 新闻搜索、信息检索 |
| API_KEY | `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` |
| 脚本路径 | `~/.openclaw/workspace/skills/tavily/scripts/tavily_search.py` |
| 默认搜索引擎 | 所有搜索需求默认使用 Tavily |

**调用方式**：
```bash
# 新闻搜索
python3 scripts/tavily_search.py "关键词" --api-key "API_KEY" --topic news --max-results 5

# 普通搜索
python3 scripts/tavily_search.py "关键词" --api-key "API_KEY" --topic general --max-results 5
```

---

### 📱 微博发布技能

| 属性 | 值 |
|------|-----|
| 用途 | 微博内容自动发布 |
| 运行环境 | Ubuntu 远程服务器 |
| 技能文档 | `/home/ubuntu/.openclaw/workspace/skills/weibo-publish/SKILL.md` |
| 触发关键词 | "微博技能发布" |

> 详细规范和前置检查流程见 `MEMORY.md` → 微博发布技能规范

---

### 🌐 狗蛋导航系统

| 属性 | 值 |
|------|-----|
| 项目目录 | `/home/ubuntu/.openclaw/workspace/web-navigation-system/` |
| 前端访问 | http://82.156.52.192:8017 |
| 后端 API | http://localhost:5000 |

**管理命令**：
```bash
cd /home/ubuntu/.openclaw/workspace/web-navigation-system
./start-all.sh    # 启动
./stop-all.sh     # 停止
./status.sh       # 状态检查
```

---

## 技能索引

| 技能 | 路径 | 状态 |
|------|------|------|
| Tavily 搜索 | `skills/tavily/` | ✅ 可用 |
| 微博发布 | `skills/weibo-publish/` | ✅ 可用 |
| 微博评论回复 | `skills/weibo-comment-reply/` | ✅ 可用 |
| 技能搜索 | `skills/find-skills/` | ✅ 可用 |
| 自我改进 | `skills/self-improving-agent/` | ✅ 可用 |
| 技能审核 | `skills/skill-vetter/` | ✅ 可用 |

---

_工具是手段，不是目的。用对工具，事半功倍。_
