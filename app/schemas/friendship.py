from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class FriendshipBase(BaseModel):
    pass


class FriendshipCreate(BaseModel):
    friend_id: UUID


class FriendshipResponse(BaseModel):
    id: UUID
    user_id: UUID
    friend_id: UUID
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
