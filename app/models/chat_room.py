from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

from app.database import Base

class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    # Write why is it String(50)
    name = Column(String(50), unique=True)

    messages = relationship("Message", back_populates="room")
