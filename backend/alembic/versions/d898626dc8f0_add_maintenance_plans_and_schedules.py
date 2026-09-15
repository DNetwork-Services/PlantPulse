"""add maintenance plans and schedules

Revision ID: d898626dc8f0
Revises: 2dcbf6eb2db8
Create Date: 2026-09-15 21:45:11.004381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd898626dc8f0'
down_revision: Union[str, None] = '2dcbf6eb2db8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
