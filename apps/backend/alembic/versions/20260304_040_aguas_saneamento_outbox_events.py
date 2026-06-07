"""create aguas_saneamento outbox events table

Revision ID: 20260304_040_aguas_saneamento_outbox_events
Revises: 20260304_039_transportes_logistica_linhas_bilhetagem
Create Date: 2026-03-04 23:20:00.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260304_040_aguas_saneamento_outbox_events"
down_revision = "20260304_039_transportes_logistica_linhas_bilhetagem"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS aguas_saneamento_outbox_events (
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
        "CREATE INDEX IF NOT EXISTS ix_as_outbox_event_name ON aguas_saneamento_outbox_events (event_name)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_as_outbox_topic ON aguas_saneamento_outbox_events (topic)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_as_outbox_processed ON aguas_saneamento_outbox_events (processed)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_as_outbox_created_at ON aguas_saneamento_outbox_events (created_at)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_as_outbox_created_at")
    op.execute("DROP INDEX IF EXISTS ix_as_outbox_processed")
    op.execute("DROP INDEX IF EXISTS ix_as_outbox_topic")
    op.execute("DROP INDEX IF EXISTS ix_as_outbox_event_name")
    op.execute("DROP TABLE IF EXISTS aguas_saneamento_outbox_events")
