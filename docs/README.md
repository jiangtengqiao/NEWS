# 临桂资讯平台 - 完整功能说明

## 一、项目概述

临桂资讯是桂林市临桂区官方新闻资讯平台，提供权威、及时、全面的新闻资讯服务。

**部署地址**: https://lingui-news.up.railway.app

## 二、已完成的功能

### 1. 用户系统
✅ **邮箱注册登录** - 使用Resend发送6位验证码邮件  
✅ **个人中心** - 头像、昵称、性别、生日、个人简介  
✅ **个人信息码** - 8位数字码，用于好友添加  
✅ **好友系统** - 添加、接受、拒绝、删除好友  
✅ **私信系统** - 好友之间一对一聊天  

### 2. 邮件系统（Resend）
✅ **专业HTML邮件模板** - 包含平台介绍、服务说明、安全提醒  
✅ **6位数字验证码** - 有效期10分钟  
✅ **验证码类型** - 邮箱验证、密码重置  
✅ **自动发送** - 注册时、找回密码时自动触发  

### 3. 支付系统（Stripe）
✅ **Stripe支付集成** - 安全的信用卡支付  
✅ **订阅模式**:
   - 月度订阅：19.9元/月
   - 年度订阅：199元/年  
   - 永久会员：599元/永久
✅ **订单管理** - 创建、支付、退款全流程  
✅ **发票系统** - 普通发票、专用发票  

### 4. 新闻系统
✅ **新闻分类**:
   - 国家时政（免费）
   - 桂林临桂（免费）
   - 社会热点（订阅）
   - 财经商业（订阅）
   - 科技教育（订阅）
   - 体育文化（订阅）
   - 名人演讲（订阅）
   - 健康生活（订阅）

✅ **新闻爬虫** - 自动爬取新华网、桂林市政府等真实来源  
✅ **新闻功能**:
   - 图文新闻
   - 视频新闻（多画质）
   - 音频新闻（语音播报）
   - 评论互动
   - 点赞收藏

### 5. 语言转译系统
✅ **支持语言**:
   - 中文简体
   - 中文繁体
   - 英语、日语、韩语
   - 粤语、广西壮话
   - 法语、德语、西班牙语等

✅ **TTS语音播报** - 多种音色可选

### 6. 画质切换系统
✅ **流畅画质** - 480P（省流量）  
✅ **标清画质** - 720P  
✅ **高清画质** - 1080P  
✅ **超清画质** - 2160P（4K）  

### 7. 文件下载系统
✅ **文档格式**: PDF、Word、Excel、PPT、TXT  
✅ **视频格式**: MP4、AVI、MKV、MOV  
✅ **音频格式**: MP3、WAV、M4A、FLAC  

### 8. 法律文档
✅ **用户协议** - 5万字以上，十篇完整内容  
✅ **隐私政策** - 5万字以上，十篇完整内容  
✅ **Cookie政策** - 功能性、分析性、营销性Cookie管理  

## 三、API接口

### 认证相关
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/logout` - 用户登出
- `GET /api/auth/me` - 获取当前用户

### 邮箱相关（Resend）
- `POST /api/email/send-verification` - 发送验证码邮件
- `POST /api/email/verify` - 验证验证码
- `POST /api/email/resend` - 重发验证码

### 支付相关（Stripe）
- `POST /api/orders/create` - 创建订单
- `POST /api/orders/alipay` - 支付宝支付
- `POST /api/orders/wechat` - 微信支付
- `GET /api/orders/history` - 订单历史

### 好友相关
- `GET /api/friends` - 获取好友列表
- `POST /api/friends/request/{user_id}` - 发送好友请求
- `POST /api/friends/request/{request_id}/accept` - 接受请求
- `POST /api/friends/request/{request_id}/reject` - 拒绝请求
- `DELETE /api/friends/{friend_id}` - 删除好友

### 私信相关
- `GET /api/messages` - 获取消息列表
- `GET /api/messages/{user_id}` - 获取对话
- `POST /api/messages` - 发送消息
- `PUT /api/messages/{message_id}/read` - 标记已读

### 新闻相关
- `GET /api/news/categories` - 获取分类
- `GET /api/news` - 获取新闻列表
- `GET /api/news/{news_id}` - 获取新闻详情
- `POST /api/news/{news_id}/like` - 点赞
- `POST /api/news/favorites` - 收藏
- `GET /api/news/favorites` - 获取收藏列表
- `GET /api/news/{news_id}/comments` - 获取评论
- `POST /api/news/comments` - 发表评论

## 四、部署到Railway

### 1. 环境变量配置

在Railway控制台设置以下环境变量：

```
# 数据库
DATABASE_URL=sqlite:///./lingui_news.db

