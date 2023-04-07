from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.posts import Post


def get_post_by_id(db: Session, post_id: int):
    post = (db.query(Post)
            .filter(Post.id == post_id)
            .filter(Post.deleted_at == None)
            .first())
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found.")
    return post
