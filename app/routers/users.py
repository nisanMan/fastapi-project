# app/routers/users.py
from fastapi import APIRouter, Depends, Cookie, Response, HTTPException, status, Request
from sqlalchemy.orm import Session
from .. import schemas
from ..database import get_db
from ..services.user_service import UserService
from ..auth.jwt_handler import decode_token, security
from fastapi.security import HTTPAuthorizationCredentials
from ..limiter import limiter
from ..config import settings

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Email already registered"},
    }
)
@limiter.limit(settings.REGISTER_RATE_LIMIT)
async def register(request: Request, user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    - **email**: must be a valid email address
    - **password**: minimum 6 characters
    """
    return UserService(db).register(user)


@router.post("/login",
    summary="Login and receive tokens",
    responses={
        200: {"description": "Access token returned, refresh token set as cookie"},
        401: {"description": "Wrong password"},
        404: {"description": "User not found"},
    }
)
@limiter.limit(settings.LOGIN_RATE_LIMIT)
async def login(request: Request, user: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    """
    Login with email and password.

    - Returns a JWT **access token**
    - Sets a **refresh token** as an httpOnly cookie
    """
    return UserService(db).login(user, response)


@router.post("/refresh",
    summary="Refresh access token",
    responses={
        200: {"description": "New access token returned"},
        401: {"description": "Invalid or expired refresh token"},
    }
)
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def refresh(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str | None = Cookie(default=None)
):
    """Rotate the refresh token and return a new access token."""
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token provided")
    return UserService(db).refresh(refresh_token, response)


@router.post("/logout",
    summary="Logout from current session",
    responses={
        200: {"description": "Logged out successfully"},
        401: {"description": "No refresh token provided"},
    }
)
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: str | None = Cookie(default=None)
):
    """Invalidate the current refresh token."""
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token provided")
    return UserService(db).logout(refresh_token, response)


@router.post("/logout-all",
    summary="Logout from all devices",
    responses={
        200: {"description": "Logged out from all devices"},
        401: {"description": "Invalid or expired token"},
    }
)
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def logout_all(
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Invalidate all refresh tokens for the current user."""
    payload = decode_token(credentials.credentials)
    return UserService(db).logout_all(payload["user_id"], response)