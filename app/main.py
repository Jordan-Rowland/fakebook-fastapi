from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.config import get_settings, Settings
from app.database import engine, SessionLocal
from app import models
from app.auth import get_current_user


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close


class UserSchema(BaseModel):
    username: str
    # username: str = Field(gt=0, lt=32)


def get_user(db, user_id):
    return db.query(models.User).get(user_id)


@app.get("/ping")
def pong(settings: Settings = Depends(get_settings)):
    return {
        "ping": "pong!",
        "environment": settings.environment,
        "testing": settings.testing
    }


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def handle_get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    return user


@app.get("/posts/users", status_code=status.HTTP_200_OK)
def get_user_posts(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail=f"User not found.")

    return db.query(models.Post).filter(models.Post.user_id == user["id"]).all()


@app.post("/users", status_code=status.HTTP_201_CREATED)
def handle_create_user(user_data: UserSchema, db: Session = Depends(get_db)):
    user = models.User(**user_data.dict())
    db.add(user)
    db.commit()
    return get_user(db, user.id)


@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
def handle_update_user(user_id, user_data: UserSchema, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    user.username = user_data.username
    db.add(user)
    db.commit()
    return get_user(db, user.id)


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def handle_update_user(user_id, user_data: UserSchema, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    user.deleted_at = user_data.deleted_at
    db.add(user)
    db.commit()
