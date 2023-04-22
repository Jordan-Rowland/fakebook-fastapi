from datetime import datetime, timedelta
import os
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.models.users import User


SECRET_KEY = os.getenv("SECRET_KEY") or "mysecretkey"  #TODO: Update this
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oath2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, password_hash):
    return bcrypt_context.verify(plain_password, password_hash)


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta]=None):
    encode = {
        "sub": username,
        "id": user_id,
        # "admin": 
    }
    encode["exp"] = datetime.utcnow() + timedelta(minutes=15)
    if expires_delta:
        encode["exp"] = datetime.utcnow() + expires_delta
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str=Depends(oath2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        # admin: bool = payload.get("admin")
        if username is None or user_id is None:
            raise HTTPException(status_code=404, detail="User not found.")
        return {
            "username": username,
            "id": user_id,
            # "admin": admin
        }
    except JWTError:
        raise HTTPException(status_code=404, detail="User not found.")
