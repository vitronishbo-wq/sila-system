"""add audit columns to economy tables

Revision ID: 20260318_1715_add_economy_audit_columns
Revises: 20260318_1700_create_economy_financas_tables
Create Date: 2026-03-18 17:15:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision: str = "20260318_1715_add_economy_audit_columns"
down_revision = "20260318_1700_create_economy_financas_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("economy_invoices", sa.Column("created_by", sa.String(50), nullable=True))
    op.add_column("economy_invoices", sa.Column("updated_by", sa.String(50), nullable=True))
    op.add_column(
        "economy_invoices",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.add_column(
        "economy_payments",
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()
        ),
    )
    op.add_column("economy_payments", sa.Column("created_by", sa.String(50), nullable=True))
    op.add_column("economy_payments", sa.Column("updated_by", sa.String(50), nullable=True))
    op.add_column(
        "economy_payments",
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )


def downgrade() -> None:
    op.drop_column("economy_payments", "is_active")
    op.drop_column("economy_payments", "updated_by")
    op.drop_column("economy_payments", "created_by")
    op.drop_column("economy_payments", "updated_at")

    op.drop_column("economy_invoices", "is_active")
    op.drop_column("economy_invoices", "updated_by")
    op.drop_column("economy_invoices", "created_by")
