from fastapi import WebSocket, WebSocketDisconnect, Query, status, APIRouter
from app.websocket.manager import ConnectionManager
import logging
from app.core.security import get_current_username
from app.database import get_db
from app.crud.message import create_message
from app.crud.chat_room import get_chatroom_by_name
from sqlalchemy.orm import Session

router = APIRouter()
manager = ConnectionManager()
logger = logging.getLogger(__name__)

@router.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str, token: str = Query(...)):
    try:
        username = get_current_username(token)
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(room_name, websocket)
    logger.info(f"WebSocket connected to room {room_name}")

    db: Session = next(get_db())

    room = get_chatroom_by_name(db, room_name)
    if not room:
        logger.warning(f"Room '{room_name}' not found")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Message received in {room_name}: {data}")

            await manager.broadcast(room_name, data)

            try:
                create_message(
                    db=db,
                    room_id=room.id,
                    username=data["username"],
                    content=data["content"]
                )
            except Exception as e:
                logger.error(f"Failed to save message to DB: {e}")

    except WebSocketDisconnect:
        manager.disconnect(room_name, websocket)
        logger.info(f"WebSocket disconnected from room {room_name}")
