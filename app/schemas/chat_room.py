from pydantic import BaseModel
from typing import List, Optional
from app.schemas.message import Message 

class ChatRoomBase(BaseModel):
    name: str

class ChatRoomCreate(ChatRoomBase):
    pass

class ChatRoom(ChatRoomBase):
    id: int
    messages: Optional[List[Message]] = []

    class Config:
        from_attributes = True


class ChatRoomResponse(ChatRoom):
    messages: Optional[List[Message]] = []