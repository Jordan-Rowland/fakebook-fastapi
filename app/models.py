# from sqlalchemy import (
#     Boolean,
#     Column,
#     ForeignKey,
#     Integer,
#     String,
#     Text,
#     DateTime,
# )
# from sqlalchemy.orm import relationship
# from datetime import datetime

# from app.database import Base


# class Follow(Base):
#     __tablename__ = "follows"

#     id = Column(Integer(), primary_key=True, index=True)
#     follower_id = Column(Integer(), ForeignKey("users.id"), primary_key=True)
#     followed_id = Column(Integer(), ForeignKey("users.id"), primary_key=True)
#     created_at = Column(DateTime, default=datetime.utcnow)


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer(), primary_key=True, index=True)
#     email = Column(String(64), unique=True, index=True, nullable=False)
#     username = Column(String(64), unique=True, nullable=False)
#     first_name = Column(String(64), nullable=False)
#     last_name = Column(String(64), nullable=False)
#     location = Column(String(64))
#     password_hash = Column(String(128), nullable=False)
#     photo = Column(String())
#     about_me = Column(Text(), default=None)
#     member_since = Column(DateTime(), default=datetime.utcnow)
#     last_seen = Column(DateTime(), default=datetime.utcnow)
#     # active = Column(Boolean(), default=True)
#     # private = Column(Boolean(), default=False)

#     posts = relationship("Post", back_populates="user", lazy=True)


# class Post(Base):
#     __tablename__ = "posts"

#     id = Column(Integer(), primary_key=True, index=True)
#     content = Column(Text(), index=True, nullable=False)
#     user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
#     parent_id = Column(Integer(), nullable=True)
#     created_at = Column(DateTime(), nullable=False, default=datetime.utcnow)
#     deleted_at = Column(DateTime(), default=None)

#     user = relationship("User", back_populates="posts", lazy=True)
