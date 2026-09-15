"""add work orders and downtime records

Revision ID: 5069d2b16976
Revises: d898626dc8f0
Create Date: 2026-09-15 22:01:38.149054

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5069d2b16976'
down_revision: Union[str, None] = 'd898626dc8f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
