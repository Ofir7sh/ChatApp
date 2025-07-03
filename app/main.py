from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routes import user
from app.routes import user, chatroom, message


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(chatroom.router, prefix="/chatrooms", tags=["chatrooms"])
app.include_router(message.router, prefix="/messages", tags=["messages"])

@app.get("/")
async def root():
    return {"message": "Hello, Chat API!"}

app.include_router(user.router)
