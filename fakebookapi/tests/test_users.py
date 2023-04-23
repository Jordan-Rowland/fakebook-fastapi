import json
import pytest

from app.models.users import User
from app.services.auth import verify_password
from tests import helper as test_helper


def test_create_user(client, session):
    post_data = {
        "username": "TestUser",
        "password": "TestUserPass",
        "email": "testuser@email.com",
        "first_name": "TestUser",
        "last_name": "TestUser",
    }
    response = client.post("/users", data=json.dumps(post_data))
    assert response.status_code == 201
    user = session.query(User).first()
    assert user.username == post_data["username"]
    assert verify_password(post_data["password"], user.password_hash)
    assert user.email == post_data["email"]
    assert user.first_name == post_data["first_name"]
    assert user.last_name == post_data["last_name"]


@pytest.mark.parametrize(
    "before_query, user_ids, prev_response, next_response",
    [
        (4, (3, 2, 1), "/users?limit=3&before_id=7", None),
        (7, (6, 5, 4), "/users?limit=3&before_id=10", "/users?limit=3&before_id=4"),
        (9, (6, 5, 4), None, "/users?limit=3&before_id=4"),
    ]
)
def test_get_paginated_users(
        client, session, before_query, user_ids, prev_response, next_response):
    test_helper.create_users_with_deleted(session, 6)
    response = client.get(f"/users?limit=3&before_id={before_query}")
    # response = client.get(f"/users?limit=3")
    assert response.status_code == 200
    data = response.json()["data"]
    print()
    print(f"{response.json()=}")
    print()
    assert data[0]["id"] == user_ids[0]
    assert data[1]["id"] == user_ids[1]
    assert data[2]["id"] == user_ids[2]
    pagination = response.json()["pagination"]
    assert pagination["prev"] == prev_response
    assert pagination["next"] == next_response
    assert pagination["count"] == len(data) == 3


def test_update_user(client, session):
    user = test_helper.create_user(session)
    patch_data = {
        "email": "updated_email@emails.com",
        "first_name": "Don",
        "last_name": "Johnson",
        "location": "Miami, FL",
        "about_me": "I like long walks on the beach and orange juice",
    }
    response = client.patch("/users/me", data=json.dumps(patch_data))
    assert response.status_code == 200
    user = session.query(User).first()
    assert user.email == patch_data["email"]
    assert user.first_name == patch_data["first_name"]
    assert user.last_name == patch_data["last_name"]
    assert user.location == patch_data["location"]
    assert user.about_me == patch_data["about_me"]


def test_delete_user(client, session):
    user = test_helper.create_user(session)
    client.delete("/users/me")
    assert False, "Unimplemented"


def test_get_user_posts(client, session):
    user = test_helper.create_user(session)
    client.get("/users/me/posts")
    assert False, "Unimplemented"

