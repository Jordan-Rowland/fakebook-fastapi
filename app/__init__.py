from fastapi import FastAPI
from app.api import users, posts, follows
from app.models import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.users_route)
app.include_router(posts.posts_route)
app.include_router(follows.follows_route)
