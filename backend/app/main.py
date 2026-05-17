from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, friends, messages, email
from app.core.database import engine, Base
from app.models import user, friendship, message, email_verification

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Customize-News API")

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


@app.get("/")
async def root():
    return {"message": "Welcome to Customize-News API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
