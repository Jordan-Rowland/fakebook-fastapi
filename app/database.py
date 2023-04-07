# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base


# # sqlite
# # SQLALCHEMY_DATABASE_URL = "sqlite:///./app/main.db"
# # engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:rootpassword@localhost:3306/fakebook"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
