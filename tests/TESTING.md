# Testing Guide

## Overview

Tests use **pytest** with a separate **SQLite** database — production data is never affected.
Current coverage: **96%**

---

## Running Tests

```bash
# Run all tests
docker-compose run api pytest tests/ -v

# Run with coverage report
docker-compose run api pytest tests/ -v --cov=app --cov-report=term-missing

# Run a specific file
docker-compose run api pytest tests/test_users.py -v

# Run a specific test
docker-compose run api pytest tests/test_users.py::test_login -v
```

---

## Test Structure

```
tests/
├── conftest.py          # Fixtures and DB setup
├── factories.py         # Reusable test data creators
├── test_health.py       # Health check endpoint
├── test_users.py        # Auth — register, login, refresh, logout
├── test_items.py        # CRUD — create, read, update, delete
└── test_rate_limit.py   # Rate limiting — 429 responses
```

---

## Factory Pattern

Instead of repeating setup code in every test, use the factories:

```python
from tests.factories import create_user, create_item

# Create a user and get auth headers
user = create_user(client, email="test@example.com")
headers = user["headers"]            # Authorization header
refresh_token = user["refresh_token"]

# Create an item
item = create_item(client, headers, title="My Item")
item_id = item["id"]
```

### Available Factories

| Factory | Parameters | Returns |
|---|---|---|
| `create_user` | `client, email, password` | `headers, refresh_token, email, password` |
| `create_item` | `client, headers, title, description` | item object |

---

## Writing a New Test

```python
# tests/test_items.py

def test_my_new_feature(client, auth_headers):
    # 1. Arrange — create test data
    item = create_item(client, auth_headers, title="Test")

    # 2. Act — call the endpoint
    response = client.get(f"/items/{item['id']}", headers=auth_headers)

    # 3. Assert — check the result
    assert response.status_code == 200
    assert response.json()["title"] == "Test"
```

---

## Coverage Report

| Module | Coverage | Notes |
|---|---|---|
| `routers/` | 97-100% | Fully covered |
| `services/` | 100% | Fully covered |
| `repositories/` | 100% | Fully covered |
| `auth/` | 92-100% | JWT edge cases partially covered |
| `logger.py` | 83% | Console handler not triggered in tests |
| `database.py` | 65% | Initialization code, not testable |

---

## What Is Not Covered and Why

| Module | Missing Lines | Reason |
|---|---|---|
| `auth/jwt_handler.py` | 33-34, 66 | Edge cases — user deleted after token issued |
| `logger.py` | 12-19 | Console JSON handler — tested via Docker logs |
| `database.py` | 10, 14, 22-26 | DB engine initialization — not unit testable |
| `main.py` | 24-25 | Migration failure path — requires DB to be down |

---

## Fixtures

Defined in `conftest.py`:

| Fixture | Description |
|---|---|
| `client` | Test client with isolated SQLite DB, resets after each test |
| `auth_headers` | Authorization header for a registered and logged-in user |
| `auth_data` | Auth headers + refresh token cookie |