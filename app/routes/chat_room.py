from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.chat_room import ChatRoomCreate, ChatRoomResponse
from app.database import get_db
from app import crud

router = APIRouter(
    prefix="/chatrooms",
    tags=["Chat Rooms"]
)

@router.post("/", response_model=ChatRoomResponse)
async def create_chatroom(chatroom: ChatRoomCreate, db: AsyncSession = Depends(get_db)):
    existing = await crud.chatroom.get_chatroom_by_name(db, chatroom.name)
    if existing:
        raise HTTPException(status_code=400, detail="Chat room already exists")

    new_room = await crud.chatroom.create_chatroom(db, chatroom)
    return new_room


@router.get("/", response_model=list[ChatRoomResponse])
async def list_chatrooms(db: AsyncSession = Depends(get_db)):
    return await crud.chatroom.get_chatrooms(db)


@router.get("/{room_name}", response_model=ChatRoomResponse)
async def get_chatroom_by_name(room_name: str, db: AsyncSession = Depends(get_db)):
    room = await crud.chatroom.get_chatroom_by_name(db, room_name)
    if not room:
        raise HTTPException(status_code=404, detail="Chat room not found")
    return room
