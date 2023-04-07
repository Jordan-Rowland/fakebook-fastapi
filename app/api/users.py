import sys
sys.path.append("..")

from typing import Optional
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models
from app.services.users import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    get_user
)


class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


users_route = APIRouter()


class UserSchema(BaseModel):  ##! Move this
    username: str
    # username: str = Field(gt=0, lt=32)


@users_route.post("/users", status_code=status.HTTP_201_CREATED)
async def add_user(user_data: CreateUser, db: Session=Depends(models.get_db)):
    user_data_ = user_data.dict()
    password = user_data_.pop("password")
    user = models.User(**user_data_, password_hash=get_password_hash(password))
    db.add(user)
    db.commit()


@users_route.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(models.get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token_expires = timedelta(minutes=60 * 24 * 3)  # 3 days valid token
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    return {"token": token}


@users_route.put("/users/{user_id}", status_code=status.HTTP_200_OK)
def handle_update_user(user_id, user_data: UserSchema, db: Session=Depends(models.get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    user.username = user_data.username
    db.add(user)
    db.commit()
    return get_user(db, user.id)


@users_route.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def handle_update_user(user_id, user_data: UserSchema, db: Session=Depends(models.get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    user.deleted_at = user_data.deleted_at
    db.add(user)
    db.commit()


@users_route.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def handle_get_user(user_id: int, db: Session=Depends(models.get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    return user


@users_route.get("/posts/users", status_code=status.HTTP_200_OK)
def get_user_posts(user: dict=Depends(get_current_user), db: Session=Depends(models.get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail=f"User not found.")

    return db.query(models.Post).filter(models.Post.user_id == user["id"]).all()
