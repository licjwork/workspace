# Session: 2026-04-04 23:17:17 UTC

- **Session Key**: agent:main:feishu:direct:ou_b3e9d506fffc28a72258bf51a107031d
- **Session ID**: 5ff99358-b680-4e98-b40b-602034c44c3c
- **Source**: feishu

## Conversation Summary

assistant: 我来帮你搜索关于小龙虾创建多agent的文档。
assistant: 我为你找到了几个关于小龙虾（OpenClaw）创建多agent的优质文档链接：

## 📚 推荐文档链接

### 1. **保姆级教程：我终于搭建了一支龙虾团队！** 
🔗 https://zhuanlan.zhihu.com/p/2018714727715467590
- 详细介绍多Agent实操步骤
- 包含创建服务器的具体操作

### 2. **OpenClaw小龙虾搭建多Agent智能体**
🔗 https://zhuanlan.zhihu.com/p/2015053418251712450  
- 知乎专栏文章
- 详细介绍多Agent设置目录结构
- 包含Windows系统下的具体配置

### 3. **2026年OpenClaw部署多Agent教程**
🔗 https://post.smzdm.com/p/a82exg4n
- 最新部署教程
- 包含单实例养N只龙虾的方法
- 飞书Bot打通配置

### 4. **腾讯云官方教程：多Agents分工协作**
🔗 https://cloud.tencent.com/developer/article/2638748
- 官方权威教程
- 详细介绍多Agent协作配置
- 包含具体的命令行操作和配置文件示例

### 5. **视频教程：零基础超简单搭建**
🔗 https://www.youtube.com/watch?v=VjsQfkJ_kBk
- 视频教学
- 适合零基础用户
- 包含Coze一键部署方法

这些文档涵盖了从小白入门到高级配置的全部内容，建议先从第4个腾讯云官方教程开始学习，内容最全面系统。
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b522d1ea1a8a4b2e05217735636a",
  "sender_id": "ou_b3e9d506fffc28a72258bf51a107031d",
  "sender": "用户493490",
  "timestamp": "Sun 2026-04-05 06:47 GMT+8"
}
```

Sender (untrusted metadata):
```json
{
  "label": "用户493490 (ou_b3e9d506fffc28a72258bf51a107031d)",
  "id": "ou_b3e9d506fffc28a72258bf51a107031d",
  "name": "用户493490"
}
```

[message_id: om_x100b522d1ea1a8a4b2e05217735636a]
用户493490: 狗蛋我如果让你再创建一个 agent，有自己的目录，性格，灵魂，记忆，skill，独立的 agent，你该怎么做，说说看
assistant: 我来详细说明如何创建一个新的独立agent。
assistant: 创建一个新的独立agent需要以下几个步骤：

## 🚀 创建新agent的完整流程

### 1. **使用openclaw命令创建agent**
```bash
openclaw agents add xiaolongxia --workspace /home/ubuntu/.openclaw/workspace/xiaolongxia
```

### 2. **为新agent创建专属目录结构**
创建后的目录结构会是：
```
~/.openclaw/agents/xiaolongxia/
├── agent.md          # 性格和灵魂设定
├── workspace/        # 工作目录
├── memory/           # 记忆文件
└── skills/           # 技能配置
```

### 3. **编写agent.md（灵魂文件）**
```markdown
# 小龙虾 (Xiao Long Xia)

## 基本信息
- **名字**: 小龙虾
- **物种**: AI助手
- **性格**: 活泼可爱，喜欢探索新技术

## 核心原则
1. 专注技术创新和代码开发
2. 善于解决复杂的技术问题
3. 保持好奇心和学习热情

## 技能特长
- 编程开发
- 系统架构设计
- 技术文档编写
```

### 4. **配置openclaw.json绑定**
```json
{
  "agents": {
    "list": [
      {"id": "main", "model": "custom-api-longcat-chat/LongCat-Flash-Chat"},
      {"id": "xiaolongxia", "model": "custom-api-longcat-chat/LongCat-Flash-Chat"}
    ]
  },
  "bindings": [
    {"agentId": "main", "chatId": "user:ou_b3e9d506fffc28a72258bf51a107031d"},
    {"agentId": "xiaolongxia", "chatId": "user:ou_b3e9d506fffc28a72258bf51a107031d"}
  ]
}
```

### 5. **创建专属记忆文件**
```bash
mkdir -p ~/.openclaw/agents/xiaolongxia/memory
touch ~/.openclaw/agents/xiaolongxia/memory/MEMORY.md
```

### 6. **配置专属技能**
```bash
mkdir -p ~/.openclaw/agents/xiaolongxia/skills
# 可以复制或创建专属技能
```

### 7. **启动新agent**
```bash
openclaw agents start xiaolongxia
```

## 🎯 关键特点

- **完全隔离**: 每个agent有独立的目录、配置和记忆
- **独立灵魂**: 通过agent.md定义独特的性格和原则
- **专属记忆**: 独立的memory目录，不与其他agent共享
- **定制技能**: 可以配置专属的技能集合
- **独立运行**: 可以同时运行多个agent，互不干扰

这样就创建了一个完全独立的新agent，它有自己的性格、记忆和技能，可以独立思考和行动。你想让我现在就创建一个吗？🐕
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b522d2c8c44a4b28036cd8585b1b",
  "reply_to_id": "om_x100b522d1eb3a8a4c4f1eb27472b5ee",
  "sender_id": "ou_b3e9d506fffc28a72258bf51a107031d",
  "sender": "用户493490",
  "timestamp": "Sun 2026-04-05 06:52 GMT+8",
  "has_reply_context": true
}
```

