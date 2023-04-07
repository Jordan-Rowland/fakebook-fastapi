from sqlalchemy.orm import Session

from app import models


def get_post_by_id(db: Session, post_id: int):
    return db.query(models.Post).get(post_id)
