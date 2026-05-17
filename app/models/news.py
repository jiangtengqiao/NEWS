import uuid
import json
from datetime import datetime
from typing import List
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Date, Boolean, func
from sqlalchemy.orm import relationship, validates
from app.core.database import Base
from app.models.user import GUID


class Category(Base):
    __tablename__ = "categories"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    name = Column(String(50), unique=True, nullable=False)
    display_name = Column(String(50), nullable=False)
    icon = Column(String(100))
    priority = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())


class News(Base):
    __tablename__ = "news"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    summary = Column(Text)
    source = Column(String(255))
    author = Column(String(255))
    image_url = Column(String(500))
    category = Column(String(50))
    _tags = Column(Text, name="tags")
    published_at = Column(DateTime, default=func.now())
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关系
    comments = relationship("NewsComment", back_populates="news", cascade="all, delete-orphan")
    favorites = relationship("NewsFavorite", back_populates="news", cascade="all, delete-orphan")
    reads = relationship("NewsRead", back_populates="news", cascade="all, delete-orphan")
    
    @property
    def tags(self) -> List[str]:
        if not self._tags:
            return []
        try:
            return json.loads(self._tags)
        except:
            return []
    
    @tags.setter
    def tags(self, value: List[str]):
        if value is None:
            self._tags = None
        else:
            self._tags = json.dumps(value, ensure_ascii=False)
    
    @validates("_tags")
    def validate_tags(self, key, value):
        if value is None:
            return None
        if isinstance(value, list):
            return json.dumps(value, ensure_ascii=False)
        return value


class NewsFavorite(Base):
    __tablename__ = "news_favorites"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    news_id = Column(GUID(), ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # 关系
    user = relationship("User", back_populates="favorites")
    news = relationship("News", back_populates="favorites")
    
    __table_args__ = (
        {'sqlite_autoincrement': True,},
    )


class NewsRead(Base):
    __tablename__ = "news_reads"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    news_id = Column(GUID(), ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    read_at = Column(DateTime, default=func.now())
    read_duration = Column(Integer)
    
    # 关系
    user = relationship("User", back_populates="news_reads")
    news = relationship("News", back_populates="reads")


class NewsComment(Base):
    __tablename__ = "news_comments"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    news_id = Column(GUID(), ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    parent_comment_id = Column(GUID(), ForeignKey("news_comments.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=func.now())
    
    # 关系
    user = relationship("User", back_populates="comments")
    news = relationship("News", back_populates="comments")
    replies = relationship("NewsComment", backref="parent_comment", remote_side=[id])


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(GUID(), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    preference_score = Column(Integer, default=0)
    
    # 关系
    user = relationship("User", back_populates="preferences")
    category = relationship("Category")
