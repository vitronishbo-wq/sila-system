"""create obras_publicas outbox tables

Revision ID: 20260304_042_obras_publicas_outbox_events
Revises: 20260304_041_energia_outbox_events
Create Date: 2026-03-04 23:59:00.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260304_042_obras_publicas_outbox_events"
down_revision = "20260304_041_energia_outbox_events"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS op_outbox_events (
            id UUID PRIMARY KEY,
            tenant_id VARCHAR(80) NOT NULL,
            aggregate_type VARCHAR(120) NOT NULL,
            aggregate_id VARCHAR(120) NOT NULL,
            event_type VARCHAR(160) NOT NULL,
            payload JSONB NOT NULL,
            idempotency_key VARCHAR(160) NOT NULL UNIQUE,
            correlation_id VARCHAR(160) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            processed_at TIMESTAMPTZ,
            failed_attempts INTEGER NOT NULL DEFAULT 0
        )
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS op_outbox_event_consumption (
            id UUID PRIMARY KEY,
            event_id UUID NOT NULL,
            consumer_name VARCHAR(200) NOT NULL,
            processed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT uq_op_outbox_event_consumption UNIQUE (event_id, consumer_name)
        )
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_op_outbox_events_tenant_id ON op_outbox_events (tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_outbox_events_event_type ON op_outbox_events (event_type)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_outbox_events_correlation_id ON op_outbox_events (correlation_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_outbox_events_created_at ON op_outbox_events (created_at)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_outbox_events_processed_at ON op_outbox_events (processed_at)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_outbox_events_failed_attempts ON op_outbox_events (failed_attempts)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_outbox_consumption_event_id ON op_outbox_event_consumption (event_id)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_op_outbox_consumption_event_id")
    op.execute("DROP INDEX IF EXISTS ix_op_outbox_events_failed_attempts")
    op.execute("DROP INDEX IF EXISTS ix_op_outbox_events_processed_at")
    op.execute("DROP INDEX IF EXISTS ix_op_outbox_events_created_at")
    op.execute("DROP INDEX IF EXISTS ix_op_outbox_events_correlation_id")
    op.execute("DROP INDEX IF EXISTS ix_op_outbox_events_event_type")
    op.execute("DROP INDEX IF EXISTS ix_op_outbox_events_tenant_id")
    op.execute("DROP TABLE IF EXISTS op_outbox_event_consumption")
    op.execute("DROP TABLE IF EXISTS op_outbox_events")

