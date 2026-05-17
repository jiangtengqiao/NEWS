# 桂林临桂新闻资讯平台 - 系统架构文档

## 一、项目概述

### 1.1 项目名称
**"临桂资讯"** - 桂林市临桂区官方新闻资讯平台

### 1.2 项目定位
打造桂林市临桂区最权威、最全面、最及时的新闻资讯平台，服务于临桂区乃至桂林市全体居民。

### 1.3 核心功能矩阵

#### 1.3.1 用户系统（庞大数据库）
- **邮箱登录系统**
  - 邮箱注册/登录
  - 邮箱验证（发送验证邮件）
  - 邮箱找回密码
  - 邮箱通知订阅
  
- **个人中心**
  - 头像上传（支持JPG、PNG、WebP，最大5MB）
  - 昵称设置（2-20个字符）
  - 性别设置
  - 生日设置
  - 个人简介（500字以内）
  - 联系方式设置
  
- **个人信息码系统**
  - 每个用户生成唯一8位数字码
  - 用于好友添加
  - 二维码展示
  
- **好友系统**
  - 通过信息码添加好友
  - 好友请求管理
  - 好友列表查看
  - 好友私信功能
  
- **私信系统**
  - 实时私信通信
  - 消息已读/未读状态
  - 历史消息查看
  - 消息提醒

#### 1.3.2 支付系统（支付宝+微信）
- **订阅付费模式**
  - 免费用户：可阅读国家时政新闻
  - 付费订阅：解锁全部功能
    - 月度订阅：19.9元/月
    - 年度订阅：199元/年（相当于16.6元/月）
    - 永久会员：599元/永久
  
- **支付功能**
  - 支付宝支付接入
  - 微信支付接入
  - 支付结果回调处理
  - 订单管理系统
  - 发票申请功能

#### 1.3.3 内容系统（庞大新闻数据库）

##### 1.3.3.1 新闻分类
1. **国家时政**（免费）
   - 国家领导人活动
   - 中央政策文件
   - 重要会议报道
   - 人事任免信息

2. **地方政务**（免费）
   - 桂林市新闻
   - 临桂区新闻
   - 各政府部门公告
   - 政务服务信息

3. **社会新闻**（订阅）
   - 热点事件
   - 民生百态
   - 突发新闻
   - 深度报道

4. **经济财经**（订阅）
   - 宏观经济
   - 股市期货
   - 产业动态
   - 投资理财

5. **科技教育**（订阅）
   - 科技创新
   - 教育动态
   - 校园新闻
   - 考试信息

6. **文化体育**（订阅）
   - 文艺演出
   - 体育赛事
   - 旅游资讯
   - 娱乐八卦

7. **健康生活**（订阅）
   - 医疗健康
   - 养生保健
   - 美食推荐
   - 时尚潮流

8. **名人志士演讲**（订阅）
   - 政要演讲
   - 商界领袖演讲
   - 学术报告
   - TED精选

##### 1.3.3.2 新闻功能
- **新闻阅读**
  - 图文新闻
  - 视频新闻（支持多画质）
  - 音频新闻（新闻播报）
  - 直播新闻
  
- **新闻收听**
  - TTS语音播报
  - 多种音色选择
  - 语速调节
  
- **新闻分享**
  - 微信分享
  - 朋友圈分享
  - 微博分享
  - 复制链接

#### 1.3.4 功能系统

##### 1.3.4.1 语言转译
- 支持中文、英文、粤语、广西壮话等
- 实时语音翻译
- 文字翻译
- 字幕翻译

##### 1.3.4.2 画质切换
- 流畅画质（省流量）
- 标清画质（360P）
- 高清画质（720P）
- 超清画质（1080P）
- 蓝光画质（4K）

##### 1.3.4.3 文件下载
- **文档格式**
  - PDF文档下载
  - Word文档下载
  - Excel表格下载
  - PPT演示文稿
  
- **视频格式**
  - MP4视频下载
  - AVI视频下载
  - MKV视频下载
  
- **音频格式**
  - MP3音频下载
  - WAV音频下载
  - M4A音频下载

##### 1.3.4.4 历史记录
- 浏览历史（永久保存）
- 搜索历史
- 下载历史
- 收藏夹

#### 1.3.5 法律合规系统

##### 1.3.5.1 Cookie使用询问
- 首次访问弹出Cookie使用说明
- 功能性Cookie（登录状态等）
- 统计性Cookie（访问分析）
- 营销性Cookie（广告推送）

##### 1.3.5.2 用户协议（五万至八万字）
**完整内容包含但不限于：**
- 服务条款总则
- 用户注册与账号
- 用户使用规范
- 内容发布规范
- 知识产权说明
- 隐私保护政策
- 付费服务条款
- 免责声明
- 争议解决机制
- 协议修改权利
- 其他条款（详细内容见附录）

##### 1.3.5.3 隐私协议（五万至八万字）
**完整内容包含但不限于：**
- 信息收集范围
- 信息使用目的
- 信息存储期限
- 信息共享对象
- 信息保护措施
- 用户权利说明
- 未成年人保护
- 跨境传输说明
- 政策更新机制
- 联系方式（详细）
- 附录：专业术语解释

