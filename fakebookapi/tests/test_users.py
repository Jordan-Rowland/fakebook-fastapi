import json

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
    client.post("/users", data=json.dumps(post_data))
    # TODO: Assert 200 status code and codes for all tests
    user = session.query(User).first()
    assert user.username == post_data["username"]
    assert verify_password(post_data["password"], user.password_hash)
    assert user.email == post_data["email"]
    assert user.first_name == post_data["first_name"]
    assert user.last_name == post_data["last_name"]


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

