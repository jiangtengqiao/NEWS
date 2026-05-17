from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.models.user import User
from app.models.friendship import Friendship
from app.schemas.friendship import FriendshipCreate, FriendshipResponse
from app.services.auth_service import get_current_active_user


router = APIRouter(prefix="/api/friends", tags=["friends"])


@router.get("/", response_model=List[FriendshipResponse])
async def get_friends(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    friendships = db.query(Friendship).filter(
        ((Friendship.user_id == current_user.id) | (Friendship.friend_id == current_user.id)),
        Friendship.status == "accepted"
    ).all()
    return friendships


@router.get("/requests", response_model=List[FriendshipResponse])
async def get_friend_requests(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    requests = db.query(Friendship).filter(
        Friendship.friend_id == current_user.id,
        Friendship.status == "pending"
    ).all()
    return requests


@router.post("/request/{friend_id}", response_model=FriendshipResponse)
async def send_friend_request(
    friend_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if friend_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot send friend request to yourself")
    
    existing = db.query(Friendship).filter(
        ((Friendship.user_id == current_user.id) & (Friendship.friend_id == friend_id)) |
        ((Friendship.user_id == friend_id) & (Friendship.friend_id == current_user.id))
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Friendship already exists")
    
    friendship = Friendship(user_id=current_user.id, friend_id=friend_id, status="pending")
    db.add(friendship)
    db.commit()
    db.refresh(friendship)
    return friendship


@router.put("/request/{request_id}/accept", response_model=FriendshipResponse)
async def accept_friend_request(
    request_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    friendship = db.query(Friendship).filter(
        Friendship.id == request_id,
        Friendship.friend_id == current_user.id,
        Friendship.status == "pending"
    ).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="Friend request not found")
    
    friendship.status = "accepted"
    db.commit()
    db.refresh(friendship)
    return friendship


@router.put("/request/{request_id}/reject")
async def reject_friend_request(
    request_id: UUID,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    friendship = db.query(Friendship).filter(
        Friendship.id == request_id,
        Friendship.friend_id == current_user.id,
        Friendship.status == "pending"
    ).first()
    if not friendship:
        raise HTTPException(status_code=404, detail="Friend request not found")
    
    friendship.status = "rejected"
    db.commit()
    return {"message": "Friend request rejected"}
