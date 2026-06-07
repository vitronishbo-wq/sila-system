"""Create attachments table

Revision ID: 002_create_attachments
Revises: 001_create_service_requests
Create Date: 2026-02-18
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

revision = "002_create_attachments"
down_revision = "001_create_service_requests"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "service_request_attachments",
        sa.Column("id", UUID(as_uuid=True), nullable=False),
        sa.Column("request_id", UUID(as_uuid=True), nullable=False),
        sa.Column("filename", sa.String(255), nullable=False),
        sa.Column("content_type", sa.String(100), nullable=False),
        sa.Column("storage_url", sa.String(2000), nullable=False),
        sa.Column("uploaded_by", UUID(as_uuid=True), nullable=False),
        sa.Column("size_bytes", sa.Integer, nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["request_id"], ["service_requests.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_service_request_attachments_request", "service_request_attachments", ["request_id"]
    )
    op.create_index(
        "ix_service_request_attachments_created", "service_request_attachments", ["created_at"]
    )


def downgrade():
    op.drop_table("service_request_attachments")
