from app import models


def get_user(db, user_id):
    return db.query(models.User).get(user_id)
