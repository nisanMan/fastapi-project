# app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, timezone


def utcnow():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")
    refresh_tokens = relationship("RefreshToken", back_populates="user")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token_hash = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utcnow)  # ← תיקון

    user = relationship("User", back_populates="refresh_tokens")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=utcnow)           # ← תיקון
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)  # ← תיקון
    is_deleted = Column(Boolean, default=False)

    owner = relationship("User", back_populates="items")


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String)
    message = Column(String)
    user_id = Column(Integer, nullable=True)
    path = Column(String, nullable=True)
    method = Column(String, nullable=True)      # GET, POST...
    status_code = Column(Integer, nullable=True) # 200, 401...
    duration_ms = Column(Integer, nullable=True) # כמה זמן לקחה הבקשה
    ip = Column(String, nullable=True)           # IP של הלקוח
    created_at = Column(DateTime, default=utcnow)