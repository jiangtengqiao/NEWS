from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services.auth_service import get_current_user
from app.models.user import User
from app.models.user_extended import Friendship, Message, UserCode
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/friends", tags=["好友"])


@router.get("")
def get_friends(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    friendships = db.query(Friendship).filter(
        (Friendship.user_id == current_user.id) | (Friendship.friend_id == current_user.id),
        Friendship.status == 'accepted'
    ).all()
    
    friends = []
    for f in friendships:
        friend = f.friend if f.user_id == current_user.id else f.user
        friends.append({
            "id": str(friend.id),
            "nickname": friend.nickname or friend.email.split('@')[0],
            "avatar_url": friend.avatar_url,
            "friendship_id": str(f.id),
            "created_at": f.created_at.isoformat()
        })
    
    return {"friends": friends}


@router.get("/requests")
def get_friend_requests(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    requests = db.query(Friendship).filter(
        Friendship.friend_id == current_user.id,
        Friendship.status == 'pending'
    ).all()
    
    return {
        "requests": [
            {
                "id": str(r.id),
                "user_id": str(r.user_id),
                "nickname": r.user.nickname or r.user.email.split('@')[0],
                "avatar_url": r.user.avatar_url,
                "created_at": r.created_at.isoformat()
            }
            for r in requests
        ]
    }


@router.post("/request/{user_id}")
def send_friend_request(
    user_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if user_id == str(current_user.id):
        raise HTTPException(status_code=400, detail="不能添加自己为好友")
    
    target_user = db.query(User).filter_by(id=uuid.UUID(user_id)).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    existing = db.query(Friendship).filter(
        ((Friendship.user_id == current_user.id) & (Friendship.friend_id == uuid.UUID(user_id))) |
        ((Friendship.user_id == uuid.UUID(user_id)) & (Friendship.friend_id == current_user.id))
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="好友关系已存在")
    
    friendship = Friendship(
        user_id=current_user.id,
        friend_id=uuid.UUID(user_id),
        status='pending'
    )
    db.add(friendship)
    db.commit()
    
    return {"message": "好友请求已发送"}


@router.post("/request/{request_id}/accept")
def accept_friend_request(
    request_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    friendship = db.query(Friendship).filter(
        Friendship.id == uuid.UUID(request_id),
        Friendship.friend_id == current_user.id,
        Friendship.status == 'pending'
    ).first()
    
    if not friendship:
        raise HTTPException(status_code=404, detail="请求不存在")
    
    friendship.status = 'accepted'
    db.commit()
    
    return {"message": "已接受好友请求"}


@router.post("/request/{request_id}/reject")
def reject_friend_request(
    request_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    friendship = db.query(Friendship).filter(
        Friendship.id == uuid.UUID(request_id),
        Friendship.friend_id == current_user.id,
        Friendship.status == 'pending'
    ).first()
    
    if not friendship:
        raise HTTPException(status_code=404, detail="请求不存在")
    
    friendship.status = 'rejected'
    db.commit()
    
    return {"message": "已拒绝好友请求"}


@router.delete("/{friend_id}")
def delete_friend(
    friend_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    friendship = db.query(Friendship).filter(
        ((Friendship.user_id == current_user.id) & (Friendship.friend_id == uuid.UUID(friend_id))) |
        ((Friendship.user_id == uuid.UUID(friend_id)) & (Friendship.friend_id == current_user.id)),
        Friendship.status == 'accepted'
    ).first()
    
    if not friendship:
        raise HTTPException(status_code=404, detail="好友关系不存在")
    
    db.delete(friendship)
    db.commit()
    
    return {"message": "已删除好友"}


# 私信相关路由
msg_router = APIRouter(prefix="/api/messages", tags=["私信"])


@msg_router.get("")
def get_messages(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    messages = db.query(Message).filter(
        (Message.sender_id == current_user.id) | (Message.receiver_id == current_user.id)
    ).order_by(Message.created_at.desc()).offset(skip).limit(limit).all()
    
    return {
        "messages": [
            {
                "id": str(m.id),
                "sender_id": str(m.sender_id),
                "receiver_id": str(m.receiver_id),
                "content": m.content,
                "is_read": m.is_read,
                "created_at": m.created_at.isoformat()
            }
            for m in messages
        ]
    }


@msg_router.get("/{user_id}")
def get_conversation(
    user_id: str,
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    messages = db.query(Message).filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == uuid.UUID(user_id))) |
        ((Message.sender_id == uuid.UUID(user_id)) & (Message.receiver_id == current_user.id))
    ).order_by(Message.created_at.asc()).offset(skip).limit(limit).all()
    
    # 标记为已读
    unread = db.query(Message).filter(
        Message.sender_id == uuid.UUID(user_id),
        Message.receiver_id == current_user.id,
        Message.is_read == False
    ).all()
    
    for m in unread:
        m.is_read = True
        m.read_at = datetime.utcnow()
    
    db.commit()
    
    return {
        "messages": [
            {
                "id": str(m.id),
                "sender_id": str(m.sender_id),
                "receiver_id": str(m.receiver_id),
                "content": m.content,
                "is_read": m.is_read,
                "created_at": m.created_at.isoformat()
            }
            for m in messages
        ]
    }


@msg_router.post("")
def send_message(
    receiver_id: str,
    content: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if receiver_id == str(current_user.id):
        raise HTTPException(status_code=400, detail="不能给自己发消息")
    
    receiver = db.query(User).filter_by(id=uuid.UUID(receiver_id)).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    message = Message(
        sender_id=current_user.id,
        receiver_id=uuid.UUID(receiver_id),
        content=content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return {
        "message": {
            "id": str(message.id),
            "sender_id": str(message.sender_id),
            "receiver_id": str(message.receiver_id),
            "content": message.content,
            "is_read": message.is_read,
            "created_at": message.created_at.isoformat()
        }
    }


@msg_router.put("/{message_id}/read")
def mark_as_read(
    message_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    message = db.query(Message).filter(
        Message.id == uuid.UUID(message_id),
        Message.receiver_id == current_user.id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")
    
    message.is_read = True
    message.read_at = datetime.utcnow()
    db.commit()
    
    return {"message": "已标记为已读"}
