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


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data["users"]) == 2


def test_get_user_by_id(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert json.loads(response.data)["name"] == "Alice"


def test_get_user_not_found(client):
    assert client.get("/users/999").status_code == 404


def test_create_user(client):
    response = client.post(
        "/users",
        data=json.dumps({"name": "Charlie", "email": "charlie@example.com"}),
        content_type="application/json",
    )
    assert response.status_code == 201


def test_update_user(client):
    response = client.put(
        "/users/1",
        data=json.dumps({"name": "Alice Updated"}),
        content_type="application/json",
    )
    assert response.status_code == 200


def test_delete_user(client):
    assert client.delete("/users/1").status_code == 200
    assert client.get("/users/1").status_code == 404
