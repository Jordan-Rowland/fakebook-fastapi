from fastapi import FastAPI
from app.api import users, posts

app = FastAPI()

app.include_router(users.users_route)
app.include_router(posts.posts_route)
