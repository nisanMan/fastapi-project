#app\routers\users.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)


@router.post("/")
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):

    new_item = models.Item(
        title=item.title,
        description=item.description
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@router.get("/")
def get_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return items





