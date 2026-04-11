# app/routers/health.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from ..database import get_db
from ..limiter import limiter
from ..config import settings
from sqlalchemy import text

router = APIRouter(tags=["Health"])

@router.get("/health",
    summary="Health check",
    responses={
        200: {"description": "App and database are healthy"},
    }
)
@limiter.limit(settings.DEFAULT_RATE_LIMIT)
async def health_check(request: Request, db: Session = Depends(get_db)):
    """Check the status of the app and database connection."""
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "database": db_status
    }