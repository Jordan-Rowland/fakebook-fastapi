import json

from app.models.posts import Post
from tests import helper as test_helper
from tests.conftest import USER_ID


def test_create_post(client, session):
    test_helper.create_user(session)
    response = client.post("/posts", data=json.dumps({"content": "This is a test post"}))
    print(response.json())
    assert response.status_code == 200
    assert response.json()["content"] == "This is a test post"
    assert response.json()["user_id"] == USER_ID


def test_create_reply_post(client, session):
    test_helper.create_user(session)
    post = test_helper.create_post(session, {"content": "this is a post for test_create_reply_post"})
    response = client.post(
        "/posts",
        data=json.dumps({
            "content": "This is a reply post",
            "parent_id": post.id,
        })
    )
    assert response.status_code == 200
    assert response.json()["parent_id"] == post.id


def test_get_post(client, session):
    test_helper.create_user(session)
    post = test_helper.create_post(session, {"content": "this is a post for test_get_post"})
    response = client.get(f"/posts/{post.id}")
    assert response.status_code == 200
    assert response.json()["id"] == post.id


def test_get_posts(client, session):
    test_helper.create_user(session)
    test_helper.create_posts(session, 2)
    test_helper.create_post(
        session,
        {"content": "this is a draft post that will not be returned", "draft": True},
    )
    response = client.get("/posts")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2


def test_get_paginated_posts(client, session):
    #! Parameterize for more tests, make sure prev/next work
    test_helper.create_user(session)
    test_helper.create_posts_with_deleted(session, 15)
    response = client.get("/posts?limit=3&after_id=10")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data[0]["id"] == 11
    assert data[1]["id"] == 12
    assert data[2]["id"] == 13
    pagination = response.json()["pagination"]
    assert pagination["prev"] == "/posts?limit=3&after_id=7"
    assert pagination["next"] == '/posts?limit=3&after_id=13'
    assert pagination["count"] == len(data) == 3
    

def test_update_post(client, session):
    test_helper.create_user(session)
    updated_post_content = "updated post!"
    post = test_helper.create_post(session)
    response = client.patch(f"/posts/{post.id}", data=json.dumps({"content": updated_post_content}))
    assert response.status_code == 200
    assert response.json()["content"] == updated_post_content


def test_delete_post(client, session):
    test_helper.create_user(session)
    post = test_helper.create_post(session)
    response = client.delete(f"/posts/{post.id}")
    assert response.status_code == 204
    db_post = session.query(Post).get(post.id)
    assert db_post.deleted_at is not None
