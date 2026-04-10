#tests/test_rate_limit.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_login_rate_limit():
    payload = {"email": "x@x.com", "password": "wrong"}
    
    for _ in range(5):
        client.post("/users/login", json=payload)

    response = client.post("/users/login", json=payload)
    assert response.status_code == 429


def test_register_rate_limit():
    for i in range(3):
        client.post("/users/register", json={
            "email": f"test{i}@test.com",
            "password": "123456"
        })

    response = client.post("/users/register", json={
        "email": "over@limit.com",
        "password": "123456"
    })
    assert response.status_code == 429


def test_rate_limit_response_format():
    payload = {"email": "x@x.com", "password": "wrong"}
    
    for _ in range(5):
        client.post("/users/login", json=payload)

    response = client.post("/users/login", json=payload)
    assert response.status_code == 429
    assert "error" in response.json()