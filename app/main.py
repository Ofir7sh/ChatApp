from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routes import user

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, Chat API!"}

app.include_router(user.router)
