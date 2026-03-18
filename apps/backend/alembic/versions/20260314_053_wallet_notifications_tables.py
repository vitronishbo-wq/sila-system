"""create wallet and notifications tables

Revision ID: 20260314_053_wallet_notifications_tables
Revises: 20260314_052_transportes_logistica_audit_columns
Create Date: 2026-03-14 12:30:00.000000
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260314_053_wallet_notifications_tables"
down_revision = "20260314_052_transportes_logistica_audit_columns"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "wallet_documents",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("citizen_id", sa.String(), nullable=False),
        sa.Column("document_type", sa.String(), nullable=False),
        sa.Column("file_url", sa.String(), nullable=False),
        sa.Column("issued_at", sa.DateTime(), nullable=True),
        sa.Column("valid_until", sa.DateTime(), nullable=True),
    )
    op.create_index(
        "ix_wallet_documents_citizen_id",
        "wallet_documents",
        ["citizen_id"],
    )

    op.create_table(
        "notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("citizen_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("channel", sa.String(), nullable=True),
    )
    op.create_index(
        "ix_notifications_citizen_id",
        "notifications",
        ["citizen_id"],
    )

    op.create_table(
        "notification_deliveries",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "notification_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("notifications.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("channel", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("delivered_at", sa.DateTime(), nullable=True),
    )

    op.create_table(
        "notification_preferences",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("citizen_id", sa.String(), nullable=False),
        sa.Column("channel", sa.String(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.text("true")),
    )
    op.create_index(
        "ix_notification_preferences_citizen_id",
        "notification_preferences",
        ["citizen_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_notification_preferences_citizen_id", table_name="notification_preferences")
    op.drop_table("notification_preferences")
    op.drop_table("notification_deliveries")
    op.drop_index("ix_notifications_citizen_id", table_name="notifications")
    op.drop_table("notifications")
    op.drop_index("ix_wallet_documents_citizen_id", table_name="wallet_documents")
    op.drop_table("wallet_documents")
