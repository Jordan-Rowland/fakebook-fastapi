import logging

from pydantic import BaseSettings


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = bool(0)


def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
