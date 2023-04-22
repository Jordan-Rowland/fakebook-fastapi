from typing import Dict, List

from fastapi import APIRouter, Depends, status
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from app.models import get_db
from app.schemas.posts import CreatePostSchema, PostResponseSchema, UpdatePostSchema
from app.services import posts as postservice
from app.services.auth import get_current_user
from app.services.helper import get_pagination_info


posts_route = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={"404": {"description": "Not found."}},
)


@posts_route.post("", response_model=PostResponseSchema)
def create_post(
    post_data: CreatePostSchema,
    db: Session=Depends(get_db),
    user: dict=Depends(get_current_user),
):
    post = postservice.create_post(db, post_data.dict(), user["id"])
    return PostResponseSchema.from_orm(post)


@posts_route.get("", response_model=Dict[str, dict | List[PostResponseSchema]])
def get_posts(
    db: Session=Depends(get_db),
    include_deleted: bool=False,
    limit: int = 10,
    before_id: int | None = None
):
    if before_id == 1:  # TODO: Do something else here.
        return {
            "data": [],
            "pagination": {"prev": f"/posts?limit={limit}&before_id={limit}", "count": None}
        }
    posts = postservice.get_posts(db, include_deleted, limit, before_id)
    paging_info = {
        "limit": limit,
        "before_id": posts[0].id + 1 if posts else before_id,
        "last": posts[-1].id if posts else 0,
        "count": len(posts),
    }
    response = {
        "data": parse_obj_as(List[PostResponseSchema], posts),
        "pagination": get_pagination_info(paging_info, before_id, limit)
    }
    return response


@posts_route.get("/{post_id}", response_model=PostResponseSchema)
def get_post(post_id: int, db: Session=Depends(get_db)):
    return postservice.get_post_by_id(db, post_id)


@posts_route.patch("/{post_id}", response_model=PostResponseSchema)
def update_post(
    post_id: int,
    update_data: UpdatePostSchema,
    db: Session=Depends(get_db),
    user: dict=Depends(get_current_user),
):
    return postservice.update_post(db, post_id, update_data.dict(), user["id"])


@posts_route.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session=Depends(get_db), user: dict=Depends(get_current_user)):
    postservice.delete_post(db, post_id, user["id"])
