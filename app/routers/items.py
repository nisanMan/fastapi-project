#app\routers\users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..auth.jwt_handler import decode_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/items", tags=["Items"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/")
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # מחייב התחברות
):
    new_item = models.Item(
        title=item.title,          # היה item.name — לא קיים
        description=item.description,
        owner_id=current_user.id   # חסר לחלוטין קודם
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

@router.get("/")
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()