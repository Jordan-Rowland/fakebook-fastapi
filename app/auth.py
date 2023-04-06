from typing import Optional
from datetime import datetime, timedelta
import os

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    status
)
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import models
from app.database import SessionLocal, engine


SECRET_KEY = os.getenv("SECRET_KEY") or "mysecretkey"
ALGORITHM = "HS256"

class CreateUser(BaseModel):
    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

oath2_bearer = OAuth2PasswordBearer(tokenUrl="token")


app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, password_hash):
    return bcrypt_context.verify(plain_password, password_hash)


def authenticate_user(username: str, password: str, db):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta]=None):
    encode = {"sub": username, "id": user_id}
    encode["exp"] = datetime.utcnow() + timedelta(minutes=15)
    if expires_delta:
        encode["exp"] = datetime.utcnow() + expires_delta
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str=Depends(oath2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=404, details="User not found.")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=404, details="User not found.")


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def add_user(user_data: CreateUser, db: Session=Depends(get_db)):
    user_data_ = user_data.dict()
    password = user_data_.pop("password")
    user = models.User(**user_data_, password_hash=get_password_hash(password))
    db.add(user)
    db.commit()


@app.post("/token", status_code=status.HTTP_200_OK)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token_expires = timedelta(minutes=90)
    token = create_access_token(user.username, user.id, expires_delta=token_expires)
    return {"token": token}
