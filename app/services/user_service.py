# app/services/user_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, Response
from .. import schemas
from ..repositories.user_repository import UserRepository
from ..repositories.token_repository import (
    save_refresh_token,
    get_token_by_hash,
    revoke_token,
    revoke_all_user_tokens,
    delete_expired_tokens
)
from ..auth.hashing import verify_password
from ..auth.jwt_handler import create_token, create_refresh_token, hash_token
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

    def login(self, user: schemas.UserLogin, response: Response):
        db_user = self.repo.get_by_email(user.email)
        if not db_user:
            log(self.db, "WARNING", f"Login attempt for non-existent email: {user.email}", path="/users/login")
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(user.password, db_user.password):
            log(self.db, "WARNING", f"Failed login attempt for: {user.email}", user_id=db_user.id, path="/users/login")
            raise HTTPException(status_code=401, detail="Wrong password")

        # Access Token
        access_token = create_token({"user_id": db_user.id})

        # Refresh Token
        token, token_hash, expires_at = create_refresh_token()
        save_refresh_token(self.db, db_user.id, token_hash, expires_at)

        # שליחה בHttpOnly Cookie
        response.set_cookie(
            key="refresh_token",
            value=token,
            httponly=True,    # לא נגיש ל-JS
            secure=True,      # רק HTTPS
            samesite="lax",
            max_age=7 * 24 * 60 * 60  # 7 ימים בשניות
        )

        log(self.db, "INFO", f"User logged in: {user.email}", user_id=db_user.id, path="/users/login")
        return schemas.TokenResponse(access_token=access_token)

    def refresh(self, token: str, response: Response):
        """מנפיק Access Token חדש + מבצע Rotation על ה-Refresh Token"""
        token_hash = hash_token(token)
        db_token = get_token_by_hash(self.db, token_hash)

        if not db_token:
            log(self.db, "WARNING", "Invalid or expired refresh token used", path="/users/refresh")
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        # Revoke הישן
        revoke_token(self.db, token_hash)

        # Cleanup ברקע — מוחק פגי תוקף
        delete_expired_tokens(self.db)

        # צור חדשים
        access_token = create_token({"user_id": db_token.user_id})
        new_token, new_hash, expires_at = create_refresh_token()
        save_refresh_token(self.db, db_token.user_id, new_hash, expires_at)

        response.set_cookie(
            key="refresh_token",
            value=new_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60
        )

        log(self.db, "INFO", f"Token refreshed for user_id: {db_token.user_id}", user_id=db_token.user_id, path="/users/refresh")
        return {"access_token": access_token, "token_type": "bearer"}

    def logout(self, token: str, response: Response):
        """מבטל את הסשן הנוכחי בלבד"""
        token_hash = hash_token(token)
        revoke_token(self.db, token_hash)
        response.delete_cookie("refresh_token")

        log(self.db, "INFO", "User logged out", path="/users/logout")
        return {"message": "Logged out"}

    def logout_all(self, user_id: int, response: Response):
        """מבטל את כל הסשנים — כל המכשירים"""
        revoke_all_user_tokens(self.db, user_id)
        response.delete_cookie("refresh_token")

        log(self.db, "INFO", f"All sessions revoked for user_id: {user_id}", user_id=user_id, path="/users/logout-all")
        return {"message": "Logged out from all devices"}