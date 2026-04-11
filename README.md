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
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── logger.py
│   ├── config.py
│   ├── limiter.py
│   │ 
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   └── item_repository.py
│   │ 
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   │ 
│   ├── routers/
│   │   ├── users.py
│   │   ├── items.py
│   │   └── health.py
│   │ 
│   └── auth/
│       ├── hashing.py
│       └── jwt_handler.py
│ 
├── tests/
│   ├── TESTING.md
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_users.py
│   ├── test_rate_limit.py
│   ├── factories.py
│   └── test_items.py
│ 
├── .env
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## Architecture

```
Request → SlowAPI (rate limit) → CORS → Router → Service → Repository → DB
```
Each layer has a single responsibility:

| Layer | Responsibility |
|---|---|
| **SlowAPI** | Rate limiting — blocks excessive requests |
| **CORS** | Cross-origin policy — controls who can call the API |
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

This API uses a two-token system:

| Token | Storage | Lifetime | Purpose |
|---|---|---|---|
| Access Token | Authorization header | 30 minutes | Authenticate requests |
| Refresh Token | httpOnly cookie | 7 days | Issue new access tokens |

### Flow
```
Register → Login → receive Access Token + Refresh Token cookie
→ use Access Token for protected requests
→ when expired, call /users/refresh to get a new one
```
### Protected requests
Authorization: Bearer <access_token>


---

## 🚀 API Endpoints

| Category | Method | Endpoint | Auth | Description |
|---|---|---|---|---|
| Users | POST | `/users/register` | ❌ | Register a new user |
| Users | POST | `/users/login` | ❌ | Login and receive JWT + refresh cookie |
| Users | POST | `/users/refresh` | ❌ | Get new access token using refresh token |
| Users | POST | `/users/logout` | ⚠️ | Logout — requires refresh token cookie |
| Users | POST | `/users/logout-all` | ✅ | Logout from all sessions |
| Items | GET | `/items/` | ✅ | Get current user's items |
| Items | GET | `/items/all` | ✅ | Get all items (paginated) |
| Items | POST | `/items/` | ✅ | Create a new item |
| Items | PUT | `/items/{item_id}` | ✅ | Update an item |
| Items | DELETE | `/items/{item_id}` | ✅ | Soft delete an item |
| Health | GET | `/health` | ❌ | App and database health status |

---

## Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | JWT signing key |
| `ALGORITHM` | JWT algorithm (default: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry duration |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiry duration |
| `DEFAULT_RATE_LIMIT` | Default rate limit (default: `100/minute`) |
| `LOGIN_RATE_LIMIT` | Login rate limit (default: `5/minute`) |
| `REGISTER_RATE_LIMIT` | Register rate limit (default: `3/minute`) |
| `ITEMS_READ_RATE_LIMIT` | Items read rate limit (default: `60/minute`) |
| `ITEMS_WRITE_RATE_LIMIT` | Items write rate limit (default: `30/minute`) |

---

## Database Migrations (Alembic)

> Migrations run automatically on every deployment via `main.py`.
> Use the commands below for local development only.

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

For the full testing guide including factory pattern, coverage breakdown, and how to write new tests:

→ See [TESTING.md](tests/TESTING.md)

---

## CI/CD

Every push to `master` triggers the following pipeline via GitHub Actions:

```
git push → Run Tests → Deploy to Railway (only if tests pass) → Run Migrations
```
| Step | Description |
|---|---|
| **Run Tests** | pytest with SQLite — production DB is never touched |
| **Deploy** | Railway deployment — only if all tests pass |
| **Migrations** | Alembic runs automatically on app startup |
---

## Generics Guide

| File | Reusable? | Notes |
|---|---|---|
| `database.py` | ✅ Fully | Only the URL changes |
| `config.py` | ✅ Fully | Add fields as needed |
| `auth/hashing.py` | ✅ Fully | Nothing changes |
| `auth/jwt_handler.py` | ✅ Almost | Only if auth scheme changes |
| `repositories/user_repository.py` | ✅ Almost | Only if extra user fields needed |
| `services/user_service.py` | ✅ Almost | Only if extra user logic needed |
| `routers/users.py` | ✅ Almost | Only if extra user endpoints needed |
| `routers/health.py` | ✅ Fully | Nothing changes |
| `logger.py` | ✅ Fully | Nothing changes |
| `limiter.py` | ✅ Fully | Only change default limits in config |
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
- [X] Rate Limiting
- [X] Refresh Tokens
- [~] Email Verification
- [~] Password Reset

**v1.7 — Monitoring & Docs**
- [x] Swagger descriptions per endpoint
- [x] Structured JSON Logging
- [~] API Versioning `/api/v1/` — skipped, planned for v2.0
- [~] Metrics — skipped, planned for v2.0

**v1.8 — Tests**
- [x] Test Coverage Report (96%)
- [x] Factory Pattern for test data
- [~] Integration Tests — skipped, planned for v2.0

**v2.0 — Infrastructure**
- [ ] Redis (cache)
- [ ] Nginx (reverse proxy)
- [ ] Background Tasks
- [ ] Environment separation (dev / staging / prod)
- [ ] CMD alembic upgrade head && uvicorn app.main:app



<!--# 🚀 FastAPI Project
🐳 Docker

---
## 📁 ⚙️ Setup & Run

 🔐 Authentication
📌 API Endpoints

 🧱  🛠🗄️ 🧪 -->
![Repo views](https://komarev.com/ghpvc/?username=nisanMan&repo=fastapi-project)


```bash
curl -X POST https://<your-api>/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"yourpassword"}'
```