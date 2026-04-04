# app/routers/users.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return UserService(db).register(user)

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return UserService(db).login(user)