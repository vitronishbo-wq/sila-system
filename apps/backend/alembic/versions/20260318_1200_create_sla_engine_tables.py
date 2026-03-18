"""Create SLA engine tables

Revision ID: 20260318_1200_create_sla_engine_tables
Revises: 20260316_1130_export_job_logs
Create Date: 2026-03-18 12:00:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision: str = "20260318_1200_create_sla_engine_tables"
down_revision: str = "9a1d2b7c3e10"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sla_base",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("service_id", sa.String(length=100), nullable=False),
        sa.Column("service_name", sa.String(length=200), nullable=False),
        sa.Column("service_description", sa.String(length=500), nullable=True),
        sa.Column("module", sa.String(length=50), nullable=False),
        sa.Column("base_hours", sa.Float(), nullable=False),
        sa.Column("priority", sa.String(length=20), nullable=False),
        sa.Column("tier", sa.String(length=20), nullable=False),
        sa.Column("legal_basis", sa.String(length=200), nullable=True),
        sa.Column("version", sa.String(length=10), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("created_by", sa.String(length=100), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.UniqueConstraint("service_id", name="uq_sla_base_service_id"),
    )
    op.create_index("ix_sla_base_service_id", "sla_base", ["service_id"])
    op.create_index("ix_sla_base_module", "sla_base", ["module"])

    op.create_table(
        "sla_policies",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("scope", sa.String(length=20), nullable=False),
        sa.Column("scope_id", sa.String(length=100), nullable=False),
        sa.Column("service_id", sa.String(length=100), nullable=True),
        sa.Column("multiplier", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("max_hours", sa.Float(), nullable=True),
        sa.Column("min_hours", sa.Float(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("reason", sa.String(length=500), nullable=True),
        sa.Column("effective_from", sa.DateTime(), nullable=False),
        sa.Column("effective_to", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("created_by", sa.String(length=100), nullable=True),
    )
    op.create_index("ix_sla_policies_scope_id", "sla_policies", ["scope_id"])
    op.create_index("ix_sla_policies_service_id", "sla_policies", ["service_id"])
    op.create_index("ix_sla_policies_effective", "sla_policies", ["effective_from", "effective_to"])

    op.create_table(
        "sla_overrides",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("conditions", sa.JSON(), nullable=False),
        sa.Column("multiplier", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_sla_overrides_priority", "sla_overrides", ["priority"])

    op.create_table(
        "sla_versions",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("version", sa.String(length=10), nullable=False),
        sa.Column("service_id", sa.String(length=100), nullable=False),
        sa.Column("base_hours", sa.Float(), nullable=False),
        sa.Column("changes", sa.JSON(), nullable=True),
        sa.Column("approved_by", sa.String(length=100), nullable=True),
        sa.Column("approved_at", sa.DateTime(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
    )
    op.create_index("ix_sla_versions_service_id", "sla_versions", ["service_id"])

    op.create_table(
        "sla_violations",
        sa.Column("id", sa.String(length=36), primary_key=True, nullable=False),
        sa.Column("request_id", sa.String(length=100), nullable=False),
        sa.Column("service_id", sa.String(length=100), nullable=False),
        sa.Column("target_hours", sa.Float(), nullable=False),
        sa.Column("actual_hours", sa.Float(), nullable=False),
        sa.Column("delta_hours", sa.Float(), nullable=False),
        sa.Column("context", sa.JSON(), nullable=True),
        sa.Column("province", sa.String(length=50), nullable=True),
        sa.Column("citizen_type", sa.String(length=20), nullable=True),
        sa.Column("channel", sa.String(length=20), nullable=True),
        sa.Column("escalated", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("escalation_level", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint("request_id", name="uq_sla_violations_request_id"),
    )
    op.create_index("ix_sla_violations_service_id", "sla_violations", ["service_id"])
    op.create_index("ix_sla_violations_province", "sla_violations", ["province"])
    op.create_index("ix_sla_violations_created_at", "sla_violations", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_sla_violations_province", table_name="sla_violations")
    op.drop_index("ix_sla_violations_service_id", table_name="sla_violations")
    op.drop_index("ix_sla_violations_created_at", table_name="sla_violations")
    op.drop_table("sla_violations")

    op.drop_index("ix_sla_versions_service_id", table_name="sla_versions")
    op.drop_table("sla_versions")

    op.drop_index("ix_sla_overrides_priority", table_name="sla_overrides")
    op.drop_table("sla_overrides")

    op.drop_index("ix_sla_policies_service_id", table_name="sla_policies")
    op.drop_index("ix_sla_policies_effective", table_name="sla_policies")
    op.drop_index("ix_sla_policies_scope_id", table_name="sla_policies")
    op.drop_table("sla_policies")

    op.drop_index("ix_sla_base_module", table_name="sla_base")
    op.drop_index("ix_sla_base_service_id", table_name="sla_base")
    op.drop_table("sla_base")
