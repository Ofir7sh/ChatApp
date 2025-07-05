import logging
import sys
from fastapi import FastAPI
from app.database import engine, Base
from app.routes import user, chat_room, message, message_ws

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('server.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Validate tables
Base.metadata.create_all(bind=engine)

# Build app
app = FastAPI()

# Connect routes
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(chat_room.router, prefix="/chatrooms", tags=["chatrooms"])
app.include_router(message.router, prefix="/messages", tags=["messages"])
app.include_router(message_ws.router)
