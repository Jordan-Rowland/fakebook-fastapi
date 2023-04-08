from datetime import datetime
import sqlalchemy as sa
from app.models import Base


class Follow(Base):
    __tablename__ = "follows"

    id = sa.Column(sa.Integer(), primary_key=True, index=True)
    follower_id = sa.Column(sa.Integer(), sa.ForeignKey("users.id"), primary_key=True)
    followed_id = sa.Column(sa.Integer(), sa.ForeignKey("users.id"), primary_key=True)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow)
