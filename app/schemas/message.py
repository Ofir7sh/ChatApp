from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.message import Message

async def get_messages_for_room(db: AsyncSession, room_id: int):
    result = await db.execute(select(Message).where(Message.chat_room_id == room_id).order_by(Message.timestamp))
    return result.scalars().all()

async def create_message(db: AsyncSession, room_id: int, username: str, content: str):
    message = Message(chat_room_id=room_id, username=username, content=content)
    db.add(message)
    await db.commit()
    await db.refresh(message)
    return message