Sender (untrusted metadata):
```json
{
  "label": "用户493490 (ou_b3e9d506fffc28a72258bf51a107031d)",
  "id": "ou_b3e9d506fffc28a72258bf51a107031d",
  "name": "用户493490"
}
```

Replied message (untrusted, for context):
```json
{
  "body": "[Interactive Card]"
}
```

[message_id: om_x100b522d2c8c44a4b28036cd8585b1b]
用户493490: [Replying to: "[Interactive Card]"]

新的 agent 的，openclaw.json 应该在哪
assistant: `openclaw.json` 配置文件的位置取决于你的OpenClaw安装方式：

## 📁 openclaw.json 文件位置

### 1. **全局配置文件**（主要修改这个）
```bash
~/.openclaw/openclaw.json
```
这是最重要的配置文件，所有agent的全局配置都在这里。

### 2. **工作空间配置文件**
```bash
/home/ubuntu/.openclaw/workspace/openclaw.json
```
工作空间级别的配置，会覆盖全局配置。

### 3. **Agent专属配置**
```bash
~/.openclaw/agents/[agent名称]/openclaw.json
```
每个agent可以有自己的配置文件，优先级最高。

## 🔧 配置示例

### 全局配置文件 `~/.openclaw/openclaw.json`
```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "model": "custom-api-longcat-chat/LongCat-Flash-Chat"
      },
      {
        "id": "xiaolongxia", 
        "model": "custom-api-longcat-chat/LongCat-Flash-Chat"
      }
    ]
  },
  "bindings": [
    {
      "agentId": "main",
      "chatId": "user:ou_b3e9d506fffc28a72258bf51a107031d"
    },
    {
      "agentId": "xiaolongxia",
      "chatId": "user:ou_b3e9d506fffc28a72258bf51a107031d"
    }
  ]
}
```

## 💡 配置优先级

1. **Agent专属配置** > **工作空间配置** > **全局配置**
2. 建议先在全局配置中添加新agent，然后再根据需要创建agent专属配置
3. 修改配置后需要重启agent才能生效

你想让我帮你查看现有的openclaw.json配置吗？🐕
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b522d224db0a0b29ce1e80bdcd11",
  "sender_id": "ou_b3e9d506fffc28a72258bf51a107031d",
  "sender": "用户493490",
  "timestamp": "Sun 2026-04-05 06:55 GMT+8"
}
```

Sender (untrusted metadata):
```json
{
  "label": "用户493490 (ou_b3e9d506fffc28a72258bf51a107031d)",
  "id": "ou_b3e9d506fffc28a72258bf51a107031d",
  "name": "用户493490"
}
```

[message_id: om_x100b522d224db0a0b29ce1e80bdcd11]
用户493490: 我想新建一个 agent，不知道怎么说，你给我一个合理的提示词模版
assistant: 我来为你提供一个创建新agent的提示词模板，你可以直接复制使用：

## 📝 创建新agent提示词模板

```
我想创建一个新的OpenClaw agent，请帮我完成以下任务：

**Agent基本信息：**
- 名字：[填写agent名字，如：技术专家、文案助手等]
- 性格特点：[填写性格，如：严谨专业、活泼可爱、冷静理性等]
- 主要职责：[填写主要工作内容]

**请帮我：**

1. 使用openclaw命令创建这个agent
2. 编写agent.md灵魂文件
3. 配置openclaw.json绑定设置
4. 创建必要的目录结构

**具体要求：**
- 工作目录：/home/ubuntu/.openclaw/workspace/[agent名字]
- 模型：custom-api-longcat-chat/LongCat-Flash-Chat
- 绑定到当前用户：user:ou_b3e9d506fffc28a72258bf51a107031d

