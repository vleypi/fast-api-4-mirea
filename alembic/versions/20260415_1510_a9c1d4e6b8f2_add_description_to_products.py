"""add description to products

Revision ID: a9c1d4e6b8f2
Revises: 7e2b8f3c1a4d
Create Date: 2026-04-15 15:10:42.987654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a9c1d4e6b8f2"
down_revision: Union[str, None] = "7e2b8f3c1a4d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("products", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("description", sa.String(), server_default="", nullable=False)
        )


def downgrade() -> None:
    with op.batch_alter_table("products", schema=None) as batch_op:
        batch_op.drop_column("description")
