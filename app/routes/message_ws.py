from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import ConnectionManager
import logging

router = APIRouter()
manager = ConnectionManager()
logger = logging.getLogger(__name__)

@router.websocket("/ws/{room_name}")
async def websocket_chat(websocket: WebSocket, room_name: str):
    await manager.connect(room_name, websocket)
    logger.info(f"WebSocket connected to room {room_name}")
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"Received message in {room_name}: {data}")
            await manager.broadcast(room_name, data)
    except WebSocketDisconnect:
        manager.disconnect(room_name, websocket)
        logger.info(f"WebSocket disconnected from room {room_name}")
