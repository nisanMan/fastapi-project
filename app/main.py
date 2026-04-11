#app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from .database import engine
from . import models
from .routers import users, items, health
from app.limiter import limiter
#fiocher to delet
from alembic.config import Config
from alembic import command
import logging

logger = logging.getLogger("app")

def run_migrations():
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Migrations completed successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}")

run_migrations()
# up to her delet
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Project",
    description="A production-ready REST API with JWT authentication, refresh tokens, and rate limiting.",
    version="1.7.0",
    contact={
        "name": "nisanMan",
        "url": "https://github.com/nisanMan/fastapi-project",
    },
    license_info={
        "name": "MIT",
    }
)

app.add_middleware(SlowAPIMiddleware)

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  #frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"], 
    allow_headers=["*"],   # Authorization, Content-Type
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(health.router)

