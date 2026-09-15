"""initial empty migration

Revision ID: ddb97cb87944
Revises: 8c7bf03b854c
Create Date: 2026-09-14 10:07:30.363234

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddb97cb87944'
down_revision: Union[str, None] = '8c7bf03b854c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
