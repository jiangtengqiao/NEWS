# Customize-News 第一阶段：核心基础系统设计

## 项目概述
- **项目名称：** Customize-News
- **阶段：** 第一阶段（核心基础系统）
- **日期：** 2026-05-17

## 技术选型

### 前端
- **框架：** Vue 3 + Nuxt 3
- **状态管理：** Pinia
- **UI 组件：** Element Plus 或 Naive UI

### 后端
- **框架：** Python 3.11 + FastAPI
- **ORM：** SQLAlchemy 2.0
- **数据库：** PostgreSQL（Render 免费版）
- **缓存：** cachetools（内存缓存，无需 Redis）

### 部署
- **平台：** Render
- **对象存储：** 阿里云 OSS（头像存储）
- **邮件服务：** Resend（免费 3,000 封/月）

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Vue 3 + Nuxt 3)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  登录页  │  │ 注册页   │  │ 个人中心 │  │ Cookie弹窗│   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼ HTTPS
┌─────────────────────────────────────────────────────────────┐
│              Backend (Python 3.11 + FastAPI)                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API 路由层                                           │  │
│  │  - /api/auth/*         (认证)                         │  │
│  │  - /api/users/*        (用户管理)                     │  │
│  │  - /api/email/*        (邮件)                         │  │
│  │  - /api/friends/*      (好友)                         │  │
│  │  - /api/messages/*     (私信)                         │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  业务逻辑层 (Services)                                │  │
│  │  - AuthService        (JWT、密码哈希)                  │  │
│  │  - UserService        (用户CRUD、头像上传)            │  │
│  │  - EmailService       (发送验证码)                    │  │
│  │  - CacheService       (内存缓存 cachetools)           │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  数据层 (SQLAlchemy + PostgreSQL)                     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      外部服务                                 │
│  - 阿里云 OSS (头像存储)                                     │
│  - Resend (邮件发送)                                          │
└─────────────────────────────────────────────────────────────┘
```

## 数据库设计

### 用户表 (users)
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(50),
    avatar_url VARCHAR(500),
    gender VARCHAR(10),
    birthday DATE,
    bio TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    is_subscribed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 用户信息码表 (user_codes)
```sql
CREATE TABLE user_codes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    code VARCHAR(20) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 好友关系表 (friendships)
```sql
CREATE TABLE friendships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    friend_id UUID REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) DEFAULT 'pending', -- pending, accepted, rejected
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, friend_id)
);
```

### 私信表 (messages)
```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id UUID REFERENCES users(id) ON DELETE CASCADE,
    receiver_id UUID REFERENCES users(id) ON DELETE CASCADE, content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 邮件验证码表 (email_verifications)
```sql
CREATE TABLE email_verifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL,
    code VARCHAR(6) NOT NULL,
    type VARCHAR(20) NOT NULL, -- register, login, reset_password
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Cookie 同意记录表 (cookie_consents)
```sql
CREATE TABLE cookie_consents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id VARCHAR(100),
    necessary BOOLEAN DEFAULT TRUE,
    analytics BOOLEAN DEFAULT FALSE,
    marketing BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API 设计

### 认证 API (`/api/auth`)
| 方法 | 路径 | 功能 |
|------|------|------|
| POST | `/register` | 注册用户 |
| POST | `/login` | 登录 |
| POST | `/logout` | 登出 |
| POST | `/refresh` | 刷新 Token |
| GET | `/me` | 获取当前用户信息 |

### 用户 API (`/api/users`)
| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/` | 获取用户列表 |
| GET | `/{user_id}` | 获取用户详情 |
| PUT | `/me` | 更新个人信息 |
| POST | `/me/avatar` | 上传头像 |
| GET | `/me/code` | 获取/生成个人信息码 |
| GET | `/code/{code}` | 通过信息码查找用户 |

### 好友 API (`/api/friends`)
| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/` | 获取好友列表 |
| GET | `/requests` | 获取好友请求 |
| POST | `/request/{user_id}` | 发送好友请求 |
| PUT | `/request/{request_id}/accept` | 接受好友请求 |
| PUT | `/request/{request_id}/reject` | 拒绝好友请求 |

### 私信 API (`/api/messages`)
| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/` | 获取消息列表 |
| GET | `/{user_id}` | 获取与某人的对话 |
| POST | `/` | 发送消息 |
| PUT | `/{message_id}/read` | 标记已读 |

### 邮件 API (`/api/email`)
| 方法 | 路径 | 功能 |
|------|------|------|
| POST | `/send-code` | 发送验证码 |
| POST | `/verify-code` | 验证验证码 |

## 项目目录结构

```
customize-news/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── friends.py
│   │   │   ├── messages.py
│   │   │   └── email.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── friendship.py
│   │   │   ├── message.py
│   │   │   └── email_verification.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── friendship.py
│   │   │   ├── message.py
│   │   │   └── email.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── email_service.py
│   │   │   └── cache_service.py
│   │   └── main.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── components/
│   │   ├── AuthForm.vue
│   │   ├── UserProfile.vue
│   │   ├── CookieConsent.vue
│   │   └── ...
│   ├── pages/
│   │   ├── index.vue
│   │   ├── login.vue
│   │   ├── register.vue
│   │   ├── profile.vue
│   │   └── ...
│   ├── composables/
│   │   ├── useAuth.ts
│   │   └── useUser.ts
│   ├── stores/
│   │   ├── auth.ts
│   │   └── user.ts
│   ├── public/
│   ├── app.vue
│   ├── nuxt.config.ts
│   ├── package.json
│   └── tsconfig.json
├── docs/
│   └── design/
│       └── phase1-core.md
├── render.yaml
├── docker-compose.yml
└── README.md
```

## 部署配置 (Render)

### render.yaml
```yaml
services:
  - type: web
    name: customize-news-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    plan: free
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: customize-news-db
          property: connectionString

  - type: web
    name: customize-news-frontend
    env: static
    buildCommand: cd frontend && npm install && npm run build
    staticPublishPath: frontend/.output/public
    plan: free

databases:
  - name: customize-news-db
    databaseName: customize_news
    user: customize_news
    plan: free
```

### 环境变量 (.env.example)
```env
# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/customize_news

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 邮件服务
EMAIL_BACKEND=resend
RESEND_API_KEY=your-resend-api-key
EMAIL_FROM=noreply@your-domain.com
EMAIL_FROM_NAME=Customize-News

# 阿里云 OSS
OSS_ACCESS_KEY_ID=your-oss-access-key-id
OSS_ACCESS_KEY_SECRET=your-oss-access-key-secret
OSS_BUCKET_NAME=your-oss-bucket-name
OSS_ENDPOINT=oss-cn-guilin.aliyuncs.com
OSS_REGION=cn-guilin
```

## 安全考虑

1. **密码安全：** 使用 bcrypt 进行密码哈希
2. **JWT 认证：** 使用 HS256 算法，设置合理过期时间
3. **CORS：** 配置正确的 CORS 策略
4. **SQL 注入防护：** 使用 SQLAlchemy ORM
5. **XSS 防护：** 前端对用户输入进行转义
6. **Cookie 安全：** HttpOnly、Secure、SameSite 属性

## 下一步

- 实施第一阶段核心基础系统
- 进行测试
- 部署到 Render