## 二、技术架构

### 2.1 前端技术栈
- **框架**: Nuxt 3 + Vue 3
- **UI库**: Nuxt UI + Tailwind CSS
- **状态管理**: Pinia
- **HTTP客户端**: $fetch
- **构建工具**: Vite

### 2.2 后端技术栈
- **框架**: FastAPI
- **ORM**: SQLAlchemy
- **数据库**: SQLite（开发）/ PostgreSQL（生产）
- **认证**: JWT Token
- **密码加密**: Bcrypt
- **API文档**: Swagger/OpenAPI

### 2.3 数据库设计

#### 2.3.1 用户相关表
```
users
├── id (UUID, PK)
├── email (VARCHAR, UNIQUE)
├── password_hash (VARCHAR)
├── nickname (VARCHAR)
├── avatar_url (VARCHAR)
├── gender (VARCHAR)
├── birthday (DATE)
├── bio (TEXT)
├── is_verified (BOOLEAN)
├── is_subscribed (BOOLEAN)
├── subscription_type (VARCHAR)  -- free/monthly/yearly/permanent
├── subscription_expire_at (DATETIME)
├── created_at (DATETIME)
└── updated_at (DATETIME)

user_codes
├── id (UUID, PK)
├── user_id (UUID, FK)
├── code (VARCHAR, UNIQUE)  -- 8位数字
├── qr_code (TEXT)  -- Base64二维码
└── created_at (DATETIME)

friendships
├── id (UUID, PK)
├── user_id (UUID, FK)
├── friend_id (UUID, FK)
├── status (VARCHAR)  -- pending/accepted/rejected
└── created_at (DATETIME)

messages
├── id (UUID, PK)
├── sender_id (UUID, FK)
├── receiver_id (UUID, FK)
├── content (TEXT)
├── is_read (BOOLEAN)
└── created_at (DATETIME)
```

#### 2.3.2 新闻相关表
```
news_categories
├── id (UUID, PK)
├── name (VARCHAR, UNIQUE)
├── display_name (VARCHAR)
├── icon (VARCHAR)
├── priority (INT)
└── created_at (DATETIME)

news
├── id (UUID, PK)
├── title (VARCHAR)
├── content (TEXT)
├── summary (TEXT)
├── source (VARCHAR)
├── author (VARCHAR)
├── image_url (VARCHAR)
├── category_id (UUID, FK)
├── tags (TEXT)  -- JSON数组
├── is_premium (BOOLEAN)  -- 是否付费
├── view_count (INT)
├── like_count (INT)
├── comment_count (INT)
├── published_at (DATETIME)
├── created_at (DATETIME)
└── updated_at (DATETIME)

news_comments
├── id (UUID, PK)
├── user_id (UUID, FK)
├── news_id (UUID, FK)
├── content (TEXT)
├── parent_id (UUID, FK)  -- 回复功能
└── created_at (DATETIME)

news_favorites
├── id (UUID, PK)
├── user_id (UUID, FK)
├── news_id (UUID, FK)
└── created_at (DATETIME)

news_reads
├── id (UUID, PK)
├── user_id (UUID, FK)
├── news_id (UUID, FK)
├── read_duration (INT)  -- 阅读时长（秒）
└── created_at (DATETIME)
```

#### 2.3.3 订单相关表
```
orders
├── id (UUID, PK)
├── user_id (UUID, FK)
├── order_no (VARCHAR, UNIQUE)  -- 订单号
├── amount (DECIMAL)
├── payment_method (VARCHAR)  -- alipay/wechat
├── payment_status (VARCHAR)  -- pending/paid/refunded
├── payment_time (DATETIME)
├── subscription_type (VARCHAR)
└── created_at (DATETIME)
```

#### 2.3.4 统计相关表
```
user_activity_stats
├── id (UUID, PK)
├── user_id (UUID, FK)
├── news_read_count (INT)
├── comment_count (INT)
├── like_count (INT)
├── date (DATE)
└── created_at (DATETIME)

daily_stats
├── id (UUID, PK)
├── date (DATE)
├── total_page_views (INT)
├── unique_visitors (INT)
├── new_users (INT)
├── paid_subscriptions (INT)
└── created_at (DATETIME)
```

### 2.4 API接口设计

#### 2.4.1 认证相关
```
POST /api/auth/register          # 用户注册
POST /api/auth/login             # 用户登录
POST /api/auth/logout            # 用户登出
POST /api/auth/refresh           # 刷新Token
GET  /api/auth/me                # 获取当前用户信息
```

#### 2.4.2 用户相关
```
GET  /api/users/{user_id}       # 获取用户信息
PUT  /api/users/me               # 更新个人资料
POST /api/users/me/avatar        # 上传头像
GET  /api/users/me/code          # 获取个人信息码
GET  /api/users/code/{code}      # 通过码查找用户
```

