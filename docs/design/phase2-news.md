# Customize-News 第二阶段：新闻系统设计

## 阶段概述
- **项目名称：** Customize-News
- **阶段：** 第二阶段（新闻系统）
- **日期：** 2026-05-17

## 功能特性

### 新闻浏览
- 新闻列表展示（分页）
- 新闻详情页
- 按类别筛选
- 按关键词搜索
- 热门新闻推荐

### 个性化新闻
- 用户新闻偏好设置
- 基于兴趣的新闻推荐
- 阅读历史记录
- 喜欢/收藏新闻

### 新闻互动
- 评论系统
- 分享功能
- 阅读统计

## 技术设计

### 数据库设计

#### 新闻表 (news)
```sql
CREATE TABLE news (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    summary TEXT,
    source VARCHAR(255),
    author VARCHAR(255),
    image_url VARCHAR(500),
    category VARCHAR(50),
    tags TEXT[],
    published_at TIMESTAMP,
    view_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 新闻分类表 (categories)
```sql
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(50) NOT NULL,
    icon VARCHAR(100),
    priority INTEGER DEFAULT 0
);
```

#### 用户新闻偏好表 (user_preferences)
```sql
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    category_id UUID REFERENCES categories(id) ON DELETE CASCADE,
    preference_score INTEGER DEFAULT 0,
    UNIQUE(user_id, category_id)
);
```

#### 新闻收藏表 (news_favorites)
```sql
CREATE TABLE news_favorites (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    news_id UUID REFERENCES news(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, news_id)
);
```

#### 新闻阅读历史表 (news_reads)
```sql
CREATE TABLE news_reads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    news_id UUID REFERENCES news(id) ON DELETE CASCADE,
    read_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    read_duration INTEGER,
    UNIQUE(user_id, news_id)
);
```

#### 新闻评论表 (news_comments)
```sql
CREATE TABLE news_comments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    news_id UUID REFERENCES news(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    parent_comment_id UUID REFERENCES news_comments(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API 设计

### 新闻 API (`/api/news`)
| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/` | 获取新闻列表（分页、筛选） |
| GET | `/{news_id}` | 获取新闻详情 |
| POST | `/{news_id}/read` | 记录阅读 |
| POST | `/{news_id}/like` | 点赞/取消点赞 |
| GET | `/categories` | 获取新闻分类 |

### 收藏 API (`/api/favorites`)
| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/` | 获取收藏列表 |
| POST | `/` | 添加收藏 |
| DELETE | `/{favorite_id}` | 取消收藏 |

### 评论 API (`/api/comments`)
| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/news/{news_id}` | 获取新闻评论 |
| POST | `/` | 发表评论 |
| DELETE | `/{comment_id}` | 删除评论 |
