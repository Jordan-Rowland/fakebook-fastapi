from datetime import datetime as dt

from app.models.posts import Post
from app.models.users import User
from app.services import users as userservice
from app.services import posts as postservice
from tests.conftest import USER_ID


def create_user(session, user_data=None):
    if user_data is None:
        user_data = {}
    user_data_ = {
        "id": USER_ID,
        "username": "TestUser",
        "email": "testuser@email.com",
        "first_name": "TestUser",
        "last_name": "TestUser",
        "password": "TestUserPass",
    }
    user_data_.update(user_data)
    user = userservice.create_user(user_data_, session)
    return user


def create_post(session, post_data=None, user_id=USER_ID):
    if post_data is None:
        post_data = {}
    post_data_ = {"content": "This is a test post for testing."}
    post_data_.update(post_data)
    post = postservice.create_post(session, post_data_, user_id)
    return post


def create_posts(session, num_posts):
    posts = []
    for i in range(num_posts):
        posts.append(create_post(session, {"content": f"post #{i+1}"}))
    return posts


def create_posts_with_deleted(session, num_posts):
    posts = []
    for i in range(num_posts):
        posts.append(create_post(
            session,
            {
                "content": f"post #{i+1}",
                "deleted_at": dt.now() if i >= 6 else None,
            }
        ))
    return posts
