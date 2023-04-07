from typing import Optional
from pydantic import BaseModel


class CreatePostSchema(BaseModel):
    content: str
    parent_id: Optional[str]
    draft: Optional[bool] = False