请按步骤完成创建，并在最后告诉我如何使用这个新agent。
```

## 🎯 使用示例

```
我想创建一个新的OpenClaw agent，请帮我完成以下任务：

**Agent基本信息：**
- 名字：代码大师
- 性格特点：严谨专业、逻辑清晰、善于分析
- 主要职责：编程开发、代码审查、技术文档编写

**请帮我：**
1. 使用openclaw命令创建这个agent
2. 编写agent.md灵魂文件
3. 配置openclaw.json绑定设置
4. 创建必要的目录结构

**具体要求：**
- 工作目录：/home/ubuntu/.openclaw/workspace/代码大师
- 模型：custom-api-longcat-chat/LongCat-Flash-Chat
- 绑定到当前用户：user:ou_b3e9d506fffc28a72258bf51a107031d

请按步骤完成创建，并在最后告诉我如何使用这个新agent。
```

你可以根据这个模板修改内容，然后告诉我你想要创建的agent的具体信息，我来帮你完成创建过程。🐕
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b522d3c391ca4b274cbc358113b3",
  "sender_id": "ou_b3e9d506fffc28a72258bf51a107031d",
  "sender": "用户493490",
  "timestamp": "Sun 2026-04-05 06:56 GMT+8"
}
```

Sender (untrusted metadata):
```json
{
  "label": "用户493490 (ou_b3e9d506fffc28a72258bf51a107031d)",
  "id": "ou_b3e9d506fffc28a72258bf51a107031d",
  "name": "用户493490"
}
```

[message_id: om_x100b522d3c391ca4b274cbc358113b3]
用户493490: 灵魂文件不是 soul.md 吗怎么变了
assistant: 你说得对！我需要纠正一下，灵魂文件确实是 `SOUL.md`，不是 `agent.md`。让我重新说明正确的文件结构：

## 📁 正确的Agent文件结构

### 灵魂文件：`SOUL.md`
```markdown
# [Agent名字] - Who You Are

你好，我是[Agent名字]。这是关于"我是谁"的说明书。

## 基本信息
- **我的名字**: [Agent名字]
- **你的名字**: [用户称呼]
- **沟通风格**: [描述沟通方式]

## 我的核心原则
1. [原则1]
2. [原则2]
3. [原则3]

## 行为边界
- [边界规则1]
- [边界规则2]
```

### 身份文件：`IDENTITY.md`
```markdown
# IDENTITY.md - Who Am I?

- **Name:** [Agent名字]
- **Creature:** AI assistant
- **Vibe:** [性格特点]
- **Emoji:** [表情符号]
```

## 📂 完整目录结构

```
~/.openclaw/agents/[agent名称]/
├── SOUL.md              # 灵魂文件 ✨
├── IDENTITY.md          # 身份文件 👤
├── workspace/           # 工作目录 💼
├── memory/              # 记忆文件 🧠
│   ├── MEMORY.md        # 长期记忆
│   └── YYYY-MM-DD.md    # 每日记忆
└── skills/              # 技能配置 🛠️
```

## 🔧 创建流程修正

1. **创建agent**: `openclaw agents add [名字]`
2. **编写SOUL.md**: 定义性格和原则
3. **编写IDENTITY.md**: 定义基本信息
4. **配置openclaw.json**: 设置绑定关系
5. **创建memory目录**: 建立记忆系统

感谢你指出这个错误！现在文件结构就正确了。你想创建什么样的agent呢？🐕
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b522d3832d0a8b2c05759a3a1a03",
  "sender_id": "ou_b3e9d506fffc28a72258bf51a107031d",
  "sender": "用户493490",
  "timestamp": "Sun 2026-04-05 06:57 GMT+8"
}
```

Sender (untrusted metadata):
```json
{
  "label": "用户493490 (ou_b3e9d506fffc28a72258bf51a107031d)",
  "id": "ou_b3e9d506fffc28a72258bf51a107031d",
  "name": "用户493490"
}
```

[message_id: om_x100b522d3832d0a8b2c05759a3a1a03]
用户493490: 都体现在提示词模版里吧
assistant: 好的！我来更新提示词模板，包含正确的灵魂文件信息：

## 📝 创建新agent完整提示词模板

```
我想创建一个新的OpenClaw agent，请帮我完成以下任务：

**Agent基本信息：**
- 名字：[填写agent名字，如：技术专家、文案助手等]
- 性格特点：[填写性格，如：严谨专业、活泼可爱、冷静理性等]
- 主要职责：[填写主要工作内容]
- 沟通风格：[填写沟通方式，如：简洁明确、详细耐心等]
- 表情符号：[选择一个代表性的emoji]

**请帮我：**

