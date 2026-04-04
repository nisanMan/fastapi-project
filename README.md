# 🚀 FastAPI Project

A REST API built with FastAPI, PostgreSQL, Docker, and JWT Authentication.
A minimal backend project built with FastAPI, fully containerized using Docker. This project serves as a foundation for building scalable REST APIs.
---
## 📁 Project Structure
```
fastapi_project/
├── .github/                  
│   └── workflows/            
│       └── ci.yml 
├──app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── logger.py
│   ├── config.py
│   │
│   ├──repositories/
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   └──item_repository.py
│   │
│   ├──services/
│   │   ├──__init__.py
│   │   ├──user_service.py
│   │   └──item_service.py
│   │
│   ├── routers       !
│   │   ├── users.py  !
│   │   └── items.py  !
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
## 🛠 Next Steps 
>V1.0
- [X] Use Docker Compose
- [X] Use GIT
>v1.1
- [X] JWT auth
- [X] PostgreSQL connection
- [X] Implement full CRUD 
- [X] Implement Soft Delete
>v1.2
- [x] Alembic migrations
- [x] CORS
- [X] Pagination
- [X] Logging
>v1.3
- [X] Tests (pytest)
>v1.4
- [x] GitHub Repository
- [X] CI/CD (GitHub Actions)
- [X] Deploy (Railway)

>v1.5 — Architecture & Config
- [X] Config Class (pydantic-settings)
- [X] Repository & Service Pattern
- [ ] Health Check endpoint

> ```Request → Router → Service → Repository → DB```

> v1.6 — Security
- [ ] Rate Limiting
- [ ] Refresh Tokens
- [ ] Email Verification
- [ ] Password Reset

> v1.7 — Monitoring & Docs
- [ ] Structured JSON Logging
- [ ] Metrics (request count, response time)
- [ ] Swagger descriptions per endpoint
- [ ] API Versioning `/api/v1/`

> v1.8 — Tests
- [ ] Test Coverage Report
- [ ] Integration Tests
- [ ] Factory Pattern for test data

> v2.0 — Infrastructure
- [ ] Redis (cache)
- [ ] Nginx (reverse proxy)
- [ ] Background tasks
- [ ] Environment separation (dev / staging / prod)

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


## 🧪 Tests

Tests are written with **pytest** and use a separate **SQLite** database
so they never affect production data.

### Run tests
```bash
docker-compose run api pytest tests/ -v
```

### Test coverage

| File | Tests |
|------|-------|
| `test_users.py` | register, duplicate register, login, wrong password |
| `test_items.py` | create, get, delete, delete by non-owner (403) |

| Test | What it checks |
|------|---------------|
| `test_register` | Registration returns 201 |
| `test_register_duplicate` | Duplicate email returns 400 |
| `test_login` | Login returns a JWT token |
| `test_login_wrong_password` | Wrong password returns 401 |
| `test_create_item` | Item creation works correctly |
| `test_get_items` | Items are returned for authenticated user |
| `test_delete_item` | Owner can delete their item |
| `test_delete_item_not_owner` | Non-owner gets 403 Forbidden |