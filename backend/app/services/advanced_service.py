from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime, date

from app.models.advanced import Notification, UserSetting, UserActivityStat
from app.schemas.advanced import (
    NotificationCreate, NotificationUpdate, UserSettingUpdate
)


class NotificationService:
    @staticmethod
    def get_notifications(db: Session, user_id: UUID, skip: int = 0, limit: int = 20) -> List[Notification]:
        return db.query(Notification).filter(
            Notification.user_id == user_id
        ).order_by(Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_unread_count(db: Session, user_id: UUID) -> int:
        return db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read.is_(False)
        ).count()
    
    @staticmethod
    def create_notification(db: Session, notification: NotificationCreate) -> Notification:
        db_notification = Notification(**notification.model_dump())
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        return db_notification
    
    @staticmethod
    def mark_read(db: Session, notification_id: UUID, user_id: UUID) -> Optional[Notification]:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        if notification:
            notification.is_read = True
            db.commit()
            db.refresh(notification)
        return notification
    
    @staticmethod
    def mark_all_read(db: Session, user_id: UUID) -> int:
        updated = db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read.is_(False)
        ).update({"is_read": True})
        db.commit()
        return updated
    
    @staticmethod
    def delete_notification(db: Session, notification_id: UUID, user_id: UUID) -> bool:
        notification = db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        if notification:
            db.delete(notification)
            db.commit()
            return True
        return False


class UserSettingService:
    @staticmethod
    def get_settings(db: Session, user_id: UUID) -> UserSetting:
        settings = db.query(UserSetting).filter(UserSetting.user_id == user_id).first()
        if not settings:
            settings = UserSetting(user_id=user_id)
            db.add(settings)
            db.commit()
            db.refresh(settings)
        return settings
    
    @staticmethod
    def update_settings(db: Session, user_id: UUID, update: UserSettingUpdate) -> UserSetting:
        settings = UserSettingService.get_settings(db, user_id)
        update_data = update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(settings, field, value)
        db.commit()
        db.refresh(settings)
        return settings


class StatsService:
    @staticmethod
    def get_user_stats(db: Session, user_id: UUID, days: int = 30) -> List[UserActivityStat]:
        return db.query(UserActivityStat).filter(
            UserActivityStat.user_id == user_id,
            UserActivityStat.date >= date.today().replace(day=1)
        ).order_by(UserActivityStat.date.desc()).limit(days).all()
    
    @staticmethod
    def record_activity(db: Session, user_id: UUID, activity_type: str):
        today = date.today()
        stat = db.query(UserActivityStat).filter(
            UserActivityStat.user_id == user_id,
            UserActivityStat.date == today
        ).first()
        
        if not stat:
            stat = UserActivityStat(user_id=user_id, date=today)
            db.add(stat)
        
        if activity_type == "news_read":
            stat.news_read_count += 1
        elif activity_type == "comment":
            stat.comment_count += 1
        elif activity_type == "like":
            stat.like_count += 1
        elif activity_type == "friend_request":
            stat.friend_request_count += 1
        elif activity_type == "message":
            stat.message_count += 1
        
        db.commit()
        db.refresh(stat)
        return stat
    
    @staticmethod
    def get_reading_stats(db: Session, user_id: UUID) -> dict:
        reads = db.query(UserActivityStat).filter(UserActivityStat.user_id == user_id).all()
        total_read = sum(r.news_read_count for r in reads)
        return {"total_read": total_read}
