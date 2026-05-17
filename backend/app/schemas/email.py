from pydantic import BaseModel, EmailStr


class EmailCodeRequest(BaseModel):
    email: EmailStr
    type: str


class EmailVerifyCodeRequest(BaseModel):
    email: EmailStr
    code: str
    type: str


class CookieConsentCreate(BaseModel):
    necessary: bool = True
    analytics: bool = False
    marketing: bool = False
