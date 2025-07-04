from fastapi import FastAPI
from app.database import engine
from app.database import Base
from app.routes import user, chat_room, message
import logging
from app.routes import message_ws

# Define logger
logging.basicConfig(
    filename='server.log',          
    level=logging.DEBUG,        
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)

# Validate tables
Base.metadata.create_all(bind=engine)

# Build app
app = FastAPI()

# Connect routes
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(chat_room.router, prefix="/chatrooms", tags=["chatrooms"])
app.include_router(message.router, prefix="/messages", tags=["messages"])
app.include_router(message_ws.router)  # ללא פריפיקס, כדי שהנתיב יהיה /ws/{room_name}
