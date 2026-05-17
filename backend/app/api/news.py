from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.user import User
from app.schemas.news import (
    CategoryResponse, CategoryCreate,
    NewsResponse, NewsCreate, NewsUpdate,
    NewsFavoriteResponse, NewsFavoriteCreate,
    NewsReadResponse,
    NewsCommentResponse, NewsCommentCreate
)
from app.services.auth_service import get_current_active_user
from app.services.news_service import NewsService
from app.services.advanced_service import NotificationService, StatsService


router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return NewsService.get_categories(db)


@router.get("/", response_model=List[NewsResponse])
def get_news_list(
    skip: int = 0,
    limit: int = 20,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return NewsService.get_news_list(db, skip=skip, limit=limit, category=category, search=search)


@router.get("/{news_id}", response_model=NewsResponse)
def get_news(news_id: UUID, db: Session = Depends(get_db)):
    news = NewsService.get_news(db, news_id)
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news


@router.post("/{news_id}/read", response_model=NewsReadResponse)
def record_read(
    news_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    read = NewsService.record_read(db, news_id, current_user.id)
    try:
        StatsService.record_activity(db, current_user.id, "news_read")
    except:
        pass
    return read


@router.post("/{news_id}/like")
def toggle_like(
    news_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    liked = NewsService.toggle_like(db, news_id, current_user.id)
    if liked:
        try:
            StatsService.record_activity(db, current_user.id, "like")
        except:
            pass
    return {"liked": liked}


@router.post("/", response_model=NewsResponse)
def create_news(
    news: NewsCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return NewsService.create_news(db, news)


@router.put("/{news_id}", response_model=NewsResponse)
def update_news(
    news_id: UUID,
    news_update: NewsUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    updated = NewsService.update_news(db, news_id, news_update)
    if not updated:
        raise HTTPException(status_code=404, detail="News not found")
    return updated


@router.get("/{news_id}/comments", response_model=List[NewsCommentResponse])
def get_comments(news_id: UUID, db: Session = Depends(get_db)):
    return NewsService.get_comments(db, news_id)


@router.post("/comments", response_model=NewsCommentResponse)
def create_comment(
    comment: NewsCommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    comment = NewsService.create_comment(db, current_user.id, comment)
    try:
        StatsService.record_activity(db, current_user.id, "comment")
    except:
        pass
    return comment


@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    success = NewsService.delete_comment(db, comment_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted"}


@router.get("/favorites", response_model=List[NewsFavoriteResponse])
def get_favorites(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return NewsService.get_favorites(db, current_user.id)


@router.post("/favorites", response_model=NewsFavoriteResponse)
def add_favorite(
    favorite: NewsFavoriteCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return NewsService.add_favorite(db, current_user.id, favorite.news_id)


@router.delete("/favorites/{favorite_id}")
def remove_favorite(
    favorite_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    success = NewsService.remove_favorite(db, favorite_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Favorite not found")
    return {"message": "Favorite removed"}