# 安全
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Resend邮件
RESEND_API_KEY=re_your_resend_api_key

# Stripe支付
STRIPE_SECRET_KEY=sk_live_your_stripe_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# 前端URL
FRONTEND_URL=https://your-app-name.up.railway.app
```

### 2. Resend配置

1. 访问 https://resend.com 注册账号
2. 创建API Key
3. 配置发件域名（需要DNS验证）
4. 在Railway环境变量中设置 `RESEND_API_KEY`

### 3. Stripe配置

1. 访问 https://stripe.com 注册账号
2. 获取API密钥（测试模式/生产模式）
3. 配置Webhook端点
4. 在Railway环境变量中设置密钥

### 4. 部署步骤

```bash
# 安装Railway CLI
npm install -g @railway/cli

# 登录
railway login

# 初始化项目
railway init

# 设置环境变量
railway variables set RESEND_API_KEY=re_your_key
railway variables set STRIPE_SECRET_KEY=sk_live_your_key

# 部署
railway up
```

### 5. 自定义域名（可选）

在Railway控制台添加自定义域名：
- 临桂资讯: www.lingui.cn / lingui.cn
- 解析DNS到Railway提供的地址

## 五、邮件模板预览

用户收到的验证邮件将包含：
1. **专业HTML设计** - 响应式布局，美观大方
2. **6位验证码** - 大字体高亮显示
3. **平台介绍** - 临桂资讯功能特色
4. **服务说明** - 国家时政免费、订阅付费
5. **安全提醒** - 防止诈骗提示
6. **联系方式** - 客服电话、邮箱、地址

## 六、支付流程

### Stripe支付流程
1. 用户选择订阅类型（月度/年度/永久）
2. 点击支付，跳转到Stripe Checkout页面
3. 输入信用卡信息完成支付
4. Stripe Webhook通知支付成功
5. 用户订阅状态自动更新

### 订阅权益
- 月度订阅：19.9元/月 - 解锁全部内容30天
- 年度订阅：199元/年 - 解锁全部内容365天
- 永久会员：599元/永久 - 终身解锁

## 七、新闻来源

### 免费新闻
- 新华网 - 国家时政
- 人民网 - 国家时政
- 中国政府网 - 国家政策
- 桂林市政府网 - 桂林新闻
- 临桂区政府网 - 临桂新闻

### 订阅新闻
- 腾讯新闻 - 社会热点
- 东方财富网 - 财经商业
- 36氪 - 科技教育
- 虎扑体育 - 体育文化

## 八、技术架构

### 后端
- FastAPI - Web框架
- SQLAlchemy - ORM
- SQLite/PostgreSQL - 数据库
- JWT - 认证
- Bcrypt - 密码加密

### 前端
- Nuxt 3 - Vue框架
- Tailwind CSS - 样式
- Pinia - 状态管理
- $fetch - HTTP客户端

### 第三方服务
- Resend - 邮件发送
- Stripe - 支付处理
- Railway - 部署平台

## 九、联系方式

**官方网站**: http://www.lingui.cn  
**客服邮箱**: service@lingui.cn  
**客服电话**: 0773-558XXXX（工作日9:00-18:00）  
**办公地址**: 广西壮族自治区桂林市临桂区致远路1号

---

**© 2026 桂林市临桂区融媒体中心**  
**临桂资讯 - 桂林市临桂区官方新闻资讯平台**
