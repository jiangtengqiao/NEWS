from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserCodeResponse
from app.services.auth_service import get_current_active_user
from app.services.user_service import UserService


router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: UUID, db: Session = Depends(get_db)):
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/me", response_model=UserResponse)
async def update_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    updated_user = UserService.update_user(db, current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.post("/me/avatar")
async def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    avatar_url = UserService.upload_avatar(db, current_user.id, file)
    return {"avatar_url": avatar_url}


@router.get("/me/code", response_model=UserCodeResponse)
async def get_my_code(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user_code = UserService.get_or_create_user_code(db, current_user.id)
    return user_code


@router.get("/code/{code}", response_model=UserResponse)
async def get_user_by_code(code: str, db: Session = Depends(get_db)):
    user = UserService.get_user_by_code(db, code)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
