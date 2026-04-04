# app/repositories/item_repository.py
from sqlalchemy.orm import Session
from .. import models, schemas


class ItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_items(self, user_id: int) -> list[models.Item]:
        return self.db.query(models.Item).filter(
            models.Item.owner_id == user_id,
            models.Item.is_deleted == False
        ).all()

    def get_all_paginated(self, skip: int, limit: int):
        items = self.db.query(models.Item).offset(skip).limit(limit).all()
        total = self.db.query(models.Item).count()
        return items, total

    def get_by_id(self, item_id: int) -> models.Item | None:
        return self.db.query(models.Item).filter(
            models.Item.id == item_id,
            models.Item.is_deleted == False
        ).first()

    def create(self, item: schemas.ItemCreate, owner_id: int) -> models.Item:
        new_item = models.Item(
            title=item.title,
            description=item.description,
            owner_id=owner_id
        )
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item

    def update(self, db_item: models.Item, item: schemas.ItemCreate) -> models.Item:
        db_item.title = item.title
        db_item.description = item.description
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def soft_delete(self, db_item: models.Item) -> None:
        db_item.is_deleted = True
        self.db.commit()