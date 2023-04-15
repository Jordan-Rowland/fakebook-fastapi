from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.posts import Post


def get_posts(db, include_deleted=False, page=1, limit=10):
    query = db.query(Post).filter(Post.draft == False)
    if not include_deleted:
        query = query.filter(Post.deleted_at == None)
    last = page * limit
    first = last - limit
    return query.filter(Post.id > first).filter(Post.id <= last).all()


def get_post_by_id(db: Session, post_id: int):
    post = (db.query(Post)
            .filter(Post.id == post_id)
            .filter(Post.deleted_at == None)
            .first())
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found.")
    return post


def create_post(db: Session, post_data, user):
    post = Post(**post_data.dict(), user_id=user["id"])
    db.add(post)
    db.commit()
    return get_post_by_id(db, post.id)


def update_post(db, post_id, post_data, user):
    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .filter(Post.user_id == user["id"])
        .filter(Post.deleted_at == None)
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found.")
    post.update(post_data.dict())
    db.commit()
    return get_post_by_id(db, post.id)


def delete_post(db, post_id, user):
    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .filter(Post.user_id == user["id"])
        .filter(Post.deleted_at == None)
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found.")
    post.delete()
    db.commit()
