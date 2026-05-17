import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Date, Text, DateTime, Integer, DECIMAL, ForeignKey
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.orm import relationship
from app.core.database import Base


class GUID(TypeDecorator):
    """Platform-independent GUID type."""
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            from sqlalchemy.dialects.postgresql import UUID as PGUUID
            return dialect.type_descriptor(PGUUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class User(Base):
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    nickname = Column(String(50), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    gender = Column(String(10), nullable=True)
    birthday = Column(Date, nullable=True)
    bio = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    location = Column(String(200), nullable=True)
    
    is_verified = Column(Boolean, default=False)
    is_subscribed = Column(Boolean, default=False)
    subscription_type = Column(String(20), default='free')  # free/monthly/yearly/permanent
    subscription_expire_at = Column(DateTime, nullable=True)
    
    # 语言偏好
    preferred_language = Column(String(10), default='zh-CN')
    audio_quality = Column(String(10), default='high')  # low/medium/high/ultra
    
    # 统计
    total_read_time = Column(Integer, default=0)  # 秒
    total_downloads = Column(Integer, default=0)
    total_shares = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime, nullable=True)

    # 关系
    user_code = relationship("UserCode", back_populates="user", uselist=False, cascade="all, delete-orphan")
    friendships_as_user = relationship("Friendship", foreign_keys="Friendship.user_id", back_populates="user", cascade="all, delete-orphan")
    friendships_as_friend = relationship("Friendship", foreign_keys="Friendship.friend_id", back_populates="friend", cascade="all, delete-orphan")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender", cascade="all, delete-orphan")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver", cascade="all, delete-orphan")
    email_verifications = relationship("EmailVerification", back_populates="user", cascade="all, delete-orphan")
    
    # 新闻相关
    favorites = relationship("NewsFavorite", back_populates="user", cascade="all, delete-orphan")
    news_reads = relationship("NewsRead", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("NewsComment", back_populates="user", cascade="all, delete-orphan")
    
    # 订单
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    
    # 统计
    activity_stats = relationship("UserActivityStat", back_populates="user", cascade="all, delete-orphan")
