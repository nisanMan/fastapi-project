 #tests\test_items.py
 # tests/test_items.py

def get_token(client):
    client.post("/users/register", json={
        "email": "test@example.com",
        "password": "123456"
    })
    response = client.post("/users/login", json={
        "email": "test@example.com",
        "password": "123456"
    })
    return response.json()["access_token"]


def test_create_item(client):
    token = get_token(client)
    response = client.post("/items/", json={
        "title": "Test Item",
        "description": "Test Description"
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Item"


def test_get_items(client):
    token = get_token(client)
    client.post("/items/", json={
        "title": "Test Item",
        "description": "Test Description"
    }, headers={"Authorization": f"Bearer {token}"})
    response = client.get("/items/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_delete_item(client):
    token = get_token(client)
    create = client.post("/items/", json={
        "title": "Test Item",
        "description": "Test Description"
    }, headers={"Authorization": f"Bearer {token}"})
    item_id = create.json()["id"]
    response = client.delete(f"/items/{item_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted"


def test_delete_item_not_owner(client):
    # יוצר משתמש ראשון עם item
    token1 = get_token(client)
    create = client.post("/items/", json={
        "title": "Test Item",
        "description": "Test Description"
    }, headers={"Authorization": f"Bearer {token1}"})
    item_id = create.json()["id"]

    # משתמש שני מנסה למחוק
    client.post("/users/register", json={
        "email": "other@example.com",
        "password": "123456"
    })
    response2 = client.post("/users/login", json={
        "email": "other@example.com",
        "password": "123456"
    })
    token2 = response2.json()["access_token"]

    response = client.delete(f"/items/{item_id}", headers={"Authorization": f"Bearer {token2}"})
    assert response.status_code == 403
