import random
import string
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.models.email_verification import EmailVerification
from app.core.config import settings


class EmailService:
    @staticmethod
    def generate_verification_code() -> str:
        return ''.join(random.choices(string.digits, k=6))

    @staticmethod
    def create_verification_code(db: Session, email: str, type: str) -> str:
        code = EmailService.generate_verification_code()
        expires_at = datetime.utcnow() + timedelta(minutes=10)
        db.query(EmailVerification).filter(
            EmailVerification.email == email,
            EmailVerification.type == type
        ).delete()
        verification = EmailVerification(
            email=email,
            code=code,
            type=type,
            expires_at=expires_at
        )
        db.add(verification)
        db.commit()
        return code

    @staticmethod
    def verify_code(db: Session, email: str, code: str, type: str) -> bool:
        verification = db.query(EmailVerification).filter(
            EmailVerification.email == email,
            EmailVerification.code == code,
            EmailVerification.type == type,
            EmailVerification.expires_at > datetime.utcnow()
        ).first()
        if verification:
            db.delete(verification)
            db.commit()
            return True
        return False

    @staticmethod
    def send_verification_email(email: str, code: str, type: str):
        print(f"Sending {type} verification code {code} to {email}")
