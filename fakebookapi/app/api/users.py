from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from app.models import get_db
from app.models.posts import Post
from app.schemas.users import CreateUserSchema, PatchUserSchema
from app.services import users as userservice
from app.services.auth import get_current_user
from app.services.helper import get_pagination_info
from app.services.users import create_user, delete_user, get_user, update_user


users_route = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={"404": {"description": "Not found."}}
)


@users_route.post("", status_code=status.HTTP_201_CREATED)
async def add_user(user_data: CreateUserSchema, db: Session=Depends(get_db)):
    return create_user(user_data.dict(), db)


# TODO: List response models
@users_route.get("", status_code=status.HTTP_200_OK)
async def get_users(
    db: Session=Depends(get_db),
    include_deleted: bool=False,
    limit: int = 10,
    before_id: int | None = None
):
    if before_id == 1:
        return {
            "data": [],
            "pagination": {"prev": f"/users?limit={limit}&before_id={limit}", "count": None}
        }
    users = userservice.get_users(db, include_deleted, limit, before_id)
    paging_info = {
        "limit": limit,
        "before_id": users[0].id + 1 if users else before_id,
        "last": users[-1].id if users else 0,
        "count": len(users),
    }
    response = {
        # "data": parse_obj_as(List[UserResponseSchema], users),
        "data": users,
        "pagination": get_pagination_info("users", paging_info, before_id, limit)
    }
    return response


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
    return db.query(Post).filter(Post.user_id == user["id"]).all()  # TODO: Extract to service func
