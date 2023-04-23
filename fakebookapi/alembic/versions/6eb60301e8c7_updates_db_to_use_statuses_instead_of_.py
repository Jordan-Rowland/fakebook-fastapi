"""updates db to use statuses instead of bool fields

Revision ID: 6eb60301e8c7
Revises: 22f7e6e8ba77
Create Date: 2023-04-23 14:05:47.261874

"""
from alembic import op
import sqlalchemy as sa

from app.services.helper import PostStatusEnum, UserStatusEnum



# revision identifiers, used by Alembic.
revision = '6eb60301e8c7'
down_revision = '22f7e6e8ba77'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_column("posts", "draft")
    op.add_column(
        "posts", sa.Column(
            "status", sa.String(12), nullable=False, default=PostStatusEnum.PUBLISHED
        )
    )
    
    op.drop_column("users", "active")
    op.drop_column("users", "private")
    op.add_column(
        "users", sa.Column(
            "status", sa.String(12), nullable=False, default=UserStatusEnum.ACTIVE
        )
    )


def downgrade() -> None:
    op.drop_column("posts", "status")
    op.add_column("posts", sa.Column("draft", sa.Boolean(), nullable=False, default=False))

    op.drop_column("users", "status")
    op.add_column("users", sa.Column("active", sa.Boolean(), nullable=False, default=True))
    op.add_column("users", sa.Column("private", sa.Boolean(), nullable=False, default=False))
