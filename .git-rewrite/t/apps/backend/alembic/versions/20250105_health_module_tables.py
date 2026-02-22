"""Create health module tables

Revision ID: 20250105_health
Revises: a1b2c3d4e5f6
Create Date: 2025-01-05 12:00:00.000000+00:00
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20250105_health"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade(engine_name: str = "") -> None:
    """Upgrade database schema and/or data, creating a new revision.

    Args:
        engine_name: Database engine name. If not provided, applies to all engines.
    """
    if engine_name and engine_name != "postgresql":
        return

    with op.get_context().begin_transaction():
        # ========================================================================
        # Health Services Table
        # ========================================================================
        op.create_table(
            "health_services",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("name", sa.String(length=255), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("category", sa.String(length=100), nullable=True),
            sa.Column(
                "status",
                sa.String(length=50),
                nullable=False,
                server_default="available",
            ),
            sa.Column("estimated_duration", sa.String(length=50), nullable=True),
            sa.Column("requirements", sa.Text(), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            op.f("ix_health_services_id"), "health_services", ["id"], unique=False
        )
        op.create_index(
            op.f("ix_health_services_category"),
            "health_services",
            ["category"],
            unique=False,
        )
        op.create_index(
            op.f("ix_health_services_status"),
            "health_services",
            ["status"],
            unique=False,
        )
        op.create_index(
            op.f("ix_health_services_deleted_at"),
            "health_services",
            ["deleted_at"],
            unique=False,
        )

        # ========================================================================
        # Health Records Table
        # ========================================================================
        op.create_table(
            "health_records",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("patient_name", sa.String(length=255), nullable=True),
            sa.Column("diagnosis", sa.Text(), nullable=True),
            sa.Column("notes", sa.Text(), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            op.f("ix_health_records_id"), "health_records", ["id"], unique=False
        )
        op.create_index(
            op.f("ix_health_records_user_id"),
            "health_records",
            ["user_id"],
            unique=False,
        )
        op.create_index(
            op.f("ix_health_records_deleted_at"),
            "health_records",
            ["deleted_at"],
            unique=False,
        )

        # ========================================================================
        # Appointments Table
        # ========================================================================
        op.create_table(
            "appointments",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("service_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("scheduled_date", sa.DateTime(timezone=True), nullable=False),
            sa.Column("notes", sa.Text(), nullable=True),
            sa.Column(
                "status",
                sa.String(length=50),
                nullable=False,
                server_default="scheduled",
            ),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(
                ["service_id"], ["health_services.id"], ondelete="RESTRICT"
            ),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            op.f("ix_appointments_id"), "appointments", ["id"], unique=False
        )
        op.create_index(
            op.f("ix_appointments_user_id"), "appointments", ["user_id"], unique=False
        )
        op.create_index(
            op.f("ix_appointments_service_id"),
            "appointments",
            ["service_id"],
            unique=False,
        )
        op.create_index(
            op.f("ix_appointments_scheduled_date"),
            "appointments",
            ["scheduled_date"],
            unique=False,
        )
        op.create_index(
            op.f("ix_appointments_status"), "appointments", ["status"], unique=False
        )
        op.create_index(
            op.f("ix_appointments_deleted_at"),
            "appointments",
            ["deleted_at"],
            unique=False,
        )

        # ========================================================================
        # Medical Records Table
        # ========================================================================
        op.create_table(
            "medical_records",
            sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("appointment_id", postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column("diagnosis", sa.Text(), nullable=True),
            sa.Column("treatment", sa.Text(), nullable=True),
            sa.Column("notes", sa.Text(), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column(
                "updated_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=False,
            ),
            sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(
                ["appointment_id"], ["appointments.id"], ondelete="CASCADE"
            ),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("appointment_id"),
        )
        op.create_index(
            op.f("ix_medical_records_id"), "medical_records", ["id"], unique=False
        )
        op.create_index(
            op.f("ix_medical_records_appointment_id"),
            "medical_records",
            ["appointment_id"],
            unique=True,
        )
        op.create_index(
            op.f("ix_medical_records_deleted_at"),
            "medical_records",
            ["deleted_at"],
            unique=False,
        )


def downgrade(engine_name: str = "") -> None:
    """Downgrade database schema and/or data back to the previous revision.

    Args:
        engine_name: Database engine name. If not provided, applies to all engines.
    """
    if engine_name and engine_name != "postgresql":
        return

    with op.get_context().begin_transaction():
        # Drop tables in reverse order (respecting foreign key constraints)
        op.drop_table("medical_records")
        op.drop_table("appointments")
        op.drop_table("health_records")
        op.drop_table("health_services")
