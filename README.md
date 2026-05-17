# Customize-News

个性化新闻平台 - 第一阶段完成：用户系统与社交功能

## 项目状态 ✅

**第一阶段核心基础系统已完成！** 包含：
- ✅ 用户认证系统（注册、登录、JWT）
- ✅ 用户资料管理（昵称、头像、个人简介等）
- ✅ 好友系统（好友码、好友请求、好友列表）
- ✅ 私信系统（对话列表、发送消息、消息状态）
- ✅ Cookie 同意功能
- ✅ 完整的后端 API
- ✅ 现代化的前端界面

## 技术栈

### 后端
- **FastAPI** - 现代 Web 框架
- **SQLAlchemy 2.0** - ORM 数据库操作
- **SQLite** - 本地开发数据库（支持 PostgreSQL 生产环境）
- **Pydantic** - 数据验证
- **JWT** - 身份认证

### 前端
- **Nuxt 3** - Vue 3 框架
- **@nuxt/ui** - UI 组件库
- **Pinia** - 状态管理
- **TypeScript** - 类型安全

## 项目结构

```
/workspace/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # 数据验证
│   │   └── services/       # 业务逻辑
│   ├── requirements.txt    # Python 依赖
│   └── .env.example       # 环境变量示例
├── frontend/               # Nuxt 3 前端
│   ├── components/         # Vue 组件
│   ├── composables/        # 组合式函数
│   ├── pages/              # 页面路由
│   ├── stores/             # Pinia 状态
│   └── types/              # TypeScript 类型
└── docs/                   # 项目文档
```

## 快速开始

### 后端启动

后端已经在运行中！访问：
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

如需手动重启：
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # 如需要
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端启动

```bash
cd frontend
npm install
npm run dev
```

然后访问 http://localhost:3000

## 功能说明

### 用户系统
- 注册/登录：邮箱 + 密码
- 个人资料：编辑昵称、头像、性别、生日、个人简介
- 用户码：唯一的好友添加码

### 好友系统
- 添加好友：通过用户码搜索并发送请求
- 好友请求：查看、接受、拒绝请求
- 好友列表：管理所有好友

### 私信系统
- 对话列表：查看所有历史对话
- 发送消息：与好友一对一聊天
- 消息时间：显示消息发送时间

## API 文档

启动后端服务后访问 http://localhost:8000/docs 查看完整的 API 文档和交互式测试界面。

### 主要 API 端点

| 功能 | 端点 | 方法 |
|-----|-----|-----|
| 注册 | /api/auth/register | POST |
| 登录 | /api/auth/login | POST |
| 获取当前用户 | /api/auth/me | GET |
| 更新用户资料 | /api/users/me | PUT |
| 获取用户码 | /api/users/me/code | GET |
| 通过码查找用户 | /api/users/code/{code} | GET |
| 发送好友请求 | /api/friends/request/{friend_id} | POST |
| 接受请求 | /api/friends/request/{request_id}/accept | PUT |
| 发送消息 | /api/messages/ | POST |
| 获取对话 | /api/messages/{user_id} | GET |

## 数据库

项目使用 SQLite（自动创建在 `backend/customize_news.db`），无需额外配置。

如需使用 PostgreSQL：
1. 安装 PostgreSQL
2. 更新 `.env` 中的 `DATABASE_URL`
3. 重启后端服务

## 下一步计划

第二阶段：新闻功能
- 新闻浏览和筛选
- 个性化推荐
- 新闻收藏

第三阶段：高级功能
- 通知系统
- 用户设置
- 数据统计

## 贡献指南

1. 克隆项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 发起 Pull Request