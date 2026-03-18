"""merge heads

Revision ID: 4b8e10487f5a
Revises: 181c15049e80, 20260314_053_wallet_notifications_tables
Create Date: 2026-03-16 07:09:45.931253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b8e10487f5a'
down_revision: Union[str, Sequence[str], None] = ('181c15049e80', '20260314_053_wallet_notifications_tables')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
