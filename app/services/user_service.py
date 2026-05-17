import random
import string
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, UploadFile
from uuid import UUID

from app.models.user import User
from app.models.user_extended import UserCode
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


class UserService:
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            password_hash=hashed_password,
            nickname=user.nickname or user.email.split("@")[0]
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: UUID, user_update: UserUpdate) -> Optional[User]:
        db_user = UserService.get_user_by_id(db, user_id)
        if not db_user:
            return None
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_or_create_user_code(db: Session, user_id: UUID) -> UserCode:
        user_code = db.query(UserCode).filter(UserCode.user_id == user_id).first()
        if user_code:
            return user_code
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        while db.query(UserCode).filter(UserCode.code == code).first():
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        user_code = UserCode(user_id=user_id, code=code)
        db.add(user_code)
        db.commit()
        db.refresh(user_code)
        return user_code

    @staticmethod
    def get_user_by_code(db: Session, code: str) -> Optional[User]:
        user_code = db.query(UserCode).filter(UserCode.code == code).first()
        if not user_code:
            return None
        return user_code.user

    @staticmethod
    def upload_avatar(db: Session, user_id: UUID, file: UploadFile) -> str:
        return "https://via.placeholder.com/150"
