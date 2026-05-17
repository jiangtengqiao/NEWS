import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Date, Boolean, func
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.user import GUID


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    related_id = Column(GUID())
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    
    # 关系
    user = relationship("User", back_populates="notifications")


class UserSetting(Base):
    __tablename__ = "user_settings"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    public_profile = Column(Boolean, default=True)
    allow_friend_requests = Column(Boolean, default=True)
    show_online_status = Column(Boolean, default=True)
    language = Column(String(20), default='zh-CN')
    theme = Column(String(20), default='light')
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # 关系
    user = relationship("User", back_populates="settings", uselist=False)


class UserActivityStat(Base):
    __tablename__ = "user_activity_stats"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    news_read_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    friend_request_count = Column(Integer, default=0)
    message_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    
    # 关系
    user = relationship("User", back_populates="activity_stats")
