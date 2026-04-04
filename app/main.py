#app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models

from .routers import users, items, health

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  #frontend URL
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"], 
    allow_headers=["*"],   # Authorization, Content-Type
)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(health.router)