import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, Date, Text, DateTime, Integer, ForeignKey, DECIMAL
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.orm import relationship
from app.core.database import Base


class GUID(TypeDecorator):
    """Platform-independent GUID type."""
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID(as_uuid=True))
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


class UserCode(Base):
    __tablename__ = "user_codes"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    code = Column(String(8), unique=True, nullable=False, index=True)
    qr_code = Column(Text, nullable=True)
    scan_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="user_code")


class Friendship(Base):
    __tablename__ = "friendships"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    friend_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), default='pending')  # pending/accepted/rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id], back_populates="friendships_as_user")
    friend = relationship("User", foreign_keys=[friend_id], back_populates="friendships_as_friend")


class Message(Base):
    __tablename__ = "messages"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    sender_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    attachment_url = Column(String(500), nullable=True)
    attachment_type = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")


class EmailVerification(Base):
    __tablename__ = "email_verifications"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    email = Column(String(255), nullable=False)
    verification_code = Column(String(6), nullable=False)
    verification_type = Column(String(20), default='email_verification')  # email_verification/password_reset
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="email_verifications")


class CookieConsent(Base):
    __tablename__ = "cookie_consents"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    functional_cookies = Column(Boolean, default=True)
    analytics_cookies = Column(Boolean, default=False)
    marketing_cookies = Column(Boolean, default=False)
    consent_given = Column(Boolean, default=False)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="cookie_consents")


class NewsFavorite(Base):
    __tablename__ = "news_favorites"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    news_id = Column(GUID(), ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites")
    news = relationship("News", back_populates="favorites")


class NewsRead(Base):
    __tablename__ = "news_reads"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    news_id = Column(GUID(), ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    read_at = Column(DateTime, default=datetime.utcnow)
    read_duration = Column(Integer, default=0)
    progress = Column(Integer, default=0)  # 0-100

    user = relationship("User", back_populates="news_reads")
    news = relationship("News", back_populates="reads")


class NewsComment(Base):
    __tablename__ = "news_comments"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    news_id = Column(GUID(), ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(GUID(), ForeignKey("news_comments.id", ondelete="CASCADE"), nullable=True)
    content = Column(Text, nullable=False)
    like_count = Column(Integer, default=0)
    reply_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="comments")
    news = relationship("News", back_populates="comments")


class Order(Base):
    __tablename__ = "orders"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    order_no = Column(String(32), unique=True, nullable=False, index=True)
    subject = Column(String(200), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment_method = Column(String(20), nullable=True)  # alipay/wechat
    payment_status = Column(String(20), default='pending')  # pending/paid/refunded/closed
    payment_time = Column(DateTime, nullable=True)
    trade_no = Column(String(64), nullable=True)
    subscription_type = Column(String(20), nullable=True)  # monthly/yearly/permanent
    subscription_months = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="orders")


class UserActivityStat(Base):
    __tablename__ = "user_activity_stats"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    news_read_count = Column(Integer, default=0)
    news_read_time = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="activity_stats")


class DownloadHistory(Base):
    __tablename__ = "download_history"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    news_id = Column(GUID(), ForeignKey("news.id", ondelete="CASCADE"), nullable=False)
    file_type = Column(String(20), nullable=False)  # pdf/doc/video/audio
    file_url = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=True)  # bytes
    created_at = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(50), nullable=False)  # like/comment/favorite/follow/system/order
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    related_type = Column(String(50), nullable=True)  # news/comment/order
    related_id = Column(GUID(), nullable=True)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
