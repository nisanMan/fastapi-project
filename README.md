# 🚀 FastAPI Docker Backend

A minimal backend project built with FastAPI, fully containerized using Docker. This project serves as a foundation for building scalable REST APIs.
---
## 📁 Project Structure
```
fastapi_project/
│
├──app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   │
│   ├── routers
│   │   ├── users.py
│   │   └── items.py
│   │
│   └── auth
│       ├── hashing.py
│       └── jwt_handler.py
│   
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── Readme

*gitignor
*readgit

```
## 🧱 Architecture Overview
#### main.py

- App entry point

- Registers routers

#### database.py

- Database connection

- SQLAlchemy session

#### models.py

- Database tables

#### schemas.py

- Pydantic validation models

#### auth.py

- Password hashing

- JWT creation & validation

#### routers/users.py

- Register

- Login

Protected routes
---
## 📌 main.py

* Initializes the FastAPI application
* Defines API routes
* Runs via Uvicorn inside Docker
* Example:
```Python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀"}
```
---
## 📦 requirements.txt

Defines all required dependencies:

* fastapi
* uvicorn
* sqlalchemy
* psycopg2-binary
* python-jose
* passlib[bcrypt]

Installed automatically during Docker build.
---
## 🐳 Dockerfile

Responsible for:
* Using Python 3.11 slim image
* Installing dependencies
* Copying project files
* Exposing port 8000
* Running the FastAPI server
---
## ▶️ How to Run
> Enter the directory from CMD and run:
> * The Docker app needs to be running.
<!--
#### 1️⃣ Build the Docker image
```Bash
docker build -t fastapi-app .
```
#### 2️⃣ Run the container
```Bash
docker run -p 8000:8000 fastapi-app
``` 
-->
#### 1️⃣ Build the App whit Docker
```Bash
docker compose down --if alrady run befor
docker compose up
```
#### 2️⃣ Access the API

* App: http://localhost:8000

* Swagger Docs: http://localhost:8000/docs

#### for dirct SQL :
```Bash
docker exec -it fastapi_postgres psql -U postgres -d fastapi_db
```
> for exmple:
>
> * \dt
> * select * from items;

---
## 🔥 Current Features

* FastAPI server
* Dockerized environment
* Automatic API documentation
* Ready for CRUD implementation
* Ready for PostgreSQL integration
---
## 🛠 Next Steps

- [ ] Add PostgreSQL connection

- [ ] Implement full CRUD
- [ ] Add JWT Authentication
- [ ] Use Docker Compose
- [ ] Deploy to cloud (AWS / Railway / Render)

## 🛠 Next Steps v.2
- [ ] Alembic (migrations)
- [ ] Redis (cache)
- [ ] Nginx (reverse proxy)
- [ ] JWT auth


<!--
FastAPI Docker Backend Project – Summary
Project Overview

This project is a containerized backend API built with FastAPI and PostgreSQL.
It allows creating and retrieving items via REST endpoints and demonstrates:

FastAPI backend development

PostgreSQL integration with SQLAlchemy ORM

Docker containerization

Docker Compose multi-service setup (API + DB)

Architecture
Client (Browser / Postman)
          │
          ▼
      FastAPI API
          │
          ▼
     SQLAlchemy ORM
          │
          ▼
      PostgreSQL DB

Docker Compose setup:

docker-compose
│
├── api (FastAPI container)
└── db  (PostgreSQL container)
Project Structure
fastapi_project/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
│
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
Requirements (requirements.txt)
fastapi
uvicorn
sqlalchemy
psycopg2-binary
email-validator
Database Configuration (app/database.py)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:password@db:5432/fastapi_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Database Models (app/models.py)
from sqlalchemy import Column, Integer, String
from .database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
Pydantic Schemas (app/schemas.py)
from pydantic import BaseModel, EmailStr

# Users schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Items schemas
class ItemCreate(BaseModel):
    name: str
    description: str

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True
FastAPI Application (app/main.py)
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "FastAPI Docker Backend is running 🚀"}

# Create item
@app.post("/items", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    db_item = models.Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# Get all items
@app.get("/items")
def get_items(db: Session = Depends(get_db)):
    return db.query(models.Item).all()
Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
Docker Compose (docker-compose.yml)
version: "3.9"

services:

  db:
    image: postgres:15
    container_name: fastapi_postgres
    restart: always
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
      POSTGRES_DB: fastapi_db
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  api:
    build: .
    container_name: fastapi_api
    depends_on:
      db:
        condition: service_healthy
    ports:
      - "8000:8000"
Running the Project
# Stop existing containers
docker compose down

# Build and run containers
docker compose up --build

Access API docs at: http://localhost:8000/docs

Example Requests:

Create item

POST /items

{
  "name": "Laptop",
  "description": "Gaming laptop"
}

Get items

GET /items