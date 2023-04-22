import json

from app.services.auth import get_current_user
from tests import helper as test_helper


def test_create_access_token_and_get_user(client, session):
    test_helper.create_user(session)
    response = client.post(
        "/auth/token",
        data={"username": "TestUser", "password": "TestUserPass"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    user = get_current_user(response.json()["token"])
    assert user["id"] == 108
    assert user["username"] == "TestUser"
