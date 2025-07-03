from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserLogin, Token
from app.crud.user import get_user, create_user, authenticate_user
from app.database import get_db
from app.core.security import create_access_token

router = APIRouter()

@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = get_user(db, user_login.username)
    if not user:
        raise HTTPException(status_code=400, detail="User not found. Please register.")
    authenticated_user = authenticate_user(db, user_login.username, user_login.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Incorrect password.")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register", response_model=Token)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    user = get_user(db, user_create.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered.")
    new_user = create_user(db, user_create.username, user_create.password)
    token = create_access_token({"sub": new_user.username})
    return {"access_token": token, "token_type": "bearer"}
