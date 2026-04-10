from fastapi import APIRouter, Depends, Cookie, Response, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..services.user_service import UserService
from ..auth.jwt_handler import decode_token
from ..limiter import limiter
from ..config import settings

router = APIRouter(prefix="/users", tags=["Users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.REGISTER_RATE_LIMIT)
async def register(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    return UserService(db).register(user)


@router.post("/login")
@limiter.limit(settings.LOGIN_RATE_LIMIT)
async def login(request: Request, user: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    return UserService(db).login(user, response)


@router.post("/refresh")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def refresh(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str | None = Cookie(default=None)
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token provided")
    return UserService(db).refresh(refresh_token, response)


@router.post("/logout")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str | None = Cookie(default=None)
):
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token provided")
    return UserService(db).logout(refresh_token, response)


@router.post("/logout-all")
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def logout_all(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    payload = decode_token(token)
    return UserService(db).logout_all(payload["user_id"], response)