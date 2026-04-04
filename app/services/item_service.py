# app/services/item_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models, schemas
from ..repositories.item_repository import ItemRepository


class ItemService:
    def __init__(self, db: Session):
        self.repo = ItemRepository(db)

    def get_user_items(self, user_id: int):
        return self.repo.get_user_items(user_id)

    def get_all_paginated(self, page: int, limit: int):
        skip = (page - 1) * limit
        items, total = self.repo.get_all_paginated(skip, limit)
        return {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": -(-total // limit),
            "data": items
        }

    def create(self, item: schemas.ItemCreate, owner_id: int):
        return self.repo.create(item, owner_id)

    def update(self, item_id: int, item: schemas.ItemCreate, current_user: models.User):
        db_item = self.repo.get_by_id(item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        if db_item.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not your item")
        return self.repo.update(db_item, item)

    def delete(self, item_id: int, current_user: models.User):
        db_item = self.repo.get_by_id(item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        if db_item.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not your item")
        self.repo.soft_delete(db_item)
        return {"message": "Item deleted"}