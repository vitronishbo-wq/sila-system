"""create operational flow tables for orders/documents/payments

Revision ID: 20260228_003_operational_flow
Revises: 20260228_002_catalog_schema
Create Date: 2026-02-28 02:50:00.000000
"""

from alembic import op


revision = "20260228_003_operational_flow"
down_revision = "20260228_002_catalog_schema"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS operational_orders (
            id UUID PRIMARY KEY,
            citizen_id UUID NOT NULL,
            service_id UUID NOT NULL REFERENCES services(id) ON DELETE RESTRICT,
            workflow_instance_id UUID NOT NULL,
            total_amount NUMERIC(12, 2) NOT NULL,
            status VARCHAR(32) NOT NULL,
            status_history JSONB NOT NULL,
            receipt_number VARCHAR(64) UNIQUE,
            proof_payload JSONB,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            submitted_at TIMESTAMPTZ,
            completed_at TIMESTAMPTZ
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS operational_order_documents (
            id UUID PRIMARY KEY,
            order_id UUID NOT NULL REFERENCES operational_orders(id) ON DELETE CASCADE,
            filename VARCHAR(255) NOT NULL,
            content_type VARCHAR(120) NOT NULL,
            size_bytes INTEGER NOT NULL,
            uri VARCHAR(500),
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        )
        """
    )
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS operational_payments (
            id UUID PRIMARY KEY,
            order_id UUID NOT NULL REFERENCES operational_orders(id) ON DELETE CASCADE,
            reference VARCHAR(64) NOT NULL UNIQUE,
            amount NUMERIC(12, 2) NOT NULL,
            status VARCHAR(24) NOT NULL,
            provider VARCHAR(40) NOT NULL,
            failure_reason VARCHAR(255),
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            confirmed_at TIMESTAMPTZ
        )
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_operational_orders_citizen_id ON operational_orders (citizen_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_operational_orders_service_id ON operational_orders (service_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_operational_orders_status ON operational_orders (status)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_operational_orders_workflow_instance_id "
        "ON operational_orders (workflow_instance_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_operational_order_documents_order_id "
        "ON operational_order_documents (order_id)"
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_operational_payments_order_id ON operational_payments (order_id)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_operational_payments_reference ON operational_payments (reference)")
    op.execute("CREATE INDEX IF NOT EXISTS ix_operational_payments_status ON operational_payments (status)")


def downgrade():
    op.execute("DROP INDEX IF EXISTS ix_operational_payments_status")
    op.execute("DROP INDEX IF EXISTS ix_operational_payments_reference")
    op.execute("DROP INDEX IF EXISTS ix_operational_payments_order_id")
    op.execute("DROP INDEX IF EXISTS ix_operational_order_documents_order_id")
    op.execute("DROP INDEX IF EXISTS ix_operational_orders_workflow_instance_id")
    op.execute("DROP INDEX IF EXISTS ix_operational_orders_status")
    op.execute("DROP INDEX IF EXISTS ix_operational_orders_service_id")
    op.execute("DROP INDEX IF EXISTS ix_operational_orders_citizen_id")
    op.execute("DROP TABLE IF EXISTS operational_payments")
    op.execute("DROP TABLE IF EXISTS operational_order_documents")
    op.execute("DROP TABLE IF EXISTS operational_orders")
