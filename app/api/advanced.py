from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.user import User
from app.schemas.advanced import (
    NotificationResponse, NotificationUpdate,
    UserSettingResponse, UserSettingUpdate,
    UserActivityStatResponse
)
from app.services.auth_service import get_current_active_user
from app.services.advanced_service import NotificationService, UserSettingService, StatsService


router = APIRouter(tags=["advanced"])


@router.get("/api/notifications", response_model=List[NotificationResponse])
def get_notifications(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return NotificationService.get_notifications(db, current_user.id, skip=skip, limit=limit)


@router.get("/api/notifications/unread")
def get_unread_count(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return {"count": NotificationService.get_unread_count(db, current_user.id)}


@router.put("/api/notifications/{notification_id}/read", response_model=NotificationResponse)
def mark_read(
    notification_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    notification = NotificationService.mark_read(db, notification_id, current_user.id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.put("/api/notifications/read-all")
def mark_all_read(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    count = NotificationService.mark_all_read(db, current_user.id)
    return {"marked": count}


@router.delete("/api/notifications/{notification_id}")
def delete_notification(
    notification_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    success = NotificationService.delete_notification(db, notification_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification deleted"}


@router.get("/api/settings", response_model=UserSettingResponse)
def get_settings(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return UserSettingService.get_settings(db, current_user.id)


@router.put("/api/settings", response_model=UserSettingResponse)
def update_settings(
    update: UserSettingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return UserSettingService.update_settings(db, current_user.id, update)


@router.get("/api/stats/user", response_model=List[UserActivityStatResponse])
def get_user_stats(
    days: int = 30,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return StatsService.get_user_stats(db, current_user.id, days)


@router.get("/api/stats/reading")
def get_reading_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return StatsService.get_reading_stats(db, current_user.id)
