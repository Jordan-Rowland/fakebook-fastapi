from fastapi import APIRouter, Depends
from app.config import get_settings, Settings

ping_route = APIRouter()


@ping_route.get("/ping")
def ping(settings: Settings = Depends(get_settings)):
    return {
        "environment": settings.environment,
        "testing": settings.testing
    }
