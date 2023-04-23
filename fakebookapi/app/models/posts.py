from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.models import Base
from app.services.helper import PostStatusEnum


class Post(Base):
    __tablename__ = "posts"

    id = sa.Column(sa.Integer(), primary_key=True, index=True)
    content = sa.Column(sa.Text(), nullable=False)
    user_id = sa.Column(sa.Integer(), sa.ForeignKey("users.id"), nullable=False)
    parent_id = sa.Column(sa.Integer(), nullable=True)
    status = sa.Column(sa.String(11), nullable=False, default=PostStatusEnum.PUBLISHED)
    created_at = sa.Column(sa.DateTime(), nullable=False, default=datetime.now)
    deleted_at = sa.Column(sa.DateTime(), default=None)

    user = relationship("User", back_populates="posts", lazy=True)

    def update(self, post_data):
        self.content = post_data["content"]

    def delete(self):
        self.deleted_at = datetime.now()
