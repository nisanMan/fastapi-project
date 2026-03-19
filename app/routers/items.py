#app\routers\users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..auth.jwt_handler import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/items", tags=["Items"])

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials  # מחלץ את ה-token מה-header
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(models.User).filter(models.User.id == payload["user_id"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

#CROD

#Create
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

#Read
@router.get("/")
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()

# Update
@router.put("/{item_id}")
def update_item(
    item_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your item")

    db_item.title = item.title
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)

    return db_item


# Delete
@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your item")

    db.delete(db_item)
    db.commit()

    return {"message": "Item deleted"}