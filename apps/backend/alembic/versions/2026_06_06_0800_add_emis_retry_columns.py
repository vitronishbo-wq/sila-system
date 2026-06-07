"""add retry_count and next_retry_at to educacao_emis_sync_log

Revision ID: 20260606_0800_add_emis_retry_columns
Revises: 20260606_0700_create_emis_sync_log
Create Date: 2026-06-06 08:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

revision = "20260606_0800_add_emis_retry_columns"
down_revision = "20260606_0700_create_emis_sync_log"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "educacao_emis_sync_log",
        sa.Column("retry_count", sa.Integer(), nullable=False, server_default=sa.text("0")),
    )
    op.add_column(
        "educacao_emis_sync_log",
        sa.Column("next_retry_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade():
    op.drop_column("educacao_emis_sync_log", "next_retry_at")
    op.drop_column("educacao_emis_sync_log", "retry_count")
