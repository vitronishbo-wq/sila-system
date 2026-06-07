"""merge_export_and_audit_heads

Revision ID: 22ab6d804070
Revises: 20260316_054_create_audit_logs, 9a1d2b7c3e10
Create Date: 2026-03-16 16:18:57.627637

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "22ab6d804070"
down_revision: str | Sequence[str] | None = ("20260316_054_create_audit_logs", "9a1d2b7c3e10")
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
