# app/repositories/user_repository.py
from sqlalchemy.orm import Session
from .. import models, schemas
from ..auth.hashing import hash_password


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> models.User | None:
        return self.db.query(models.User).filter(models.User.email == email).first()

    def create(self, user: schemas.UserCreate) -> models.User:
        new_user = models.User(
            email=user.email,
            password=hash_password(user.password),
            phone=user.phone
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user