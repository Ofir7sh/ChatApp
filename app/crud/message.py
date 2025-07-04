from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.message import Message

# Works!
def get_messages_by_room(db: Session, room_id: int):
    result = db.execute(select(Message).where(Message.chat_room_id == room_id).order_by(Message.timestamp))
    return result.scalars().all()

# Works!
def create_message(db: Session, room_id: int, username: str, content: str):
    message = Message(chat_room_id=room_id, username=username, content=content)  
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
