from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
)
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Follow(Base):
    __tablename__ = "follows"

    id = Column(Integer(), primary_key=True, index=True)
    follower_id = Column(Integer(), ForeignKey("users.id"), primary_key=True)
    followed_id = Column(Integer(), ForeignKey("users.id"), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True, index=True)
    email = Column(String(64), unique=True, index=True, nullable=False)
    username = Column(String(64), unique=True, nullable=False)
    location = Column(String(64), default="No Location")
    password_hash = Column(String(128), nullable=False)
    photo = Column(String(), default="nouser.png")
    posts = relationship("Post", back_populates="user", lazy=True)
    about_me = Column(Text(), default=None)
    member_since = Column(DateTime(), default=datetime.utcnow)
    last_seen = Column(DateTime(), default=datetime.utcnow)
    comments = relationship("Comment", back_populates="user", lazy="dynamic")
    followed = relationship(
        "Follow",
        foreign_keys=[Follow.follower_id],
        back_populates="follower",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )
    followers = relationship(
        "Follow",
        foreign_keys=[Follow.followed_id],
        back_populates="followed",
        lazy="dynamic",
        cascade="all, delete-orphan"
    )


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer(), primary_key=True, index=True)
    content = Column(Text(), index=True, nullable=False)
    user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    comments = relationship("Comment", back_populates="post", lazy="dynamic")
    deleted_at = Column(Boolean(), default=False)


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer(), primary_key=True, index=True)
    content = Column(Text())
    created_at = Column(DateTime, index=True, nullable=False, default=datetime.now)
    disabled = Column(Boolean())
    user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer(), ForeignKey("posts.id"), nullable=False)
