# app/repositories/token_repository.py

from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models import RefreshToken


def save_refresh_token(db: Session, user_id: int, token_hash: str, expires_at: datetime) -> RefreshToken:
    """שומר טוקן חדש ב-DB"""
    db_token = RefreshToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_token_by_hash(db: Session, token_hash: str) -> RefreshToken | None:
    """מחפש טוקן לפי hash"""
    return db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash,
        RefreshToken.revoked == False,
        RefreshToken.expires_at > datetime.now(timezone.utc)
    ).first()


def revoke_token(db: Session, token_hash: str) -> None:
    """מבטל טוקן ספציפי"""
    db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash
    ).update({"revoked": True})
    db.commit()


def revoke_all_user_tokens(db: Session, user_id: int) -> None:
    """מבטל את כל הטוקנים של משתמש — logout מכל המכשירים"""
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id
    ).update({"revoked": True})
    db.commit()


def delete_expired_tokens(db: Session) -> None:
    """מוחק טוקנים פגי תוקף — ירוץ ברקע"""
    db.query(RefreshToken).filter(
        RefreshToken.expires_at < datetime.now(timezone.utc)
    ).delete()
    db.commit()