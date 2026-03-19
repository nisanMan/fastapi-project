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
├── .env   
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
docker-compose down
docker-compose build --no-cache   #if needed new continer.
docker-compose up
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

## Git init:
```Bash
 git init
 type nul > .gitignore
```
📁  .gitignore:
```Text
__pycache__/
*.pyc
.env
venv/
.DS_Store
```
```Bash
git add .
git commit -m "Version 0 - Initial FastAPI Docker project"
git status
git log
```

| File | Generic? | What changes                              |
|------|----------|-------------------------------------------|
| `database.py` | ✅ Fully generic | Only the URL                              |
| `auth/hashing.py` | ✅ Fully generic | Nothing                                   |
| `auth/jwt_handler.py` | ✅ Fully generic | `SECRET_KEY` → from `.env`                |
| `routers/users.py` | ✅ Almost generic | Only if you need extra fields on the user |
| `models.py` | ❌ Changes | Your tables                               |
| `schemas.py` | ❌ Changes | According to your models                  |
| `routers/items.py` | ❌ Changes | Your business logic                       |
| `main.py` | ⚠️ Minimal changes | Add / remove routers                      |

