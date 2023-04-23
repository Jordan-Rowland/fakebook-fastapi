from typing import Optional
from pydantic import BaseModel


class CreateUserSchema(BaseModel):
    username: str
    email: str
    password: str
    first_name: Optional[str]
    last_name: Optional[str]
    location: Optional[str]
    about_me: Optional[str]


class PatchUserSchema(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    location: Optional[str]
    about_me: Optional[str]
