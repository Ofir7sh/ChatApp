from pydantic import BaseModel
from datetime import datetime

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    content: str

class Message(MessageBase):
    id: int
    username: str
    timestamp: datetime

    class Config:
        orm_mode = True