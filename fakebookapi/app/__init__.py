from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import follows, ping, posts, users
from app.config import log
from app.models import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting up...")
    init_db()
    yield  # App runs here
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

    app.include_router(follows.follows_route)
    app.include_router(ping.ping_route)
    app.include_router(posts.posts_route)
    app.include_router(users.users_route)

    return app


app = create_app()
