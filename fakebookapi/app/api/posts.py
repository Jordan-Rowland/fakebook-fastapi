from typing import Dict, List

from fastapi import APIRouter, Depends, status
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from app.models import get_db
from app.schemas.posts import CreatePostSchema, PostResponseSchema, UpdatePostSchema
from app.services.users import get_current_user
from app.services import posts as postservice


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
    post = postservice.create_post(db, post_data, user)
    return PostResponseSchema.from_orm(post)


@posts_route.get("", response_model=Dict[str, dict | List[PostResponseSchema]])
def get_posts(
    db: Session=Depends(get_db),
    include_deleted: bool=False,
    # page: int = 1,
    limit: int = 10,
    after_id:int = 0
):
    posts = postservice.get_posts(db, include_deleted, limit, after_id)
    paging_info = {
        "limit": limit,
        "after_id": posts[0].id - 1,
        # "before_id": posts[0].id - 1,
        "last": posts[-1].id,
        "count": len(posts),
        }
    response = {
        "data": parse_obj_as(List[PostResponseSchema], posts),
        # "pagination": get_pagination_info(paging_info)
        "pagination": {  #  make a schema for this and extract to function for reuse
            **paging_info,
            "prev": (
                f"/posts?limit={limit}&after_id={paging_info['after_id'] - paging_info['count']}"
                if paging_info["after_id"] <= after_id
                else None
            ),
            "next": (
                f"/posts?limit={limit}&after_id={paging_info['last']}"
                if paging_info["count"] == limit
                else None
            ),
            # Figure out how to find the end so next == None

        }
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
    return postservice.update_post(db, post_id, update_data, user)


@posts_route.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session=Depends(get_db), user: dict=Depends(get_current_user)):
    postservice.delete_post(db, post_id, user)
