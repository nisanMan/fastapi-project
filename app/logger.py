# app/logger.py
import logging
import json
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from . import models

# ───── JSON Console Logger ─────

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "time": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        return json.dumps(log_data)


handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False


# ───── DB + Console Logger ─────

def log(
    db: Session,
    level: str,
    message: str,
    user_id: int = None,
    path: str = None,
    method: str = None,
    status_code: int = None,
    duration_ms: int = None,
    ip: str = None,
):
    extra = {
        k: v for k, v in {
            "user_id": user_id,
            "path": path,
            "method": method,
            "status_code": status_code,
            "duration_ms": duration_ms,
            "ip": ip,
        }.items() if v is not None
    }

    log_func = {
        "INFO": logger.info,
        "WARNING": logger.warning,
        "ERROR": logger.error,
    }.get(level.upper(), logger.info)

    log_func(message, extra={"extra": extra})

    entry = models.Log(
        level=level.upper(),
        message=message,
        user_id=user_id,
        path=path,
        method=method,
        status_code=status_code,
        duration_ms=duration_ms,
        ip=ip,
    )
    db.add(entry)
    db.commit()