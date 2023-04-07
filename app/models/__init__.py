from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    create_engine,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# sqlite
# SQLALCHEMY_DATABASE_URL = "sqlite:///./app/main.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# mysql
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:rootpassword@localhost:3306/fakebook"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close


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
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    location = Column(String(64))
    password_hash = Column(String(128), nullable=False)
    photo = Column(String())
    about_me = Column(Text(), default=None)
    member_since = Column(DateTime(), default=datetime.utcnow)
    last_seen = Column(DateTime(), default=datetime.utcnow)
    # active = Column(Boolean(), default=True)
    # private = Column(Boolean(), default=False)

    posts = relationship("Post", back_populates="user", lazy=True)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer(), primary_key=True, index=True)
    content = Column(Text(), index=True, nullable=False)
    user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
    parent_id = Column(Integer(), nullable=True)
    created_at = Column(DateTime(), nullable=False, default=datetime.utcnow)
    deleted_at = Column(DateTime(), default=None)

    user = relationship("User", back_populates="posts", lazy=True)
