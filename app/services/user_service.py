# app/services/user_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import schemas
from ..repositories.user_repository import UserRepository
from ..auth.hashing import verify_password
from ..auth.jwt_handler import create_token
from ..logger import log


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        self.db = db

    def register(self, user: schemas.UserCreate):
        existing = self.repo.get_by_email(user.email)
        if existing:
            log(self.db, "WARNING", f"Registration attempt with existing email: {user.email}", path="/users/register")
            raise HTTPException(status_code=400, detail="User already exists")

        new_user = self.repo.create(user)
        log(self.db, "INFO", f"New user registered: {user.email}", user_id=new_user.id, path="/users/register")
        return {"message": "User created"}

    def login(self, user: schemas.UserLogin):
        db_user = self.repo.get_by_email(user.email)
        if not db_user:
            log(self.db, "WARNING", f"Login attempt for non-existent email: {user.email}", path="/users/login")
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(user.password, db_user.password):
            log(self.db, "WARNING", f"Failed login attempt for: {user.email}", user_id=db_user.id, path="/users/login")
            raise HTTPException(status_code=401, detail="Wrong password")

        token = create_token({"user_id": db_user.id})
        log(self.db, "INFO", f"User logged in: {user.email}", user_id=db_user.id, path="/users/login")
        return {"access_token": token, "token_type": "bearer"}