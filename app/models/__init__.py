import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# sqlite
# SQLALCHEMY_DATABASE_URL = "sqlite:///./app/main.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# mysql
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:rootpassword@localhost:3306/fakebook"
engine = sa.create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close


# class Follow(Base):
#     __tablename__ = "follows"

#     id = sa.Column(sa.Integer(), primary_key=True, index=True)
#     follower_id = sa.Column(sa.Integer(), sa.ForeignKey("users.id"), primary_key=True)
#     followed_id = sa.Column(sa.Integer(), sa.ForeignKey("users.id"), primary_key=True)
#     created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
