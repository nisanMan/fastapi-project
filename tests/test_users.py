#tests\users.py
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
