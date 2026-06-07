"""create energia outbox events table

Revision ID: 20260304_041_energia_outbox_events
Revises: 20260304_040_aguas_saneamento_outbox_events
Create Date: 2026-03-04 23:55:00.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260304_041_energia_outbox_events"
down_revision = "20260304_040_aguas_saneamento_outbox_events"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS energia_outbox_events (
            id UUID PRIMARY KEY,
            event_name VARCHAR(120) NOT NULL,
            event_version INTEGER NOT NULL DEFAULT 1,
            schema_version INTEGER NOT NULL DEFAULT 1,
            topic VARCHAR(160) NOT NULL,
            payload JSONB NOT NULL,
            headers JSONB NOT NULL DEFAULT '{}'::jsonb,
            processed BOOLEAN NOT NULL DEFAULT FALSE,
            retries INTEGER NOT NULL DEFAULT 0,
            last_error TEXT,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            processed_at TIMESTAMPTZ
        )
        """
    )

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_energia_outbox_event_name ON energia_outbox_events (event_name)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_energia_outbox_topic ON energia_outbox_events (topic)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_energia_outbox_processed ON energia_outbox_events (processed)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_energia_outbox_created_at ON energia_outbox_events (created_at)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_energia_outbox_created_at")
    op.execute("DROP INDEX IF EXISTS ix_energia_outbox_processed")
    op.execute("DROP INDEX IF EXISTS ix_energia_outbox_topic")
    op.execute("DROP INDEX IF EXISTS ix_energia_outbox_event_name")
    op.execute("DROP TABLE IF EXISTS energia_outbox_events")
