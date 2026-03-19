#app\schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone: str = None #Alembic 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ItemCreate(BaseModel):
    title: str
    description: str

class ItemResponse(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True


    