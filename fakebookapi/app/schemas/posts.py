from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

from app.services.helper import PostStatusEnum


class CreatePostSchema(BaseModel):
    content: str
    parent_id: Optional[int]
    status: str = PostStatusEnum.PUBLISHED
    created_at: datetime = datetime.now()


class UpdatePostSchema(BaseModel):
    content: str


class PostResponseSchema(BaseModel):
    id: int
    content: str
    user_id: int
    parent_id: int | None
    status: str
    created_at: datetime
    deleted_at: datetime | None

    class Config:
        orm_mode = True

    @validator("created_at", pre=True)
    def convert_datetime(cls, value):
        return datetime.strftime(value, "%Y-%m-%d %H:%M:%S")
