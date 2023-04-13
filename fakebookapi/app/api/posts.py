from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import get_db
from app.models.posts import Post
from app.schemas.posts import CreatePostSchema
from app.services.users import get_current_user
from app.services.posts import get_post_by_id


posts_route = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={"404": {"description": "Not found."}}
)


@posts_route.get("")
def get_posts(
    ##!! Need to implement for all calls
    #! Probably middleware?
    include_deleted: bool=False,
    user: dict=Depends(get_current_user),
    db: Session=Depends(get_db),
):
    if user is None:
        raise HTTPException(status_code=400, detail=f"User not found.")
    query = db.query(Post).filter(Post.draft == False)
    if not include_deleted:
        query = query.filter(Post.deleted_at == None)
    return query.all()


@posts_route.get("/{post_id}")
def get_post(post_id: int, user: dict=Depends(get_current_user), db: Session=Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=400, detail=f"User not found.")
    return get_post_by_id(db, post_id)


@posts_route.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, user: dict=Depends(get_current_user), db: Session=Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=400, detail=f"User not found.")
    post = (db.query(Post)
            .filter(Post.id == post_id)
            .filter(Post.user_id == user["id"])
            .filter(Post.deleted_at == None)
            .first())
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found.")
    post.deleted_at = datetime.now()
    db.add(post)
    db.commit()


@posts_route.post("")
def create_post(
    post_data: CreatePostSchema,
    user: dict=Depends(get_current_user),
    db: Session=Depends(get_db),
):
    post = Post(**post_data.dict(), user_id=user["id"])
    db.add(post)
    db.commit()
    return get_post_by_id(db, post.id)
