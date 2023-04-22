from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import get_db
from app.models.posts import Post
from app.models.users import User
from app.schemas.users import CreateUserSchema, UserSchema
from app.services.auth import get_current_user
from app.services.users import create_user, get_user


users_route = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={"404": {"description": "Not found."}}
)


@users_route.post("", status_code=status.HTTP_201_CREATED)
async def add_user(user_data: CreateUserSchema, db: Session=Depends(get_db)):
    create_user(user_data.dict(), db)


@users_route.get("", status_code=status.HTTP_200_OK)
async def get_users(db: Session=Depends(get_db)):
    return db.query(User).all()


@users_route.put("/me", status_code=status.HTTP_200_OK)
def handle_update_user(
    user_data: UserSchema,
    db: Session=Depends(get_db),
    user: dict=Depends(get_current_user),
):
    user.username = user_data.username
    db.add(user)
    db.commit()
    return get_user(db, user.id)


@users_route.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def handle_delete_user(
    user_data: UserSchema,
    db: Session=Depends(get_db),
    user: dict=Depends(get_current_user),
):
    user.deleted_at = user_data.deleted_at
    db.add(user)
    db.commit()


@users_route.get("/{user_id}", status_code=status.HTTP_200_OK)
def handle_get_user(user_id: int, db: Session=Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    return user


@users_route.get("/me/posts", status_code=status.HTTP_200_OK)
def get_user_posts(user: dict=Depends(get_current_user), db: Session=Depends(get_db)):
    return db.query(Post).filter(Post.user_id == user["id"]).all()