#### 2.4.3 好友相关
```
GET  /api/friends                # 获取好友列表
GET  /api/friends/requests       # 获取好友请求
POST /api/friends/request/{user_id}  # 发送好友请求
PUT  /api/friends/request/{request_id}/accept  # 接受请求
PUT  /api/friends/request/{request_id}/reject   # 拒绝请求
DELETE /api/friends/{friend_id}   # 删除好友
```

#### 2.4.4 私信相关
```
GET  /api/messages                # 获取消息列表
GET  /api/messages/{user_id}      # 获取与某用户的对话
POST /api/messages                # 发送消息
PUT  /api/messages/{message_id}/read  # 标记已读
```

#### 2.4.5 新闻相关
```
GET  /api/news/categories         # 获取分类列表
GET  /api/news                    # 获取新闻列表
GET  /api/news/{news_id}          # 获取新闻详情
POST /api/news/{news_id}/read     # 记录阅读
POST /api/news/{news_id}/like     # 点赞/取消点赞
GET  /api/news/{news_id}/comments # 获取评论
POST /api/news/comments            # 发表评论
POST /api/news/favorites          # 添加收藏
GET  /api/news/favorites          # 获取收藏列表
```

#### 2.4.6 订单相关
```
POST /api/orders/alipay           # 支付宝支付
POST /api/orders/wechat           # 微信支付
GET  /api/orders/{order_id}       # 查询订单状态
GET  /api/orders/history          # 订单历史
```

## 三、部署架构

### 3.1 开发环境
- 前端：localhost:3000
- 后端：localhost:8000
- 数据库：SQLite

### 3.2 生产环境（推荐）
- 前端：Nginx + SSL证书
- 后端：Uvicorn/Gunicorn + 多进程
- 数据库：PostgreSQL
- 缓存：Redis
- 文件存储：七牛云/阿里云OSS

## 四、数据爬取策略

### 4.1 新闻来源
1. **官方政府网站**
   - 中国政府网
   - 广西壮族自治区政府网
   - 桂林市政府网
   - 临桂区政府网

2. **权威媒体**
   - 新华社
   - 人民日报
   - 央视新闻
   - 广西日报
   - 桂林日报

3. **商业平台**
   - 腾讯新闻
   - 今日头条
   - 网易新闻
   - 凤凰网

### 4.2 爬取频率
- 头条新闻：实时爬取（每5分钟）
- 普通新闻：每小时爬取
- 历史新闻：每天更新

### 4.3 数据存储
- 所有新闻永久保存
- 用户行为数据永久保存
- 支持查看历史新闻
- 定期数据备份

## 五、安全合规

### 5.1 数据安全
- 用户密码使用Bcrypt加密
- JWT Token认证
- HTTPS加密传输
- SQL注入防护
- XSS攻击防护
- CSRF防护

### 5.2 隐私保护
- 最小化数据收集
- 数据加密存储
- 定期安全审计
- 用户数据导出功能
- 账号注销功能

### 5.3 内容合规
- 新闻来源审核
- 内容人工审核
- 敏感词过滤
- 违规内容举报
- 版权保护机制

## 六、功能优先级

### Phase 1: 核心功能（已完成基础）
- ✅ 用户注册登录
- ✅ 个人资料管理
- ✅ 新闻分类浏览
- ✅ 新闻详情查看
- ✅ 新闻点赞收藏
- ✅ 评论功能

### Phase 2: 社交功能（进行中）
- ⏳ 个人信息码
- ⏳ 好友系统
- ⏳ 私信功能

### Phase 3: 支付系统
- 🔲 支付宝接入
- 🔲 微信支付接入
- 🔲 订阅管理

### Phase 4: 内容增强
- 🔲 新闻语音播报
- 🔲 语言转译
- 🔲 文件下载
- 🔲 画质切换

### Phase 5: 法律合规
- 🔲 用户协议（五万字）
- 🔲 隐私协议（五万字）
- 🔲 Cookie提示

### Phase 6: 新闻爬取
- 🔲 国家时政爬取
- 🔲 地方新闻爬取
- 🔲 社会热点爬取
- 🔲 名人演讲资源

## 七、桂林临桂区特色功能

### 7.1 地方政务
- 临桂区政策文件库
- 政务服务指南
- 部门联系方式
- 公告通知栏

### 7.2 地方生活
- 临桂旅游攻略
- 美食推荐
- 交通信息
- 天气预报（实时）

### 7.3 地方文化
- 桂林山水介绍
- 临桂历史沿革
- 名人轶事
- 非遗传承

## 八、附录

### 8.1 专业术语解释
- **TTS**: Text-to-Speech，文字转语音
- **OCR**: Optical Character Recognition，光学字符识别
- **CDN**: Content Delivery Network，内容分发网络
- **ORM**: Object Relational Mapping，对象关系映射
- **JWT**: JSON Web Token，JSON网络令牌

### 8.2 参考资料
- 《网络安全法》
- 《个人信息保护法》
- 《互联网新闻信息服务管理规定》
- 字节跳动用户协议
- 腾讯隐私协议
- 微信支付商户文档
- 支付宝开放平台文档

---

**文档版本**: v1.0  
**创建日期**: 2026-05-17  
**最后更新**: 2026-05-17  
**文档状态**: 进行中
