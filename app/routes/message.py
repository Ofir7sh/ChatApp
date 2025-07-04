from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import message as schemas
from app.crud import message as crud
from app.crud import chat_room as chatroom_crud
from app.core.security import get_current_username
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/{room_name}", response_model=schemas.Message)
def send_message(
    room_name: str, msg: schemas.MessageCreate, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    logger.info(f"User '{username}' sending message to room '{room_name}': {msg}")

    room = chatroom_crud.get_chatroom_by_name(db, room_name)
    if not room:
        raise HTTPException(status_code=404, detail="Chat room not found")
    return crud.create_message(db, room_id=room.id, username=username, content=msg.content)



@router.get("/{room_name}", response_model=List[schemas.Message])
def get_messages(room_name: str, db: Session = Depends(get_db)):
    room = chatroom_crud.get_chatroom_by_name(db, room_name)
    if not room:
        raise HTTPException(status_code=404, detail="Chat room not found")
    return crud.get_messages_by_room(db, room.id)
