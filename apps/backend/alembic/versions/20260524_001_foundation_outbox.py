"""create foundation_outbox table

Revision ID: 20260524_001_foundation_outbox
Revises: 20260319_1400_merge_identity_and_payment_heads
Create Date: 2026-05-24 00:00:00.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260524_001_foundation_outbox"
down_revision = "20260319_1400_merge_identity_and_payment_heads"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS foundation_outbox (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            topic VARCHAR(255) NOT NULL,
            payload JSONB NOT NULL,
            tenant_id VARCHAR(80),
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            dispatched BOOLEAN NOT NULL DEFAULT false,
            dispatched_at TIMESTAMPTZ,
            locked_by VARCHAR(200),
            locked_at TIMESTAMPTZ,
            attempts INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_foundation_outbox_tenant_id ON foundation_outbox (tenant_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_foundation_outbox_dispatched ON foundation_outbox (dispatched)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_foundation_outbox_locked_by ON foundation_outbox (locked_by)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_foundation_outbox_created_at ON foundation_outbox (created_at)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_foundation_outbox_created_at")
    op.execute("DROP INDEX IF EXISTS ix_foundation_outbox_locked_by")
    op.execute("DROP INDEX IF EXISTS ix_foundation_outbox_dispatched")
    op.execute("DROP INDEX IF EXISTS ix_foundation_outbox_tenant_id")
    op.execute("DROP TABLE IF EXISTS foundation_outbox")
