# app/routers/items.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..auth.jwt_handler import decode_token
from ..services.item_service import ItemService
from ..limiter import limiter
from ..config import settings
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/items", tags=["Items"])
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = decode_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/", status_code=201)
@limiter.limit(settings.ITEMS_WRITE_RATE_LIMIT)
async def create_item(request: Request, item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return ItemService(db).create(item, current_user.id)

@router.get("/")
@limiter.limit(settings.ITEMS_READ_RATE_LIMIT)
async def get_my_items(request: Request, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return ItemService(db).get_user_items(current_user.id)

@router.get("/all")
@limiter.limit(settings.ITEMS_READ_RATE_LIMIT)
async def get_all_items(request: Request, page: int = 1, limit: int = 10, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return ItemService(db).get_all_paginated(page, limit)

@router.put("/{item_id}")
@limiter.limit(settings.ITEMS_WRITE_RATE_LIMIT)
async def update_item(request: Request, item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return ItemService(db).update(item_id, item, current_user)

@router.delete("/{item_id}", status_code=204)
@limiter.limit(settings.ITEMS_WRITE_RATE_LIMIT)
async def delete_item(request: Request, item_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return ItemService(db).delete(item_id, current_user)