from typing import Optional, List
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.models.news import Category, News, NewsFavorite, NewsRead, NewsComment, UserPreference
from app.schemas.news import (
    CategoryCreate, NewsCreate, NewsUpdate,
    NewsFavoriteCreate, NewsReadCreate, NewsCommentCreate, UserPreferenceCreate
)


class NewsService:
    @staticmethod
    def get_categories(db: Session) -> List[Category]:
        return db.query(Category).order_by(Category.priority.desc()).all()
    
    @staticmethod
    def create_category(db: Session, category: CategoryCreate) -> Category:
        db_category = Category(**category.model_dump())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    
    @staticmethod
    def get_news_list(
        db: Session, 
        skip: int = 0, 
        limit: int = 20,
        category: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[News]:
        query = db.query(News)
        if category:
            query = query.filter(News.category == category)
        if search:
            query = query.filter(News.title.ilike(f"%{search}%") | News.summary.ilike(f"%{search}%"))
        return query.order_by(News.published_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_news(db: Session, news_id: UUID) -> Optional[News]:
        return db.query(News).filter(News.id == news_id).first()
    
    @staticmethod
    def create_news(db: Session, news: NewsCreate) -> News:
        db_news = News(**news.model_dump())
        db.add(db_news)
        db.commit()
        db.refresh(db_news)
        return db_news
    
    @staticmethod
    def update_news(db: Session, news_id: UUID, news_update: NewsUpdate) -> Optional[News]:
        db_news = NewsService.get_news(db, news_id)
        if not db_news:
            return None
        update_data = news_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_news, field, value)
        db.commit()
        db.refresh(db_news)
        return db_news
    
    @staticmethod
    def record_read(db: Session, news_id: UUID, user_id: UUID) -> NewsRead:
        db_news = NewsService.get_news(db, news_id)
        if db_news:
            db_news.view_count += 1
        
        existing = db.query(NewsRead).filter(
            NewsRead.news_id == news_id, 
            NewsRead.user_id == user_id
        ).first()
        if existing:
            existing.read_at = datetime.utcnow()
            db.commit()
            db.refresh(existing)
            return existing
        
        db_read = NewsRead(news_id=news_id, user_id=user_id)
        db.add(db_read)
        db.commit()
        db.refresh(db_read)
        return db_read
    
    @staticmethod
    def toggle_like(db: Session, news_id: UUID, user_id: UUID) -> bool:
        existing = db.query(NewsFavorite).filter(
            NewsFavorite.news_id == news_id, 
            NewsFavorite.user_id == user_id
        ).first()
        
        db_news = NewsService.get_news(db, news_id)
        if not db_news:
            return False
        
        if existing:
            db.delete(existing)
            db_news.like_count -= 1
            liked = False
        else:
            favorite = NewsFavorite(news_id=news_id, user_id=user_id)
            db.add(favorite)
            db_news.like_count += 1
            liked = True
        
        db.commit()
        return liked
    
    @staticmethod
    def get_favorites(db: Session, user_id: UUID) -> List[NewsFavorite]:
        return db.query(NewsFavorite).filter(NewsFavorite.user_id == user_id).order_by(NewsFavorite.created_at.desc()).all()
    
    @staticmethod
    def add_favorite(db: Session, user_id: UUID, news_id: UUID) -> NewsFavorite:
        favorite = NewsFavorite(user_id=user_id, news_id=news_id)
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        return favorite
    
    @staticmethod
    def remove_favorite(db: Session, favorite_id: UUID, user_id: UUID) -> bool:
        favorite = db.query(NewsFavorite).filter(
            NewsFavorite.id == favorite_id, 
            NewsFavorite.user_id == user_id
        ).first()
        if favorite:
            db.delete(favorite)
            db.commit()
            return True
        return False
    
    @staticmethod
    def get_comments(db: Session, news_id: UUID) -> List[NewsComment]:
        return db.query(NewsComment).filter(
            NewsComment.news_id == news_id,
            NewsComment.parent_comment_id.is_(None)
        ).order_by(NewsComment.created_at.desc()).all()
    
    @staticmethod
    def create_comment(db: Session, user_id: UUID, comment: NewsCommentCreate) -> NewsComment:
        db_comment = NewsComment(user_id=user_id, **comment.model_dump())
        db.add(db_comment)
        
        db_news = NewsService.get_news(db, comment.news_id)
        if db_news:
            db_news.comment_count += 1
        
        db.commit()
        db.refresh(db_comment)
        return db_comment
    
    @staticmethod
    def delete_comment(db: Session, comment_id: UUID, user_id: UUID) -> bool:
        comment = db.query(NewsComment).filter(
            NewsComment.id == comment_id, 
            NewsComment.user_id == user_id
        ).first()
        if comment:
            db_news = NewsService.get_news(db, comment.news_id)
            if db_news:
                db_news.comment_count -= 1
            db.delete(comment)
            db.commit()
            return True
        return False
