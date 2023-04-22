import json

from app.models.users import User


def test_create_user(client, session):
    client.post(
        "/users",
        data=json.dumps({
            "username": "TestUser",
            "password": "TestUserPass",
            "email": "testuser@email.com",
            "first_name": "TestUser",
            "last_name": "TestUser",
        }),
    )
    user = session.query(User).first()
    assert user.username == "TestUser"
    assert user.email == "testuser@email.com"
    assert user.first_name == "TestUser"
    assert user.last_name == "TestUser"
    # assert user.password == "TestUserPass"
