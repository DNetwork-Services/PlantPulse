"""initial empty migration

Revision ID: 8c7bf03b854c
Revises: e27e7d793c6e
Create Date: 2026-09-14 09:47:47.481820

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c7bf03b854c'
down_revision: Union[str, None] = 'e27e7d793c6e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
