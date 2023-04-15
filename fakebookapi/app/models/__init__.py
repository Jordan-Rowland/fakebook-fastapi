import os

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# sqlite
# SQLALCHEMY_DATABASE_URL = "sqlite:///./app/test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# mysql
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:rootpassword@localhost:3306/fakebook"
# Change `localhost` to `host.docker.internal` for Docker
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:rootpassword@host.docker.internal:3306/fakebook"
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")
engine = sa.create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db(engine):
    Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close
