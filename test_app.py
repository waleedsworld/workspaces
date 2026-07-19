import json

import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def reset_users():
    # Reset the store to a known state before every test.
    from app import users

    users.clear()
    users.extend(
        [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
        ]
    )


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Welcome to the Workspaces API"
    assert "endpoints" in data


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"
    assert data["user_count"] == 2


def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "users" in data
    assert data["count"] == 2
    assert len(data["users"]) == 2
    assert data["users"][0]["name"] == "Alice"


def test_get_user_by_id(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["id"] == 1
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"


def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data["error"] == "User not found"


def test_create_user(client):
    new_user = {"name": "Charlie", "email": "charlie@example.com"}
    response = client.post(
        "/users", data=json.dumps(new_user), content_type="application/json"
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["name"] == "Charlie"
    assert data["email"] == "charlie@example.com"
    assert "id" in data


def test_create_user_missing_fields(client):
    response = client.post(
        "/users",
        data=json.dumps({"name": "Charlie"}),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert "error" in json.loads(response.data)


def test_create_user_invalid_email(client):
    response = client.post(
        "/users",
        data=json.dumps({"name": "Charlie", "email": "not-an-email"}),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert "error" in json.loads(response.data)


def test_create_user_duplicate_email(client):
    response = client.post(
        "/users",
        data=json.dumps({"name": "Alice II", "email": "alice@example.com"}),
        content_type="application/json",
    )
    assert response.status_code == 409
    assert "error" in json.loads(response.data)


def test_create_user_empty_name(client):
    response = client.post(
        "/users",
        data=json.dumps({"name": "   ", "email": "new@example.com"}),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_update_user(client):
    updated = {"name": "Alice Updated", "email": "alice.updated@example.com"}
    response = client.put(
        "/users/1", data=json.dumps(updated), content_type="application/json"
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["name"] == "Alice Updated"
    assert data["email"] == "alice.updated@example.com"


def test_update_user_partial(client):
    response = client.put(
        "/users/1",
        data=json.dumps({"name": "Alice Modified"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["name"] == "Alice Modified"
    assert data["email"] == "alice@example.com"


def test_update_user_not_found(client):
    response = client.put(
        "/users/999",
        data=json.dumps({"name": "Nobody"}),
        content_type="application/json",
    )
    assert response.status_code == 404


def test_update_user_invalid_email(client):
    response = client.put(
        "/users/1",
        data=json.dumps({"email": "nope"}),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_update_user_duplicate_email(client):
    response = client.put(
        "/users/1",
        data=json.dumps({"email": "bob@example.com"}),
        content_type="application/json",
    )
    assert response.status_code == 409


def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "User deleted successfully"

    # Confirm the user is really gone.
    assert client.get("/users/1").status_code == 404


def test_delete_user_not_found(client):
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert "error" in json.loads(response.data)


def test_method_not_allowed(client):
    response = client.patch("/users/1")
    assert response.status_code == 405
    assert "error" in json.loads(response.data)
