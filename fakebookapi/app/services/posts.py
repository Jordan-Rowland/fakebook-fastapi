from fastapi import HTTPException
from sqlalchemy import desc

from app.models.posts import Post


def get_posts(db, include_deleted=False, limit=10, before_id=None):
    query = db.query(Post).filter(Post.draft == False)
    if not include_deleted:
        query = query.filter(Post.deleted_at == None)
    if before_id is not None:
        query = query.filter(Post.id < before_id)
    return query.order_by(desc(Post.id)).limit(limit).all()


def get_post_by_id(db, post_id):
    post = (db.query(Post)
            .filter(Post.id == post_id)
            .filter(Post.deleted_at == None)
            .first())
    if not post:
        raise HTTPException(status_code=404, detail=f"Post {post_id} not found.")
    return post


def get_user_post_by_id(db, post_id, user_id):
    post = (
        db.query(Post)
        .filter(Post.id == post_id)
        .filter(Post.user_id == user_id)
        .filter(Post.deleted_at == None)
        .first()
    )
    return post


def create_post(db, post_data, user_id):
    post = Post(**post_data, user_id=user_id)
    db.add(post)
    db.commit()
    return get_user_post_by_id(db, post.id, user_id)


def update_post(db, post_id, post_data, user_id):
    post = get_user_post_by_id(db, post_id, user_id)
    if not post:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Post {post_id} not found. This post may not exist "
                "or you do not have permissions to access it."
            )
        )
    post.update(post_data)
    db.commit()
    return get_user_post_by_id(db, post.id, user_id)


def delete_post(db, post_id, user_id):
    post = get_user_post_by_id(db, post_id, user_id)
    if not post:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Post {post_id} not found. This post may not exist "
                "or you do not have permissions to access it."
            )
        )
    post.delete()
    db.commit()
