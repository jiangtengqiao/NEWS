from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.email import EmailCodeRequest, EmailVerifyCodeRequest
from app.services.email_service import EmailService


router = APIRouter(prefix="/api/email", tags=["email"])


@router.post("/send-code")
async def send_code(request: EmailCodeRequest, db: Session = Depends(get_db)):
    code = EmailService.create_verification_code(db, request.email, request.type)
    EmailService.send_verification_email(request.email, code, request.type)
    return {"message": "Verification code sent"}


@router.post("/verify-code")
async def verify_code(request: EmailVerifyCodeRequest, db: Session = Depends(get_db)):
    if not EmailService.verify_code(db, request.email, request.code, request.type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification code"
        )
    return {"message": "Verification successful"}
