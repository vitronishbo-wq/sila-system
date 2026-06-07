"""merge heads

Revision ID: 4b8e10487f5a
Revises: 181c15049e80, 20260314_053_wallet_notifications_tables
Create Date: 2026-03-16 07:09:45.931253

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "4b8e10487f5a"
down_revision: str | Sequence[str] | None = (
    "181c15049e80",
    "20260314_053_wallet_notifications_tables",
)
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
