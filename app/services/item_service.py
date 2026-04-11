# app/services/item_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models, schemas
from ..repositories.item_repository import ItemRepository
from ..logger import log


class ItemService:
    def __init__(self, db: Session):
        self.repo = ItemRepository(db)
        self.db = db

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
        new_item = self.repo.create(item, owner_id)
        log(self.db, "INFO", "item_created",
            user_id=owner_id,
            path="/items/",
            method="POST",
            status_code=201)
        self.db.refresh(new_item)
        return new_item

    def update(self, item_id: int, item: schemas.ItemCreate, current_user: models.User):
        db_item = self.repo.get_by_id(item_id)
        if not db_item:
            log(self.db, "WARNING", "item_not_found",
                user_id=current_user.id,
                path=f"/items/{item_id}",
                method="PUT",
                status_code=404)
            raise HTTPException(status_code=404, detail="Item not found")
        if db_item.owner_id != current_user.id:
            log(self.db, "WARNING", "item_update_forbidden",
                user_id=current_user.id,
                path=f"/items/{item_id}",
                method="PUT",
                status_code=403)
            raise HTTPException(status_code=403, detail="Not your item")
        updated = self.repo.update(db_item, item)
        log(self.db, "INFO", "item_updated",
            user_id=current_user.id,
            path=f"/items/{item_id}",
            method="PUT",
            status_code=200)
        self.db.refresh(updated)
        return updated

    def delete(self, item_id: int, current_user: models.User):
        db_item = self.repo.get_by_id(item_id)
        if not db_item:
            log(self.db, "WARNING", "item_not_found",
                user_id=current_user.id,
                path=f"/items/{item_id}",
                method="DELETE",
                status_code=404)
            raise HTTPException(status_code=404, detail="Item not found")
        if db_item.owner_id != current_user.id:
            log(self.db, "WARNING", "item_delete_forbidden",
                user_id=current_user.id,
                path=f"/items/{item_id}",
                method="DELETE",
                status_code=403)
            raise HTTPException(status_code=403, detail="Not your item")
        self.repo.soft_delete(db_item)
        log(self.db, "INFO", "item_deleted",
            user_id=current_user.id,
            path=f"/items/{item_id}",
            method="DELETE",
            status_code=204)
        return {"message": "Item deleted"}