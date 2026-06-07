"""create obras_publicas event sourcing and governance tables

Revision ID: 20260305_045_obras_publicas_event_sourcing_governance
Revises: 20260305_044_obras_publicas_dashboard_projection_offsets
Create Date: 2026-03-05 03:05:00.000000
"""

from __future__ import annotations

from alembic import op

revision = "20260305_045_obras_publicas_event_sourcing_governance"
down_revision = "20260305_044_obras_publicas_dashboard_projection_offsets"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS op_event_store (
            id UUID PRIMARY KEY,
            aggregate_id VARCHAR(120) NOT NULL,
            aggregate_type VARCHAR(120) NOT NULL,
            event_type VARCHAR(160) NOT NULL,
            event_data JSONB NOT NULL,
            version INTEGER NOT NULL,
            tenant_id VARCHAR(80) NOT NULL,
            region_code VARCHAR(16) NOT NULL,
            correlation_id VARCHAR(160) NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            CONSTRAINT uq_op_event_store_aggregate_version UNIQUE (aggregate_id, version)
        )
        """
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_event_store_aggregate_id ON op_event_store (aggregate_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_event_store_event_type ON op_event_store (event_type)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_event_store_tenant_id ON op_event_store (tenant_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_event_store_region_code ON op_event_store (region_code)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_op_event_store_created_at ON op_event_store (created_at)"
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS event_catalog (
            event_name VARCHAR(160) PRIMARY KEY,
            version INTEGER NOT NULL,
            owner VARCHAR(120) NOT NULL,
            description VARCHAR(400) NOT NULL,
            schema JSONB NOT NULL,
            active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_event_catalog_owner ON event_catalog (owner)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_event_catalog_active ON event_catalog (active)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_event_catalog_active")
    op.execute("DROP INDEX IF EXISTS ix_event_catalog_owner")
    op.execute("DROP TABLE IF EXISTS event_catalog")
    op.execute("DROP INDEX IF EXISTS ix_op_event_store_created_at")
    op.execute("DROP INDEX IF EXISTS ix_op_event_store_region_code")
    op.execute("DROP INDEX IF EXISTS ix_op_event_store_tenant_id")
    op.execute("DROP INDEX IF EXISTS ix_op_event_store_event_type")
    op.execute("DROP INDEX IF EXISTS ix_op_event_store_aggregate_id")
    op.execute("DROP TABLE IF EXISTS op_event_store")
