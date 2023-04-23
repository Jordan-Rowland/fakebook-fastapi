from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from app.models import Base
from app.services.helper import UserStatusEnum


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer(), primary_key=True, index=True)
    email = sa.Column(sa.String(64), unique=True, index=True, nullable=False)
    username = sa.Column(sa.String(64), unique=True, nullable=False)
    first_name = sa.Column(sa.String(64), nullable=False)
    last_name = sa.Column(sa.String(64), nullable=False)
    location = sa.Column(sa.String(64))
    password_hash = sa.Column(sa.String(128), nullable=False)
    photo = sa.Column(sa.String(64))
    about_me = sa.Column(sa.Text(), default=None)
    member_since = sa.Column(sa.DateTime(), default=datetime.now)
    last_seen = sa.Column(sa.DateTime(), default=datetime.now)
    status = sa.Column(sa.String(11), nullable=False, default=UserStatusEnum.ACTIVE)

    posts = relationship("Post", back_populates="user", lazy=True)

    def update(self, post_data):
        print(f"{post_data=}")
        for k, v in post_data.items():
            if v:
                setattr(self, k, v)

    def delete(self):
        self.status = UserStatusEnum.DELETED
