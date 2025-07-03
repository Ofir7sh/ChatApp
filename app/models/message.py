from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    chat_room_id = Column(Integer, ForeignKey("chat_rooms.id"))
    username = Column(String)  

    chat_room = relationship("ChatRoom", back_populates="messages")