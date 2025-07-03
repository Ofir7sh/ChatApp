from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, security
from app.schemas import UserLogin, UserRegister
from app.database import get_async_db

router = APIRouter()

# Check if the username exist
@router.post("/users/check")
async def check_user(user: UserLogin, db: AsyncSession = Depends(get_async_db)):
    db_user = await crud.get_user_by_username(db, user.username)
    return {"user_exists": bool(db_user)}

# Register new user
@router.post("/users/register")
async def register(user: UserRegister, db: AsyncSession = Depends(get_async_db)):
    db_user = await crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    created_user = await crud.create_user(db, user.username, user.password)
    token = security.create_access_token({"sub": created_user.username})
    return {"msg": "User created", "access_token": token}

# Login user
@router.post("/users/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_async_db)):
    db_user = await crud.get_user_by_username(db, user.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")
    token = security.create_access_token({"sub": db_user.username})
    return {"msg": "Login successful", "access_token": token}
