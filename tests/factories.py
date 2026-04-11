# tests/factories.py

def create_user(client, email="test@example.com", password="123456"):
    client.post("/users/register", json={"email": email, "password": password})
    response = client.post("/users/login", json={"email": email, "password": password})
    token = response.json()["access_token"]
    refresh_token = response.cookies.get("refresh_token")
    return {
        "headers": {"Authorization": f"Bearer {token}"},
        "refresh_token": refresh_token,
        "email": email,
        "password": password,
    }


def create_item(client, headers, title="Test Item", description="Test Description"):
    response = client.post("/items/", json={
        "title": title,
        "description": description
    }, headers=headers)
    return response.json()