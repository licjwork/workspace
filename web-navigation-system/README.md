# 狗蛋导航系统 🐕

## 项目概述
一个完整的网页导航系统，包含前端和后端服务，支持网站分类管理和搜索功能。

## 📊 项目状态
- **网站总数**: 56个
- **分类统计**: 
  - 🤖 AI类: 11个
  - 🛠️ 工具类: 22个
  - 💼 工作类: 10个  
  - 📚 学习类: 6个
  - 🎮 娱乐类: 7个
- **API接口**: 10+
- **核心功能**: 分类展示、实时搜索、收藏功能、网站管理、用户系统、启动后端
./start-backend.sh

# 启动前端  
./start-frontend.sh

# 单独停止
./stop-backend.sh
./stop-frontend.sh
```

### 方式三：手动启动
```bash
# 启动后端服务
cd backend
pip install -r requirements.txt
python run.py

# 启动前端服务
cd frontend
npm install
npm start
```

后端服务将运行在 http://localhost:5000
前端服务将运行在 http://82.156.52.192:8017

访问 http://82.156.52.192:8017 查看导航页面

### 方式四：域名访问（生产环境）
通过Nginx域名访问：https://xiaoliyaooo.ltd/nav/

## 🛠️ 技术栈
- **前端**: Node.js + Express + HTML/CSS/JS
- **后端**: Python + Flask + SQLite
- **数据库**: SQLite

## ✨ 功能特性
- ✅ 网站分类展示（全部/AI/工作/学习/娱乐/工具）
- ✅ 实时搜索功能
- ✅ 响应式设计（支持移动端）
- ✅ 完整的RESTful API
- ✅ 收藏功能（前后端完整实现）
- ✅ 网站管理界面（添加/编辑/删除网站）
- ✅ 用户系统（注册/登录/个性化）
- ✅ 数据库自动初始化
- ✅ 🐟 敲木鱼小组件

## 🚀 快速开始

### 方式一：后台启动（推荐）
```bash
cd web-navigation-system

# 启动全部服务
./start-all.sh

# 查看服务状态
./status.sh

# 停止全部服务
./stop-all.sh
```

### 方式二：单独启动
```bash
# 启动后端
./start-backend.sh

# 启动前端  
./start-frontend.sh

# 单独停止
./stop-backend.sh
./stop-frontend.sh
```

### 方式三：手动启动
```bash
# 启动后端服务
cd backend
pip install -r requirements.txt
python run.py

# 启动前端服务
cd frontend
npm install
npm start
```

后端服务将运行在 http://localhost:5000
前端服务将运行在 http://82.156.52.192:8017

访问 http://82.156.52.192:8017 查看导航页面

## 🔌 核心API接口

### 网站管理
- `GET /api/sites` - 获取网站列表（支持category=all|ai|work|study|entertainment|tools）
- `POST /api/sites` - 添加网站
- `PUT /api/sites/{id}` - 更新网站
- `DELETE /api/sites/{id}` - 删除网站

### 收藏功能
- `POST /api/favorites` - 添加收藏
- `DELETE /api/favorites/{site_id}` - 取消收藏
- `GET /api/favorites` - 获取收藏列表
- `GET /api/favorites/{site_id}` - 检查收藏状态

### 统计信息
- `GET /api/stats` - 获取分类统计
- `GET /api/news` - 获取最新资讯
- `GET /api/weibo/hot` - 获取微博热搜（模拟数据）

### 用户系统
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 用户注销
- `POST /api/auth/verify` - 验证会话

### 木鱼功能
- `GET /api/wooden-fish/user/{id}` - 获取用户木鱼计数
- `POST /api/wooden-fish/user/{id}` - 更新木鱼计数
- `GET /api/wooden-fish/leaderboard` - 获取木鱼排行榜

## 📁 项目结构
```
web-navigation-system/
├── frontend/              # 前端代码
├── backend/               # 后端代码
├── database/             # 数据库文件
└── README.md
```

## 📚 网站分类

#### 🤖 AI类（11个）
- OpenAI、Claude、DeepSeek、ChatGPT、Midjourney、Stable Diffusion、Hugging Face、GitHub Copilot、Google Bard、Microsoft Bing AI、Notion AI

#### 🛠️ 工具类（22个）
- 百度、Google、淘宝、regex101、ASCIIFlow、CloudConvert、Canva、TinyPNG、JSON格式化、URL编码、Base64、MD5加密、QR码生成、时间戳转换、IP查询、Whois查询、端口扫描、Ping测试、Traceroute、DNS查询、SSL证书检查、网站测速

#### 💼 工作类（10个）
- GitHub、Stack Overflow、LeetCode、LinkedIn、Dribbble、Behance、Product Hunt、AngelList、RemoteOK、Glassdoor

#### 📚 学习类（6个）
- 知乎、InfoQ、CSDN、掘金、博客园、Medium

#### 🎮 娱乐类（7个）
- 哔哩哔哩、YouTube、微博、Dribbble、V2EX、Reddit、Hacker News

## 🚧 开发计划
- [x] 收藏功能（前后端已完成）
- [x] 网站管理界面（已完成）
- [x] 用户系统（已完成）
- [ ] 网站图标上传
- [x] 🐟 敲木鱼小组件（已实现）
- [ ] 智能推荐功能
- [ ] 使用统计和热力图
- [ ] 浏览器扩展

## 🔧 配置说明

### Nginx配置
- **域名**: xiaoliyaooo.ltd
- **前端代理**: `/nav/` → `http://127.0.0.1:8017/`
- **后端API**: 通过域名 `xiaoliyaooo.ltd` 访问
- **SSL**: 已配置HTTPS证书
- **CSP**: Content Security Policy已配置

### 前端API配置
- **代理目标**: `xiaoliyaooo.ltd` (端口80)
- **API路径**: `/api/*`
- **CORS**: 已配置Content Security Policy
- **会话支持**: 自动传递X-Session-Token头

### 定时任务
- **执行时间**: 偶数小时 (0,2,4,6...)
- **任务内容**: 国际新闻搜索 + AI翻译 + 飞书推送
- **脚本**: `auto-weibo-format.sh`
- **新闻源**: Tavily API
- **翻译服务**: LongCat AI
- **推送目标**: 飞书私聊 (ou_b3e9d506fffc28a72258bf51a107031d)
- **数据保存**: `backend/news.json` 和 `database/news.json`

### 服务端口
- **前端服务**: 8017 (Node.js Express)
- **后端API**: 5000 (Python Flask)
- **数据库**: SQLite (database/navigation.db)
- **Nginx**: 80/443 (域名访问)

### 日志文件
- **前端日志**: frontend.log
- **后端日志**: backend.log
- **推送日志**: news-push.log

---
**Powered by 狗蛋 🐕**