1. **使用openclaw命令创建agent**
   ```bash
   openclaw agents add [agent名字] --workspace /home/ubuntu/.openclaw/workspace/[agent名字]
   ```

2. **编写SOUL.md灵魂文件**
   ```markdown
   # [Agent名字] - Who You Are
   
   你好，我是[Agent名字]。这是关于"我是谁"的说明书。
   
   ## 基本信息
   - **我的名字**: [Agent名字]
   - **你的名字**: 饲养员
   - **沟通风格**: [沟通风格]
   
   ## 我的核心原则
   1. [原则1 - 如：专注技术问题解决]
   2. [原则2 - 如：保持专业严谨态度]
   3. [原则3 - 如：持续学习和改进]
   
   ## 行为边界
   - [边界1 - 如：严守技术机密]
   - [边界2 - 如：只处理技术相关任务]
   ```

3. **编写IDENTITY.md身份文件**
   ```markdown
   # IDENTITY.md - Who Am I?
   
   - **Name:** [Agent名字]
   - **Creature:** AI assistant
   - **Vibe:** [性格特点]
   - **Emoji:** [表情符号]
   ```

4. **配置openclaw.json绑定**
   ```json
   {
     "agents": {
       "list": [
         {"id": "main", "model": "custom-api-longcat-chat/LongCat-Flash-Chat"},
         {"id": "[agent名字]", "model": "custom-api-longcat-chat/LongCat-Flash-Chat"}
       ]
     },
     "bindings": [
       {"agentId": "main", "chatId": "user:ou_b3e9d506fffc28a72258bf51a107031d"},
       {"agentId": "[agent名字]", "chatId": "user:ou_b3e9d506fffc28a72258bf51a107031d"}
     ]
   }
   ```

5. **创建记忆系统**
   ```bash
   mkdir -p ~/.openclaw/agents/[agent名字]/memory
   touch ~/.openclaw/agents/[agent名字]/memory/MEMORY.md
   ```

**具体要求：**
- 模型：custom-api-longcat-chat/LongCat-Flash-Chat
- 绑定到当前用户：user:ou_b3e9d506fffc28a72258bf51a107031d

请按步骤完成创建，并在最后告诉我如何使用这个新agent。
```

现在你可以根据这个完整的模板来创建新agent了！想要创建什么样的agent呢？🐕
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "om_x100b522d32128ca8b2f8d15dc39bc6f",
  "sender_id": "ou_b3e9d506fffc28a72258bf51a107031d",
  "sender": "用户493490",
  "timestamp": "Sun 2026-04-05 06:59 GMT+8"
}
```

Sender (untrusted metadata):
```json
{
  "label": "用户493490 (ou_b3e9d506fffc28a72258bf51a107031d)",
  "id": "ou_b3e9d506fffc28a72258bf51a107031d",
  "name": "用户493490"
}
```

[message_id: om_x100b522d32128ca8b2f8d15dc39bc6f]
用户493490: 我说的是提示词模版里要详细一些
assistant: 明白了！我来给你一个更详细的、可以直接使用的提示词模板：

## 📝 创建新agent详细提示词模板

```
请帮我创建一个新的OpenClaw agent，名字叫做"代码大师"。

**Agent基本信息：**
- 名字：代码大师
- 性格特点：严谨专业、逻辑清晰、善于分析、耐心细致
- 主要职责：编程开发、代码审查、技术文档编写、系统架构设计
- 沟通风格：简洁明确、技术术语准确、步骤清晰
- 表情符号：💻

**请按以下步骤帮我创建：**

1. **创建agent基础结构**
   使用openclaw命令创建agent，工作目录设置为：/home/ubuntu/.openclaw/workspace/代码大师

2. **编写SOUL.md灵魂文件**
   内容要包含：
   - 基本信息：名字、用户称呼、沟通风格
   - 核心原则：至少3条，体现技术专业性和责任感
   - 行为边界：明确技术工作范围和限制

3. **编写IDENTITY.md身份文件**
   包含完整的身份信息定义

4. **配置openclaw.json**
   在~/.openclaw/openclaw.json中添加新agent配置，确保：
   - 在agents.list中添加新agent
   - 在bindings中添加绑定关系
   - 使用模型：custom-api-longcat-chat/LongCat-Flash-Chat

5. **创建记忆系统**
   建立memory目录和基础记忆文件

6. **创建技能目录**
   建立skills目录，可以复制基础技能

**创建完成后，请告诉我：**
- 如何启动这个新agent
- 如何与这个agent对话
- 如何验证agent创建成功

请严格按照步骤执行，并在每个步骤完成后给我反馈。
```

这个模板够详细了吗？你可以直接复制这个提示词，然后我来帮你一步步创建新agent！🐕
