from app.models.users import User
from app.services.auth import get_password_hash


def create_user(user_data, db):
    user_data_ = user_data
    password = user_data_.pop("password")
    user = User(**user_data_, password_hash=get_password_hash(password))
    db.add(user)
    db.commit()
    return user


def get_user(db, user_id):
    return db.query(User).get(user_id)


def update_user(db, user_data, user_id):
    user = get_user(db, user_id)
    if password := user_data.pop("password", None):
        user_data["password_hash"] = get_password_hash(password)
    user.update(user_data)
    db.commit()
    return get_user(db, user.id)


def delete_user(db, user_id):
    user = get_user(db, user_id)
    user.delete()
    db.commit()
