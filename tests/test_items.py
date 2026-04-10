# tests/test_items.py

def test_create_item(client, auth_headers):
    response = client.post("/items/", json={
        "title": "Test Item",
        "description": "Test Description"
    }, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Item"


def test_get_items_empty(client, auth_headers):
    response = client.get("/items/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_get_items(client, auth_headers):
    client.post("/items/", json={
        "title": "Test Item",
        "description": "Test Description"
    }, headers=auth_headers)
    response = client.get("/items/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_all_items(client, auth_headers):
    for i in range(3):
        client.post("/items/", json={
            "title": f"Item {i}",
            "description": "desc"
        }, headers=auth_headers)
    response = client.get("/items/all?page=1&limit=10", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert data["page"] == 1
    assert len(data["data"]) == 3


def test_update_item(client, auth_headers):
    create = client.post("/items/", json={
        "title": "Old Title",
        "description": "Old Desc"
    }, headers=auth_headers)
    item_id = create.json()["id"]
    response = client.put(f"/items/{item_id}", json={
        "title": "New Title",
        "description": "New Desc"
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"


def test_update_item_not_owner(client, auth_headers):
    create = client.post("/items/", json={
        "title": "Test Item",
        "description": "desc"
    }, headers=auth_headers)
    item_id = create.json()["id"]

    client.post("/users/register", json={
        "email": "other@example.com",
        "password": "123456"
    })
    response2 = client.post("/users/login", json={
        "email": "other@example.com",
        "password": "123456"
    })
    token2 = response2.json()["access_token"]

    response = client.put(f"/items/{item_id}", json={
        "title": "Hacked",
        "description": "Hacked"
    }, headers={"Authorization": f"Bearer {token2}"})
    assert response.status_code == 403


def test_delete_item(client, auth_headers):
    create = client.post("/items/", json={
        "title": "Test Item",
        "description": "Test Description"
    }, headers=auth_headers)
    item_id = create.json()["id"]
    response = client.delete(f"/items/{item_id}", headers=auth_headers)
    assert response.status_code == 204


def test_delete_item_not_owner(client, auth_headers):
    create = client.post("/items/", json={
        "title": "Test Item",
        "description": "Test Description"
    }, headers=auth_headers)
    item_id = create.json()["id"]

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