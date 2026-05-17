from app.schemas.user import (
    UserBase,
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    Token,
    TokenData,
    UserCodeResponse
)
from app.schemas.friendship import FriendshipBase, FriendshipCreate, FriendshipResponse
from app.schemas.message import MessageBase, MessageCreate, MessageResponse
from app.schemas.email import EmailCodeRequest, EmailVerifyCodeRequest, CookieConsentCreate
from app.schemas.news import (
    CategoryBase, CategoryCreate, CategoryResponse,
    NewsBase, NewsCreate, NewsUpdate, NewsResponse,
    NewsFavoriteBase, NewsFavoriteCreate, NewsFavoriteResponse,
    NewsReadBase, NewsReadCreate, NewsReadResponse,
    NewsCommentBase, NewsCommentCreate, NewsCommentResponse,
    UserPreferenceBase, UserPreferenceCreate, UserPreferenceResponse
)
from app.schemas.advanced import (
    NotificationBase, NotificationCreate, NotificationUpdate, NotificationResponse,
    UserSettingBase, UserSettingUpdate, UserSettingResponse,
    UserActivityStatBase, UserActivityStatCreate, UserActivityStatResponse
)

__all__ = [
    "UserBase",
    "UserCreate",
    "UserLogin",
    "UserUpdate",
    "UserResponse",
    "Token",
    "TokenData",
    "UserCodeResponse",
    "FriendshipBase",
    "FriendshipCreate",
    "FriendshipResponse",
    "MessageBase",
    "MessageCreate",
    "MessageResponse",
    "EmailCodeRequest",
    "EmailVerifyCodeRequest",
    "CookieConsentCreate",
    # News schemas
    "CategoryBase", "CategoryCreate", "CategoryResponse",
    "NewsBase", "NewsCreate", "NewsUpdate", "NewsResponse",
    "NewsFavoriteBase", "NewsFavoriteCreate", "NewsFavoriteResponse",
    "NewsReadBase", "NewsReadCreate", "NewsReadResponse",
    "NewsCommentBase", "NewsCommentCreate", "NewsCommentResponse",
    "UserPreferenceBase", "UserPreferenceCreate", "UserPreferenceResponse",
    # Advanced schemas
    "NotificationBase", "NotificationCreate", "NotificationUpdate", "NotificationResponse",
    "UserSettingBase", "UserSettingUpdate", "UserSettingResponse",
    "UserActivityStatBase", "UserActivityStatCreate", "UserActivityStatResponse"
]
