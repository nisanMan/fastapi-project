# app/routers/users.py

from fastapi import APIRouter, Depends, Cookie, Response, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..services.user_service import UserService
from ..auth.jwt_handler import decode_token

router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return UserService(db).register(user)


@router.post("/login")
def login(user: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    return UserService(db).login(user, response)


@router.post("/refresh")
def refresh(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str | None = Cookie(default=None)
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token provided")
    return UserService(db).refresh(refresh_token, response)


@router.post("/logout")
def logout(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str | None = Cookie(default=None)
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token provided")
    return UserService(db).logout(refresh_token, response)


@router.post("/logout-all")
def logout_all(
    response: Response,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)   # ← Access Token בלבד
):
    payload = decode_token(token)
    return UserService(db).logout_all(payload["user_id"], response)