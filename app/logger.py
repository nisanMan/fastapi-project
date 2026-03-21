#app/logger.py
from sqlalchemy.orm import Session
from . import models

def log(db: Session, level: str, message: str, user_id: int = None, path: str = None):
    entry = models.Log(
        level=level,
        message=message,
        user_id=user_id,
        path=path
    )
    db.add(entry)
    db.commit()



