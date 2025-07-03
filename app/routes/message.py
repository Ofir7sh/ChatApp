from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_async_db
from app.schemas import message as schemas
from app.crud import message as crud
from app.crud import chatroom as chatroom_crud

router = APIRouter()

@router.post("/{room_id}", response_model=schemas.Message)
async def send_message(room_id: int, msg: schemas.MessageCreate, db: AsyncSession = Depends(get_async_db)):
    room = await chatroom_crud.get_chatroom_by_id(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Chat room not found")
    return await crud.create_message(db, room_id=room_id, msg=msg)

@router.get("/{room_id}", response_model=List[schemas.Message])
async def get_messages(room_id: int, db: AsyncSession = Depends(get_async_db)):
    return await crud.get_messages_for_room(db, room_id)
