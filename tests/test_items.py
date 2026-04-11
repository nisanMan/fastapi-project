# tests/test_items.py
from .factories import create_user, create_item


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
    create_item(client, auth_headers)
    response = client.get("/items/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_all_items(client, auth_headers):
    for i in range(3):
        create_item(client, auth_headers, title=f"Item {i}")
    response = client.get("/items/all?page=1&limit=10", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert data["page"] == 1
    assert len(data["data"]) == 3


def test_update_item(client, auth_headers):
    item = create_item(client, auth_headers, title="Old Title", description="Old Desc")
    response = client.put(f"/items/{item['id']}", json={
        "title": "New Title",
        "description": "New Desc"
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"


def test_update_item_not_owner(client, auth_headers):
    item = create_item(client, auth_headers)
    other = create_user(client, email="other@example.com")
    response = client.put(f"/items/{item['id']}", json={
        "title": "Hacked",
        "description": "Hacked"
    }, headers=other["headers"])
    assert response.status_code == 403


def test_delete_item(client, auth_headers):
    item = create_item(client, auth_headers)
    response = client.delete(f"/items/{item['id']}", headers=auth_headers)
    assert response.status_code == 204


def test_delete_item_not_owner(client, auth_headers):
    item = create_item(client, auth_headers)
    other = create_user(client, email="other@example.com")
    response = client.delete(f"/items/{item['id']}", headers=other["headers"])
    assert response.status_code == 403

def test_update_nonexistent_item(client, auth_headers):
    response = client.put("/items/9999", json={
        "title": "X", "description": "X"
    }, headers=auth_headers)
    assert response.status_code == 404


def test_delete_nonexistent_item(client, auth_headers):
    response = client.delete("/items/9999", headers=auth_headers)
    assert response.status_code == 404

