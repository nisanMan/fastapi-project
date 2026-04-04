# FastAPI Project

A production-ready REST API built with **FastAPI**, **PostgreSQL**, **Docker**, and **JWT Authentication**.
Structured with a clean **Repository & Service** architecture, fully containerized, tested, and deployed via CI/CD.

---

## Project Structure

```
fastapi_project/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── logger.py
│   ├── config.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   └── item_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   ├── routers/
│   │   ├── users.py
│   │   ├── items.py
│   │   └── health.py
│   └── auth/
│       ├── hashing.py
│       └── jwt_handler.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users.py
│   └── test_items.py
├── .env
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## Architecture

```
Request → Router → Service → Repository → DB
```

Each layer has a single responsibility:

| Layer | Responsibility |
|---|---|
| **Router** | HTTP only — receives requests, returns responses |
| **Service** | Business logic, validation, error handling |
| **Repository** | Database access only — all queries live here |

---

## Setup & Run

### Prerequisites
- Docker & Docker Compose

### Local Development

```bash
# Clone the repository
git clone <repo-url>
cd fastapi_project

# Create environment file
cp .env.example .env

# Build and start
docker-compose up --build
```

| | URL |
|---|---|
| API | `http://localhost:8000` |
| Swagger UI | `http://localhost:8000/docs` |
| Health Check | `http://localhost:8000/health` |

### Live Demo
Explore the deployed API: [railway.app/docs](https://fastapi-project-production-4bdc.up.railway.app/docs)

---

## Authentication

Register and login to receive a JWT token. Include it in all protected requests:

```
Authorization: Bearer <token>
```

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/users/register` | ❌ | Register a new user |
| POST | `/users/login` | ❌ | Login and receive JWT token |
| GET | `/items/` | ✅ | Get current user's items |
| GET | `/items/all` | ✅ | Get all items (paginated) |
| POST | `/items/` | ✅ | Create a new item |
| PUT | `/items/{id}` | ✅ | Update an item |
| DELETE | `/items/{id}` | ✅ | Soft delete an item |
| GET | `/health` | ❌ | App and database health status |

---

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT signing key |
| `ALGORITHM` | JWT algorithm (default: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry duration |

---

## Database Migrations (Alembic)

```bash
# Generate a migration after model changes
docker-compose run api alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose run api alembic upgrade head

# Rollback last migration
docker-compose run api alembic downgrade -1
```

### Direct DB Access

```bash
docker exec -it fastapi_postgres psql -U postgres -d fastapi_db
```

Useful commands: `\dt` to list tables, `SELECT * FROM items;` to query data.

---

## Tests

Tests use **pytest** with a separate **SQLite** database — production data is never affected.

```bash
docker-compose run api pytest tests/ -v
```

### Test Coverage

| Test | What it checks |
|---|---|
| `test_register` | Registration returns 201 |
| `test_register_duplicate` | Duplicate email returns 400 |
| `test_login` | Login returns a JWT token |
| `test_login_wrong_password` | Wrong password returns 401 |
| `test_create_item` | Item creation works correctly |
| `test_get_items` | Items returned for authenticated user |
| `test_delete_item` | Owner can delete their item |
| `test_delete_item_not_owner` | Non-owner receives 403 Forbidden |

---

## CI/CD

Every push to `master` triggers the following pipeline via GitHub Actions:

```
git push → Run Tests → Deploy to Railway (only if tests pass)
```

---

## Generics Guide
| File | Reusable? | Notes |
|---|---|---|
| `database.py` | ✅ Fully | Only the URL changes |
| `config.py` | ✅ Fully | Add fields as needed |
| `auth/hashing.py` | ✅ Fully | Nothing changes |
| `auth/jwt_handler.py` | ✅ Fully | Nothing changes |
| `repositories/user_repository.py` | ✅ Almost | Only if extra user fields needed |
| `services/user_service.py` | ✅ Almost | Only if extra user logic needed |
| `routers/users.py` | ✅ Almost | Only if extra user endpoints needed |
| `routers/health.py` | ✅ Fully | Nothing changes |
| `logger.py` | ✅ Fully | Nothing changes |
| `main.py` | ⚠️ Minimal | Add/remove routers only |
| `models.py` | ❌ Project-specific | Your tables |
| `schemas.py` | ❌ Project-specific | Follows your models |
| `repositories/item_repository.py` | ❌ Project-specific | Your DB queries |
| `services/item_service.py` | ❌ Project-specific | Your business logic |
| `routers/items.py` | ❌ Project-specific | Your endpoints |

---

## Roadmap

**v1.0 — Foundation**
- [x] Docker Compose
- [x] Git

**v1.1 — Core Features**
- [x] JWT Authentication
- [x] PostgreSQL
- [x] Full CRUD
- [x] Soft Delete

**v1.2 — Production Basics**
- [x] Alembic migrations
- [x] CORS
- [x] Pagination
- [x] Logging

**v1.3 — Testing**
- [x] pytest

**v1.4 — Deployment**
- [x] GitHub Repository
- [x] CI/CD (GitHub Actions)
- [x] Deploy (Railway)

**v1.5 — Architecture**
- [x] Config Class (pydantic-settings)
- [x] Repository & Service Pattern
- [x] Health Check endpoint

**v1.6 — Security**
- [ ] Rate Limiting
- [ ] Refresh Tokens
- [ ] Email Verification
- [ ] Password Reset

**v1.7 — Monitoring & Docs**
- [ ] Structured JSON Logging
- [ ] Metrics (request count, response time)
- [ ] Swagger descriptions per endpoint
- [ ] API Versioning `/api/v1/`

**v1.8 — Tests**
- [ ] Test Coverage Report
- [ ] Integration Tests
- [ ] Factory Pattern for test data

**v2.0 — Infrastructure**
- [ ] Redis (cache)
- [ ] Nginx (reverse proxy)
- [ ] Background Tasks
- [ ] Environment separation (dev / staging / prod)

<!--# 🚀 FastAPI Project
🐳 Docker

---
## 📁 ⚙️ Setup & Run

 🔐 Authentication
📌 API Endpoints

 🧱  🛠🗄️ 🧪 -->
![Repo views](https://komarev.com/ghpvc/?username=nisanMan&repo=fastapi-project)