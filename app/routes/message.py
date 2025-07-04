from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import message as schemas
from app.crud import message as crud
from app.crud import chat_room as chatroom_crud

router = APIRouter()

@router.post("/{room_name}", response_model=schemas.Message)
def send_message(room_name: str, msg: schemas.MessageCreate, db: Session = Depends(get_db)):
    room = chatroom_crud.get_chatroom_by_name(db, room_name)
    if not room:
        raise HTTPException(status_code=404, detail="Chat room not found")
    # הנחה שה־MessageCreate כולל username ו-content
    return crud.create_message(db, room_id=room.id, username=msg.username, content=msg.content)


@router.get("/{room_name}", response_model=List[schemas.Message])
def get_messages(room_name: str, db: Session = Depends(get_db)):
    room = chatroom_crud.get_chatroom_by_name(db, room_name)
    if not room:
        raise HTTPException(status_code=404, detail="Chat room not found")
    return crud.get_messages_by_room(db, room.id)
