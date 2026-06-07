"""create economy financas tables

Revision ID: 20260318_1700_create_economy_financas_tables
Revises: 20260318_1510_merge_locations_cascade_head
Create Date: 2026-03-18 17:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision: str = "20260318_1700_create_economy_financas_tables"
down_revision = "20260318_1510_merge_locations_cascade_head"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "economy_invoices",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("citizen_id", sa.String(64), nullable=False),
        sa.Column("reference", sa.String(64), nullable=False, unique=True),
        sa.Column("revenue_code", sa.String(32), nullable=False),
        sa.Column("cost_center", sa.String(32), nullable=False),
        sa.Column("service_code", sa.String(64), nullable=False),
        sa.Column("service_name", sa.String(255), nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column("due_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("request_id", sa.String(64), nullable=True),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_economy_invoices_citizen_id", "economy_invoices", ["citizen_id"])
    op.create_index("ix_economy_invoices_reference", "economy_invoices", ["reference"], unique=True)
    op.create_index("ix_economy_invoices_status", "economy_invoices", ["status"])
    op.create_index("ix_economy_invoices_service_code", "economy_invoices", ["service_code"])

    op.create_table(
        "economy_payments",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "invoice_id",
            sa.String(36),
            sa.ForeignKey("economy_invoices.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("citizen_id", sa.String(64), nullable=False),
        sa.Column("amount", sa.Numeric(14, 2), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("gateway_reference", sa.String(128), nullable=False, unique=True),
        sa.Column("payment_method", sa.String(64), nullable=False),
        sa.Column("status", sa.String(32), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_economy_payments_invoice_id", "economy_payments", ["invoice_id"])
    op.create_index("ix_economy_payments_citizen_id", "economy_payments", ["citizen_id"])
    op.create_index(
        "ix_economy_payments_gateway_reference",
        "economy_payments",
        ["gateway_reference"],
        unique=True,
    )
    op.create_index("ix_economy_payments_status", "economy_payments", ["status"])


def downgrade() -> None:
    op.drop_index("ix_economy_payments_status", table_name="economy_payments")
    op.drop_index("ix_economy_payments_gateway_reference", table_name="economy_payments")
    op.drop_index("ix_economy_payments_citizen_id", table_name="economy_payments")
    op.drop_index("ix_economy_payments_invoice_id", table_name="economy_payments")
    op.drop_table("economy_payments")
    op.drop_index("ix_economy_invoices_service_code", table_name="economy_invoices")
    op.drop_index("ix_economy_invoices_status", table_name="economy_invoices")
    op.drop_index("ix_economy_invoices_reference", table_name="economy_invoices")
    op.drop_index("ix_economy_invoices_citizen_id", table_name="economy_invoices")
    op.drop_table("economy_invoices")
