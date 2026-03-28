# 🚀 FastAPI Project

A REST API built with FastAPI, PostgreSQL, Docker, and JWT Authentication.
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
│   ├── logger.py
│   │
│   ├── routers
│   │   ├── users.py
│   │   └── items.py
│   │
│   └── auth
│       ├── hashing.py
│       └── jwt_handler.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users.py
│   └── test_items.py
│ 
├── .env   
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── Readme

*gitignor
*readgit
*sqlalchemy

```
## ⚙️ Setup & Run
```bash
# Clone the project
git clone 

# Create .env file
cp .env.example .env

# Build and run
docker-compose up --build
```
API available at: `http://localhost:8000`

Swagger docs: `http://localhost:8000/docs`

---
## 🔐 Authentication

Register and login to receive a JWT token.
Include it in requests as: `Authorization: Bearer <token>`
---
# 📌 API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/users/register` | ❌ | Register new user |
| POST | `/users/login` | ❌ | Login and get token |
| GET | `/items/` | ✅ | Get your items |
| GET | `/items/all` | ✅ | Get all items |
| POST | `/items/` | ✅ | Create item |
| PUT | `/items/{id}` | ✅ | Update item |
| DELETE | `/items/{id}` | ✅ | Delete item |

---
## 🗄️ Database Migrations (Alembic)
```bash
# Create migration after model change
docker-compose run api alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose run api alembic upgrade head

# Rollback last migration
docker-compose run api alembic downgrade -1
```

---

## 🧱 Architecture Overview
#### !!!
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

## ▶️ How to Run
> Enter the directory from CMD and run:
> * The Docker app needs to be running.

#### 1️⃣ Build the App whit Docker
```Bash
docker-compose down
docker compose up --build
# OR if needed new continer:
docker-compose build --no-cache
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
## 🛠 Next Steps V1.0
- [X] Use Docker Compose
- [X] Use GIT
- [ ] GITHUB repository

## 🛠 Next Steps v1.1
- [X] JWT auth
- [X] PostgreSQL connection
- [X] Implement full CRUD 
- [X] Implement Soft Delete

### v1.2
- [x] Alembic migrations
- [x] CORS
- [X] Pagination
- [ ] Tests (pytest)
- [X] Logging
- [ ] Rate limiting
- [ ] Redis (cache)
- [ ] Nginx (reverse proxy)
- [ ] Deploy (Railway / Render)
- [ ] Background tasks

### v1.3
- [ ] Background tasks
- [ ] Environment separation (dev / staging / prod)
- [ ] CI/CD (GitHub Actions)

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
## Generic? ✅ Yes ❌ No 
| File | Generic? | What changes                              |
|------|----------|-------------------------------------------|
| `database.py` | ✅ Fully generic | Only the URL                              |
| `auth/hashing.py` | ✅ Fully generic | Nothing                                   |
| `auth/jwt_handler.py` | ✅ Fully generic | Nothing       |
| `routers/users.py` | ✅ Almost generic | Only if you need extra fields on the user |
| `models.py` | ❌ Changes | Your tables                               |
| `schemas.py` | ❌ Changes | According to your models                  |
| `routers/items.py` | ❌ Changes | Your business logic                       |
| `main.py` | ⚠️ Minimal changes | Add / remove routers                      |

## Generic? ✅ Yes ❌ No
```
fastapi_project/
│
├──app/
│   ├── main.py ✅ Minimal changes | Add / remove routers ❌
│   ├── models.py ❌ Your tables
│   ├── schemas.py ❌  According to models
│   ├── database.py ✅
│   │
│   ├── routers 
│   │   ├── users.py ✅ Only if need extra fields in user ❌
│   │   ├── ...❌
│   │   └── items.py ❌ According to API logic
│   │
│   └── auth ✅
│       ├── hashing.py ✅
│       └── jwt_handler.py ✅
└── ...
```
## 🗄️ Database Migrations (Alembic)
```bash
# Create migration after model change
docker-compose run api alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose run api alembic upgrade head

# Rollback last migration
docker-compose run api alembic downgrade -1
```

id |                 title                  |                   description                   | owner_id |         created_at         |         updated_at         | is_deleted
----+----------------------------------------+-------------------------------------------------+----------+----------------------------+----------------------------+------------
2 | my user user@example.com me pasword is | 123456                                          |        1 |                            |                            |
4 | nisan@example.com                      | 654321                                          |        2 |                            |                            |
8 | the 3 user is NewUser@example.com      | my password is 111111 don't tale it is a secret |        3 |                            |                            |
10 | i posted it for soft delete            | string of garbage                               |        1 | 2026-03-21 11:30:54.334735 | 2026-03-21 11:30:54.334739 | f
9 | i posted it for soft delete            | string of garbage                               |        1 | 2026-03-21 11:30:48.55164  | 2026-03-21 11:31:32.10828  | t
(5 rows)