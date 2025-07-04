from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.chat_room import ChatRoomCreate, ChatRoomResponse
from app.database import get_db
from app import crud

router = APIRouter()

@router.post("/", response_model=ChatRoomResponse)
def create_chatroom(chatroom: ChatRoomCreate, db: AsyncSession = Depends(get_db)):
    existing = crud.chat_room.get_chatroom_by_name(db, chatroom.name)
    if existing:
        raise HTTPException(status_code=400, detail="Chat room already exists")

    new_room = crud.chat_room.create_chatroom(db, chatroom.name)
    return new_room


@router.get("/", response_model=list[ChatRoomResponse])
def list_chatrooms(db: AsyncSession = Depends(get_db)):
    return crud.chat_room.get_all_chat_rooms(db)


@router.get("/{room_name}", response_model=ChatRoomResponse)
def get_chatroom_by_name(room_name: str, db: AsyncSession = Depends(get_db)):
    room = crud.chat_room.get_chatroom_by_name(db, room_name)
    if not room:
        raise HTTPException(status_code=404, detail="Chat room not found")
    return room
