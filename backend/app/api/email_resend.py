from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.models.user import User
from app.models.user_extended import EmailVerification
from app.services.email_service import EmailService
from datetime import datetime, timedelta
import uuid

router = APIRouter(prefix="/api/email", tags=["邮箱"])


class SendVerificationRequest(BaseModel):
    email: str
    type: str = "email_verification"  # email_verification/password_reset


class VerifyCodeRequest(BaseModel):
    email: str
    code: str
    type: str = "email_verification"


@router.post("/send-verification")
def send_verification_email(
    request: SendVerificationRequest,
    db: Session = Depends(get_db)
):
    # 检查邮箱是否已注册（对于注册验证）
    if request.type == "email_verification":
        existing = db.query(User).filter_by(email=request.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="该邮箱已被注册")
    
    # 生成6位验证码
    code = EmailService.generate_verification_code()
    
    # 删除旧的验证码
    db.query(EmailVerification).filter_by(email=request.email, is_used=False).delete()
    
    # 创建新的验证码记录
    verification = EmailVerification(
        user_id=uuid.uuid4(),  # 临时用户ID
        email=request.email,
        verification_code=code,
        verification_type=request.type,
        is_used=False,
        expires_at=datetime.utcnow() + timedelta(minutes=10)
    )
    db.add(verification)
    db.commit()
    
    # 发送邮件
    if request.type == "email_verification":
        success = EmailService.send_verification_email(request.email, code)
    else:
        success = EmailService.send_password_reset_email(request.email, code)
    
    if success:
        return {
            "message": "验证码已发送到邮箱",
            "email": request.email,
            "expires_in": 600  # 10分钟
        }
    else:
        raise HTTPException(status_code=500, detail="邮件发送失败")


@router.post("/verify")
def verify_code(
    request: VerifyCodeRequest,
    db: Session = Depends(get_db)
):
    verification = db.query(EmailVerification).filter_by(
        email=request.email,
        verification_code=request.code,
        verification_type=request.type,
        is_used=False
    ).first()
    
    if not verification:
        raise HTTPException(status_code=400, detail="验证码无效")
    
    if verification.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="验证码已过期")
    
    # 标记为已使用
    verification.is_used = True
    db.commit()
    
    return {
        "message": "验证成功",
        "verified": True
    }


@router.post("/resend")
def resend_verification(
    request: SendVerificationRequest,
    db: Session = Depends(get_db)
):
    # 删除旧的验证码
    db.query(EmailVerification).filter_by(email=request.email, is_used=False).delete()
    db.commit()
    
    # 重新发送
    return send_verification_email(request, db)
