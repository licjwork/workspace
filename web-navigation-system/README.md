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
- **API接口**: 10个
- **核心功能**: 分类展示、实时搜索、收藏功能、网站管理、用户系统

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
- 百度、Google、淘宝、regex101、ASCIIFlow、CloudConvert等

#### 💼 工作类（10个）
- GitHub、Stack Overflow、LeetCode、LinkedIn等

#### 📚 学习类（6个）
- 知乎、InfoQ、CSDN等

#### 🎮 娱乐类（7个）
- 哔哩哔哩、YouTube、微博、Dribbble等

## 🚧 开发计划
- [x] 收藏功能（前后端已完成）
- [x] 网站管理界面（已完成）
- [x] 用户系统（已完成）
- [ ] 网站图标上传
- [x] 🐟 敲木鱼小组件（已实现）
- [ ] 智能推荐功能
- [ ] 使用统计和热力图
- [ ] 浏览器扩展

---
**Powered by 狗蛋 🐕**
