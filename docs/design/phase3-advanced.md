# Customize-News 第三阶段：高级功能设计

## 阶段概述
- **项目名称：** Customize-News
- **阶段：** 第三阶段（高级功能）
- **日期：** 2026-05-17

## 功能特性

### 通知系统
- 实时通知（好友请求、新消息、评论、点赞）
- 通知标记已读
- 通知历史记录
- 推送通知（可选）

### 用户设置
- 个人设置（通知偏好、隐私设置）
- 账户设置（邮箱、密码修改）
- 数据导出
- 账户删除

### 数据统计
- 用户活动统计
- 阅读统计
- 互动统计
- 数据可视化

## 数据库设计

#### 通知表 (notifications)
```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- friend_request, message, comment, like
    title VARCHAR(255) NOT NULL,
    content TEXT,
    related_id UUID,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 用户设置表 (user_settings)
```sql
CREATE TABLE user_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    email_notifications BOOLEAN DEFAULT TRUE,
    push_notifications BOOLEAN DEFAULT TRUE,
    public_profile BOOLEAN DEFAULT TRUE,
    allow_friend_requests BOOLEAN DEFAULT TRUE,
    show_online_status BOOLEAN DEFAULT TRUE,
    language VARCHAR(20) DEFAULT 'zh-CN',
    theme VARCHAR(20) DEFAULT 'light',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 用户活动统计表 (user_activity_stats)
```sql
CREATE TABLE user_activity_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    news_read_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    friend_request_count INTEGER DEFAULT 0,
    message_count INTEGER DEFAULT 0,
    UNIQUE(user_id, date)
);
```

## API 设计

### 通知 API (`/api/notifications`)
| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/` | 获取通知列表 |
| PUT | `/{notification_id}/read` | 标记已读 |
| PUT | `/read-all` | 全部标记已读 |
| DELETE | `/{notification_id}` | 删除通知 |

### 设置 API (`/api/settings`)
| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/` | 获取用户设置 |
| PUT | `/` | 更新设置 |

### 统计 API (`/api/stats`)
| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/user` | 获取用户活动统计 |
| GET | `/reading` | 获取阅读统计 |
