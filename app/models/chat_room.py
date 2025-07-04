from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)

    messages = relationship("Message", back_populates="chat_room")
