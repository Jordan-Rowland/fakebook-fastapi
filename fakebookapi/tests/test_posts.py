import json

from app.models.posts import Post
import pytest
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


##!! Might want to block this
# def test_cannot_create_reply_post_to_another_reply_post(client, session):


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


@pytest.mark.parametrize(
    "after_query, post_ids, prev_response, next_response",
    [
        (4, (3, 2, 1), "/posts?limit=3&before_id=7", None),
        (7, (6, 5, 4), "/posts?limit=3&before_id=10", "/posts?limit=3&before_id=4"),
        (9, (6, 5, 4), None, "/posts?limit=3&before_id=4"),
    ]
)
def test_get_paginated_posts(
        client, session, after_query, post_ids, prev_response, next_response):
    test_helper.create_user(session)
    test_helper.create_posts_with_deleted(session, 15)
    response = client.get(f"/posts?limit=3&before_id={after_query}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data[0]["id"] == post_ids[0]
    assert data[1]["id"] == post_ids[1]
    assert data[2]["id"] == post_ids[2]
    pagination = response.json()["pagination"]
    assert pagination["prev"] == prev_response
    assert pagination["next"] == next_response
    assert pagination["count"] == len(data) == 3
    

def test_update_post(client, session):
    test_helper.create_user(session)
    updated_post_content = "updated post!"
    post = test_helper.create_post(session)
    response = client.patch(f"/posts/{post.id}", data=json.dumps({"content": updated_post_content}))
    assert response.status_code == 200
    assert response.json()["content"] == updated_post_content


def test_cannot_update_other_users_post(client, session):
    other_user = test_helper.create_user(session, {"id": 255})
    print(other_user.id)
    updated_post_content = "updated post!"
    post = test_helper.create_post(session, {"user_id": other_user.id})
    response = client.patch(f"/posts/{post.id}", data=json.dumps({"content": updated_post_content}))
    assert response.status_code == 404
    assert response.json()["detail"] == (
        f"Post {post.id} not found. This post may not exist "
        "or you do not have permissions to access it."
    )


def test_delete_post(client, session):
    test_helper.create_user(session)
    post = test_helper.create_post(session)
    response = client.delete(f"/posts/{post.id}")
    assert response.status_code == 204
    db_post = session.query(Post).get(post.id)
    assert db_post.deleted_at is not None


def test_cannot_delete_other_users_post(client, session):
    other_user = test_helper.create_user(session, {"id": 255})
    post = test_helper.create_post(session, {"user_id": other_user.id})
    response = client.delete(f"/posts/{post.id}")
    print(response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == (
        f"Post {post.id} not found. This post may not exist "
        "or you do not have permissions to access it."
    )
