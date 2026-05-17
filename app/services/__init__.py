from app.services.cache_service import cache_service, CacheService
from app.services.auth_service import (
    get_current_user,
    get_current_active_user,
    AuthService
)
from app.services.user_service import UserService
from app.services.email_service import EmailService
from app.services.news_service import NewsService
from app.services.advanced_service import NotificationService, UserSettingService, StatsService

__all__ = [
    "cache_service",
    "CacheService",
    "get_current_user",
    "get_current_active_user",
    "AuthService",
    "UserService",
    "EmailService",
    "NewsService",
    "NotificationService",
    "UserSettingService",
    "StatsService"
]
