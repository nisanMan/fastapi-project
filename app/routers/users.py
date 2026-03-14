#app\routers\users.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import models, schemas, auth
from app.database import get_db

# users register
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = auth.hash_password(user.password)

    new_user = models.User(
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created"}

#  users login
@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if not db_user:
        return {"error": "user not found"}

    if not auth.verify_password(user.password, db_user.password):
        return {"error": "wrong password"}

    token = auth.create_token({"user_id": db_user.id})

    return {"access_token": token}   

# chak users
@router.get("/")
def get_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users