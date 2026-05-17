from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    EMAIL_BACKEND: str = "resend"
    RESEND_API_KEY: Optional[str] = None
    EMAIL_FROM: str = "noreply@example.com"
    EMAIL_FROM_NAME: str = "Customize-News"
    
    OSS_ACCESS_KEY_ID: Optional[str] = None
    OSS_ACCESS_KEY_SECRET: Optional[str] = None
    OSS_BUCKET_NAME: Optional[str] = None
    OSS_ENDPOINT: str = "oss-cn-guilin.aliyuncs.com"
    OSS_REGION: str = "cn-guilin"

    class Config:
        env_file = ".env"


settings = Settings()
