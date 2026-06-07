"""create obras_publicas dashboard projection offsets table

Revision ID: 20260305_044_obras_publicas_dashboard_projection_offsets
Revises: 20260305_043_obras_publicas_saga_cqrs
Create Date: 2026-03-05 02:10:00.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260305_044_obras_publicas_dashboard_projection_offsets"
down_revision = "20260305_043_obras_publicas_saga_cqrs"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS op_dashboard_projection_offsets (
            event_id UUID PRIMARY KEY,
            consumed_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS op_dashboard_projection_offsets")
