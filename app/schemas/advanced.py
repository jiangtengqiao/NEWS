from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel
from uuid import UUID


class NotificationBase(BaseModel):
    type: str
    title: str
    content: Optional[str] = None
    related_id: Optional[UUID] = None


class NotificationCreate(NotificationBase):
    user_id: UUID


class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None


class NotificationResponse(NotificationBase):
    id: UUID
    user_id: UUID
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserSettingBase(BaseModel):
    email_notifications: bool = True
    push_notifications: bool = True
    public_profile: bool = True
    allow_friend_requests: bool = True
    show_online_status: bool = True
    language: str = 'zh-CN'
    theme: str = 'light'


class UserSettingUpdate(BaseModel):
    email_notifications: Optional[bool] = None
    push_notifications: Optional[bool] = None
    public_profile: Optional[bool] = None
    allow_friend_requests: Optional[bool] = None
    show_online_status: Optional[bool] = None
    language: Optional[str] = None
    theme: Optional[str] = None


class UserSettingResponse(UserSettingBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserActivityStatBase(BaseModel):
    date: date
    news_read_count: int = 0
    comment_count: int = 0
    like_count: int = 0
    friend_request_count: int = 0
    message_count: int = 0


class UserActivityStatCreate(UserActivityStatBase):
    user_id: UUID


class UserActivityStatResponse(UserActivityStatBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
