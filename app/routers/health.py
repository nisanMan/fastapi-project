# app/routers/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import text

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "database": db_status
    }