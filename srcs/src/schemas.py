# src/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FriendBase(BaseModel):
    user_id: int
    friend_id: int

class FriendCreate(FriendBase):
    pass

class Friend(FriendBase):
    id: int
    friend_since: datetime

    class Config:
        orm_mode = True

class FriendRequestBase(BaseModel):
    sender_id: int
    receiver_id: int

class FriendRequestCreate(FriendRequestBase):
    pass

class FriendRequest(FriendRequestBase):
    id: int
    status: str
    sent_at: datetime
    responded_at: Optional[datetime] = None

    class Config:
        orm_mode = True
