"""Empty migration - skip problematic operations

Revision ID: 0fe8c8a824ed
Revises: 20250105_governance
Create Date: 2025-12-14 05:20:25.589225

This migration has been simplified to an empty migration because it was
trying to drop tables that don't exist in the database state. The tables
referenced for deletion do not exist after the previous migrations.
"""
from __future__ import annotations

# revision identifiers, used by Alembic.
revision = '0fe8c8a824ed'
down_revision = '20250105_governance'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema and/or data, creating a new revision."""
    # This migration is intentionally empty
    # The tables referenced for deletion don't exist in the current database state
    pass


def downgrade() -> None:
    """Downgrade database schema and/or data back to the previous revision."""
    # This downgrade is intentionally empty
    pass
