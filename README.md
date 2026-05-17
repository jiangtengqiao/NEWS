# Customize-News

个性化新闻平台

## 项目结构

- `backend/` - FastAPI 后端
- `frontend/` - Nuxt 3 前端
- `docs/` - 文档

## 本地开发

### 使用 Docker Compose

```bash
docker-compose up
```

### 手动启动

#### 后端

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### 前端

```bash
cd frontend
npm install
npm run dev
```