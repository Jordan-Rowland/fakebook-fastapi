from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.models import Base
from app.models.posts import Post


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
    member_since = sa.Column(sa.DateTime(), default=datetime.utcnow)
    last_seen = sa.Column(sa.DateTime(), default=datetime.utcnow)
    active = sa.Column(sa.Boolean(), default=True)
    private = sa.Column(sa.Boolean(), default=False)

    posts = relationship("Post", back_populates="user", lazy=True)
