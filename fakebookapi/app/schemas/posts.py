from datetime import datetime

from typing import Optional
from pydantic import BaseModel, validator


class CreatePostSchema(BaseModel):
    content: str
    parent_id: Optional[int]
    draft: Optional[bool] = False
    created_at: datetime = datetime.now()


class UpdatePostSchema(BaseModel):
    content: str


class PostResponseSchema(BaseModel):
    id: int
    content: str
    user_id: int
    parent_id: int | None
    draft: bool
    created_at: datetime

    class Config:
        orm_mode = True

    @validator("created_at", pre=True)
    def convert_datetime(cls, value):
        return datetime.strftime(value, "%Y-%m-%d %H:%M:%S")
