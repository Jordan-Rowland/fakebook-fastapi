from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import get_db
from app.models.posts import Post
from app.models.users import User
from app.schemas.users import CreateUserSchema, PatchUserSchema
from app.services.auth import get_current_user
from app.services.users import create_user, delete_user, get_user, update_user


users_route = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={"404": {"description": "Not found."}}
)


@users_route.post("", status_code=status.HTTP_201_CREATED)
async def add_user(user_data: CreateUserSchema, db: Session=Depends(get_db)):
    return create_user(user_data.dict(), db)


@users_route.get("", status_code=status.HTTP_200_OK)
async def get_users(db: Session=Depends(get_db)):
    # Update for pagination and desc order
    return db.query(User).all()


@users_route.patch("/me", status_code=status.HTTP_200_OK)
def handle_update_user(
    user_data: PatchUserSchema, db: Session=Depends(get_db), user: dict=Depends(get_current_user)
):
    return update_user(db, user_data.dict(), user["id"])


@users_route.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def handle_delete_user(db: Session=Depends(get_db), user: dict=Depends(get_current_user)):
    delete_user(db, user["id"])


@users_route.get("/{user_id}", status_code=status.HTTP_200_OK)
def handle_get_user(user_id: int, db: Session=Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    return user


@users_route.get("/me/posts", status_code=status.HTTP_200_OK)
def get_user_posts(user: dict=Depends(get_current_user), db: Session=Depends(get_db)):
    return db.query(Post).filter(Post.user_id == user["id"]).all()
