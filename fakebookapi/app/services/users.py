from app import models
from app.services.auth import get_password_hash
from app.models.users import User


def create_user(user_data, db):
    user_data_ = user_data
    password = user_data_.pop("password")
    user = User(**user_data_, password_hash=get_password_hash(password))
    db.add(user)
    db.commit()
    return user


def get_user(db, user_id):
    return db.query(models.User).get(user_id)
