from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.chat_room import ChatRoom

async def get_all_chat_rooms(db: AsyncSession):
    result = await db.execute(select(ChatRoom))
    return result.scalars().all()

async def get_chatroom_by_name(db: AsyncSession, name: str):
    result = await db.execute(select(ChatRoom).where(ChatRoom.name == name))
    return result.scalar_one_or_none()

async def create_chatroom(db: AsyncSession, name: str):
    db_room = ChatRoom(name=name)
    db.add(db_room)
    await db.commit()
    await db.refresh(db_room)
    return db_room

