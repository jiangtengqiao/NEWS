from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    receiver_id: UUID


class MessageResponse(MessageBase):
    id: UUID
    sender_id: UUID
    receiver_id: UUID
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
