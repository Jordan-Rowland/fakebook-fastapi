from typing import Optional
from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str


class UserSchema(BaseModel):
    username: str
    # username: str = Field(gt=0, lt=32)