"""adds Post.draft field

Revision ID: 22f7e6e8ba77
Revises: 
Create Date: 2023-04-07 15:22:45.854148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22f7e6e8ba77'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("draft", sa.Boolean(), nullable=False, default=False))


def downgrade() -> None:
    op.drop_column("posts", "draft")
