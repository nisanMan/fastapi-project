# tests/test_users.py

def test_register(client):
    response = client.post("/users/register", json={
        "email": "test@example.com",
        "password": "123456"
    })
    assert response.status_code == 201
    assert response.json()["message"] == "User created"


def test_register_duplicate(client):
    client.post("/users/register", json={
        "email": "test@example.com",
        "password": "123456"
    })
    response = client.post("/users/register", json={
        "email": "test@example.com",
        "password": "123456"
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"


def test_register_invalid_email(client):
    response = client.post("/users/register", json={
        "email": "not-an-email",
        "password": "123456"
    })
    assert response.status_code == 422


def test_login(client):
    client.post("/users/register", json={
        "email": "test@example.com",
        "password": "123456"
    })
    response = client.post("/users/login", json={
        "email": "test@example.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.cookies.get("refresh_token") is not None


def test_login_wrong_password(client):
    client.post("/users/register", json={
        "email": "test@example.com",
        "password": "123456"
    })
    response = client.post("/users/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post("/users/login", json={
        "email": "nobody@example.com",
        "password": "123456"
    })
    assert response.status_code == 404


# ───── Refresh Token ─────

def test_refresh(client, auth_data):
    client.cookies.set("refresh_token", auth_data["refresh_token"])
    response = client.post("/users/refresh")
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.cookies.get("refresh_token") is not None


def test_refresh_rotates_token(client, auth_data):
    old_refresh = auth_data["refresh_token"]
    client.cookies.set("refresh_token", old_refresh)
    response = client.post("/users/refresh")
    new_refresh = response.cookies.get("refresh_token")
    assert new_refresh != old_refresh


def test_refresh_old_token_invalid(client, auth_data):
    old_refresh = auth_data["refresh_token"]
    client.cookies.set("refresh_token", old_refresh)
    client.post("/users/refresh")

    client.cookies.set("refresh_token", old_refresh)
    response = client.post("/users/refresh")
    assert response.status_code == 401


def test_refresh_no_cookie(client):
    response = client.post("/users/refresh")
    assert response.status_code == 401


# ───── Logout ─────

def test_logout(client, auth_data):
    client.cookies.set("refresh_token", auth_data["refresh_token"])
    response = client.post("/users/logout")
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out"


def test_logout_invalidates_token(client, auth_data):
    client.cookies.set("refresh_token", auth_data["refresh_token"])
    client.post("/users/logout")

    client.cookies.set("refresh_token", auth_data["refresh_token"])
    response = client.post("/users/refresh")
    assert response.status_code == 401


# ───── Logout All ─────

def test_logout_all(client, auth_data):
    response = client.post("/users/logout-all", headers=auth_data["headers"])
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out from all devices"


def test_logout_all_invalidates_all_tokens(client, auth_data):
    client.post("/users/logout-all", headers=auth_data["headers"])

    client.cookies.set("refresh_token", auth_data["refresh_token"])
    response = client.post("/users/refresh")
    assert response.status_code == 401

def test_access_protected_route_without_token(client):
    response = client.get("/items/")
    assert response.status_code == 403

