"""create obras_publicas saga and dashboard read model tables

Revision ID: 20260305_043_obras_publicas_saga_cqrs
Revises: 20260304_042_obras_publicas_outbox_events
Create Date: 2026-03-05 00:40:00.000000
"""

from __future__ import annotations

from alembic import op


revision = "20260305_043_obras_publicas_saga_cqrs"
down_revision = "20260304_042_obras_publicas_outbox_events"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS op_sagas (
            id UUID PRIMARY KEY,
            saga_type VARCHAR(120) NOT NULL,
            correlation_id VARCHAR(160) NOT NULL,
            tenant_id VARCHAR(80) NOT NULL,
            state VARCHAR(80) NOT NULL,
            data JSONB NOT NULL,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            completed_at TIMESTAMPTZ
        )
        """
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS op_dashboard_read (
            obra_id VARCHAR(120) PRIMARY KEY,
            tenant_id VARCHAR(80) NOT NULL,
            codigo VARCHAR(80) NOT NULL,
            status VARCHAR(80) NOT NULL,
            valor_total NUMERIC(18,2) NOT NULL DEFAULT 0,
            valor_executado NUMERIC(18,2) NOT NULL DEFAULT 0,
            percentual_execucao NUMERIC(7,2) NOT NULL DEFAULT 0,
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS ix_op_sagas_saga_type ON op_sagas (saga_type)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_sagas_correlation_id ON op_sagas (correlation_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_sagas_tenant_id ON op_sagas (tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_sagas_state ON op_sagas (state)")
    op.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS uq_op_sagas_tenant_type_correlation "
        "ON op_sagas (tenant_id, saga_type, correlation_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_dashboard_read_tenant_id ON op_dashboard_read (tenant_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_dashboard_read_codigo ON op_dashboard_read (codigo)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_op_dashboard_read_status ON op_dashboard_read (status)")


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_op_dashboard_read_status")
    op.execute("DROP INDEX IF EXISTS ix_op_dashboard_read_codigo")
    op.execute("DROP INDEX IF EXISTS ix_op_dashboard_read_tenant_id")
    op.execute("DROP INDEX IF EXISTS uq_op_sagas_tenant_type_correlation")
    op.execute("DROP INDEX IF EXISTS ix_op_sagas_state")
    op.execute("DROP INDEX IF EXISTS ix_op_sagas_tenant_id")
    op.execute("DROP INDEX IF EXISTS ix_op_sagas_correlation_id")
    op.execute("DROP INDEX IF EXISTS ix_op_sagas_saga_type")
    op.execute("DROP TABLE IF EXISTS op_dashboard_read")
    op.execute("DROP TABLE IF EXISTS op_sagas")
