"""Create provider operations tables (certification, contracts, sla snapshots)

Revision ID: 20260607_0001_create_provider_operations_tables
Revises: 20260606_0900_add_educacao_identity_tables
Create Date: 2026-06-07 05:30:00.000000
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision: str = "20260607_0001_create_provider_operations_tables"
down_revision: str = "20260606_0900_add_educacao_identity_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # TASK-097: Provider Certification
    op.create_table(
        "provider_certifications",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("provider", sa.String(length=100), nullable=False, index=True),
        sa.Column("environment", sa.String(length=50), nullable=False, server_default="homologation"),
        sa.Column(
            "certification_status",
            sa.Enum("mock", "homologation", "certified", "production", "suspended", name="cert_status"),
            nullable=False,
            server_default="mock",
        ),
        sa.Column("approved_by", sa.String(length=200), nullable=True),
        sa.Column("approval_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expiration_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(length=50), nullable=True),
        sa.Column("updated_by", sa.String(length=50), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_cert_provider", "provider_certifications", ["provider", "created_at"])

    # TASK-098: Contract Registry
    op.create_table(
        "provider_contracts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("provider", sa.String(length=100), nullable=False, index=True),
        sa.Column("contract_number", sa.String(length=100), nullable=False),
        sa.Column("entity", sa.String(length=200), nullable=False),
        sa.Column("signed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "status",
            sa.Enum("draft", "active", "suspended", "terminated", name="contract_status"),
            nullable=False,
            server_default="draft",
        ),
        sa.Column("terms", sa.Text(), nullable=True),
        sa.Column("metadata", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(length=50), nullable=True),
        sa.Column("updated_by", sa.String(length=50), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_contract_provider", "provider_contracts", ["provider", "created_at"])

    # TASK-099: SLA Snapshots
    op.create_table(
        "provider_sla_snapshots",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("provider", sa.String(length=100), nullable=False, index=True),
        sa.Column("availability", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("latency_p95", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("latency_p99", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("error_rate", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("mttr", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("mtbf", sa.Float(), nullable=False, server_default="0.0"),
        sa.Column("snapshot_timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("created_by", sa.String(length=50), nullable=True),
        sa.Column("updated_by", sa.String(length=50), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_snap_provider_ts", "provider_sla_snapshots", ["provider", "snapshot_timestamp"])


def downgrade() -> None:
    op.drop_table("provider_sla_snapshots")
    op.drop_table("provider_contracts")
    op.drop_table("provider_certifications")
    op.execute("DROP TYPE IF EXISTS cert_status")
    op.execute("DROP TYPE IF EXISTS contract_status")
