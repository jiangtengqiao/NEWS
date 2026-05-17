from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, friends, messages, email, news as news_api, advanced
from app.api.orders import router as orders_router
from app.api.social import router as social_router, msg_router as messages_router
from app.core.database import engine, Base, SessionLocal
from app.models import user, friendship, message, email_verification, news as news_models, advanced as advanced_models
from app.models import user_extended
from app.schemas.news import NewsCreate, CategoryCreate
from app.services.news_service import NewsService
from app.services.news_spider import initialize_news_spider

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="桂林临桂资讯平台 API", version="1.0.0", description="桂林市临桂区官方新闻资讯平台")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(friends.router)
app.include_router(messages.router)
app.include_router(email.router)
app.include_router(news_api.router)
app.include_router(advanced.router)
app.include_router(orders_router)
app.include_router(social_router)
app.include_router(messages_router)


def init_sample_data():
    db = SessionLocal()
    try:
        if not NewsService.get_categories(db):
            categories = [
                {"name": "technology", "display_name": "科技", "icon": "fa-laptop", "priority": 10},
                {"name": "business", "display_name": "商业", "icon": "fa-chart-line", "priority": 9},
                {"name": "health", "display_name": "健康", "icon": "fa-heartbeat", "priority": 8},
                {"name": "sports", "display_name": "体育", "icon": "fa-futbol", "priority": 7},
                {"name": "entertainment", "display_name": "娱乐", "icon": "fa-star", "priority": 6},
            ]
            for cat in categories:
                NewsService.create_category(db, CategoryCreate(**cat))
        
        if not NewsService.get_news_list(db, limit=1):
            sample_news = [
                {
                    "title": "AI 时代的到来：如何改变我们的生活",
                    "summary": "人工智能正在迅速改变各个行业，从医疗到教育，无所不在。",
                    "content": "人工智能（AI）正在以前所未有的速度改变我们的世界。本文将探讨AI如何在医疗、教育、交通等领域带来革命性的变化...",
                    "source": "Tech Daily",
                    "author": "张明",
                    "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800",
                    "category": "technology",
                    "tags": ["AI", "科技", "未来"]
                },
                {
                    "title": "2024年经济形势展望：机遇与挑战",
                    "summary": "全球经济正处于关键转折点，新兴市场将迎来新的发展机遇。",
                    "content": "随着疫情的逐渐缓解，全球经济进入了新的发展阶段。2024年，我们将看到更多的投资机会，同时也需要应对通胀、供应链等挑战...",
                    "source": "Finance Weekly",
                    "author": "李华",
                    "image_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
                    "category": "business",
                    "tags": ["经济", "投资", "2024"]
                },
                {
                    "title": "健康生活指南：运动与饮食的完美平衡",
                    "summary": "科学研究表明，适度的运动加上均衡的饮食是保持健康的关键。",
                    "content": "想要保持健康的身体，运动和饮食两者缺一不可。本文将为您详细介绍如何制定科学的锻炼计划和健康的饮食方案...",
                    "source": "Health Today",
                    "author": "王医生",
                    "image_url": "https://images.unsplash.com/photo-1461896836934-ffe607ba821?w=800",
                    "category": "health",
                    "tags": ["健康", "运动", "饮食"]
                },
                {
                    "title": "世界杯回顾：那些令人难忘的瞬间",
                    "summary": "从经典进球到史诗般的比赛，世界杯带给我们无数美好的回忆。",
                    "content": "世界杯作为全球最受欢迎的体育赛事，每一届都有许多令人难忘的瞬间。让我们一起回顾那些激动人心的时刻...",
                    "source": "Sports World",
                    "author": "体育评论员",
                    "image_url": "https://images.unsplash.com/photo-1461896836934-ffe607ba821?w=800",
                    "category": "sports",
                    "tags": ["足球", "世界杯", "体育"]
                }
            ]
            for news_data in sample_news:
                NewsService.create_news(db, NewsCreate(**news_data))
    finally:
        db.close()


init_sample_data()


@app.get("/")
async def root():
    return {"message": "Welcome to Customize-News API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
