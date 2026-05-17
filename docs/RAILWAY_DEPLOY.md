# Railway 部署指南

## 已配置完成！现在可以部署到 Railway 了。

## 部署步骤

### 1. 准备代码仓库

确保你的代码已经推送到 GitHub/GitLab 仓库。

### 2. 在 Railway 创建项目

1. 访问 [railway.app](https://railway.app)
2. 点击 "New Project"
3. 选择 "Deploy from repo"
4. 选择你的 GitHub/GitLab 仓库
5. 选择分支选择 `main` 或 `master`

### 3. 配置环境变量

在 Railway 项目设置中添加以下环境变量：

```bash
# 必需配置
DATABASE_URL=sqlite:///./lingui_news.db
SECRET_KEY=your-random-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
RESEND_API_KEY=re_5wjazCJy_HxHdrWeYsuQJrwVHUjGVEkm4
FRONTEND_URL=https://lingui-news.up.railway.app
```

**重要：**
- 请修改 `SECRET_KEY` 为随机字符串
- `RESEND_API_KEY` 已配置为你提供的 key

### 4. 部署

点击 "Deploy" 按钮开始部署。Railway 会自动：
- 检测到 `railway.json` 配置
- 安装 Node.js 和 Python 环境
- 构建前端
- 启动后端服务

### 5. 访问你的网站

部署成功后，你的网站将可以通过以下地址访问：
- 默认域名：`https://lingui-news.up.railway.app`
- 或你在 Railway 项目中配置的域名

## 项目配置说明

### railway.json 配置

- **buildCommand: 先构建前端，再复制到后端目录
- **startCommand: 启动 FastAPI 后端
- **frontend_dist: 前端构建产物由 FastAPI 提供服务

### 数据库

当前使用 SQLite，适合开发测试。如果需要 PostgreSQL，可以在 Railway 中添加 PostgreSQL 插件。

## 功能说明

✅ 邮箱验证（Resend 真实邮件）
✅ 用户注册/登录
✅ 新闻浏览
✅ 好友系统
✅ 私信聊天
✅ 用户协议和隐私政策
⚠️ 支付功能（模拟版）

## 注意事项

1. **支付功能：目前是模拟版本，真实支付宝/微信支付需要：
   - 营业执照
   - 备案域名
   - 支付宝/微信商户号

2. **Resend 邮件：当前使用测试域名 `onboarding@resend.dev`，只能发送到你在 Resend 验证过的邮箱。如需发送到任意邮箱，需要在 Resend 添加并验证你自己的域名。

3. **数据持久化**：Railway 的文件系统是临时的，每次部署会重置。如需持久化数据，建议使用 Railway PostgreSQL 数据库。

