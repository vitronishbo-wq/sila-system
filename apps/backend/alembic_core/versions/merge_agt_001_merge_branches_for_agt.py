"""merge branches for agt

Revision ID: merge_agt_001
Revises: 6g2b3c4d, agt_001
Create Date: 2026-02-19 00:20:08.427496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'merge_agt_001'
down_revision: Union[str, Sequence[str], None] = ('6g2b3c4d', 'agt_001')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
