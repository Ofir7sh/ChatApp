from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.models.chat_room import ChatRoom

def get_all_chat_rooms(db: Session):
    result = db.execute(select(ChatRoom))
    return result.scalars().all()  

def get_chatroom_by_name(db: Session, name: str):
    result = db.execute(select(ChatRoom).where(ChatRoom.name == name))
    return result.scalar_one_or_none()  

def create_chatroom(db: Session, name: str):
    db_room = ChatRoom(name=name)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room
