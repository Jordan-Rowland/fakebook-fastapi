from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import users, posts, follows
from app.models import init_db
from app.config import log


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting up...")
    init_db()
    yield
    log.info("Shutting down...")


def create_app():
    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    app.include_router(users.users_route)
    app.include_router(posts.posts_route)
    app.include_router(follows.follows_route)

    return app


app = create_app()
