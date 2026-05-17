from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID


class CategoryBase(BaseModel):
    name: str
    display_name: str
    icon: Optional[str] = None
    priority: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class NewsBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None
    source: Optional[str] = None
    author: Optional[str] = None
    image_url: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None


class NewsCreate(NewsBase):
    pass


class NewsUpdate(NewsBase):
    title: Optional[str] = None
    content: Optional[str] = None


class NewsResponse(NewsBase):
    id: UUID
    published_at: datetime
    view_count: int
    like_count: int
    comment_count: int
    created_at: datetime
    updated_at: datetime
    tags: Optional[List[str]] = None
    
    class Config:
        from_attributes = True
    
    @classmethod
    def model_validate(cls, obj, **kwargs):
        if hasattr(obj, "tags"):
            return super().model_validate(obj, **kwargs)
        data = {
            "id": obj.id,
            "title": obj.title,
            "content": obj.content,
            "summary": obj.summary,
            "source": obj.source,
            "author": obj.author,
            "image_url": obj.image_url,
            "category": obj.category,
            "published_at": obj.published_at,
            "view_count": obj.view_count,
            "like_count": obj.like_count,
            "comment_count": obj.comment_count,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at,
            "tags": obj.tags if hasattr(obj, "tags") else []
        }
        return cls(**data)


class NewsFavoriteBase(BaseModel):
    pass


class NewsFavoriteCreate(BaseModel):
    news_id: UUID


class NewsFavoriteResponse(BaseModel):
    id: UUID
    user_id: UUID
    news_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True


class NewsReadBase(BaseModel):
    read_duration: Optional[int] = None


class NewsReadCreate(NewsReadBase):
    pass


class NewsReadResponse(NewsReadBase):
    id: UUID
    user_id: UUID
    news_id: UUID
    read_at: datetime
    
    class Config:
        from_attributes = True


class NewsCommentBase(BaseModel):
    content: str


class NewsCommentCreate(NewsCommentBase):
    news_id: UUID
    parent_comment_id: Optional[UUID] = None


class NewsCommentResponse(NewsCommentBase):
    id: UUID
    user_id: UUID
    news_id: UUID
    parent_comment_id: Optional[UUID] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserPreferenceBase(BaseModel):
    preference_score: int = 0


class UserPreferenceCreate(BaseModel):
    category_id: UUID
    preference_score: int = 0


class UserPreferenceResponse(BaseModel):
    id: UUID
    user_id: UUID
    category_id: UUID
    preference_score: int
    
    class Config:
        from_attributes = True
