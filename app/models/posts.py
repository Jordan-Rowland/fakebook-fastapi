from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.models import Base


class Post(Base):
    __tablename__ = "posts"

    id = sa.Column(sa.Integer(), primary_key=True, index=True)
    content = sa.Column(sa.Text(), nullable=False)
    user_id = sa.Column(sa.Integer(), sa.ForeignKey("users.id"), nullable=False)
    parent_id = sa.Column(sa.Integer(), nullable=True)
    draft = sa.Column(sa.Boolean(), default=False)
    created_at = sa.Column(sa.DateTime(), nullable=False, default=datetime.utcnow)
    deleted_at = sa.Column(sa.DateTime(), default=None)

    user = relationship("User", back_populates="posts", lazy=True)
