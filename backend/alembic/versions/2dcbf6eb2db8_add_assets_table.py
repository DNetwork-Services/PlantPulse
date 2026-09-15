"""add assets table

Revision ID: 2dcbf6eb2db8
Revises: ddb97cb87944
Create Date: 2026-09-15 21:35:05.645674

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dcbf6eb2db8'
down_revision: Union[str, None] = 'ddb97cb87944'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
