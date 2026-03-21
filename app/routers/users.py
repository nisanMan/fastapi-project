#app\routers\users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..auth.hashing import hash_password, verify_password
from ..auth.jwt_handler import create_token

from ..logger import log 


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        log(db, "WARNING", f"Registration attempt with existing email: {user.email}", path="/users/register")  # LOG
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = models.User(
        email=user.email,
        password=hash_password(user.password),
        phone=user.phone #Alembic 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    log(db, "INFO", f"New user registered: {user.email}", user_id=new_user.id, path="/users/register")  #LOG
    return {"message": "User created"}

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user:
        log(db, "WARNING", f"Login attempt for non-existent email: {user.email}", path="/users/login")  #LOG
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.password, db_user.password):
        log(db, "WARNING", f"Failed login attempt for: {user.email}", user_id=db_user.id, path="/users/login")  #LOG
        raise HTTPException(status_code=401, detail="Wrong password")
    
    token = create_token({"user_id": db_user.id})

    log(db, "INFO", f"User logged in: {user.email}", user_id=db_user.id, path="/users/login")  #LOG
    return {"access_token": token, "token_type": "bearer"}